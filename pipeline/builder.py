# -*- coding: utf-8 -*-
"""Pipeline único de geração de conteúdo (config-driven).

Consolida o antigo fluxo de 8 agentes (intro → outline → desenvolvimento →
conclusão → unificador → linkagem → revisor → executor) em 3 agentes:

    1) redator   — escreve o corpo completo já estruturado, com extensão controlada;
    2) linkador  — insere links internos do catálogo + externos autoritativos;
    3) revisor   — revisa NO LUGAR e devolve o HTML final (não gera JSON).

Cada task fixa explicitamente seu `context`, então nenhum agente reconstrói o post
a partir de uma versão pré-linkagem (causa do bug de perda de links). A assinatura
é anexada depois, de forma determinística (ver core/content.py).
"""
from crewai import Crew, Agent, Task, LLM
from crews._common import REGRA_KEYWORD
from core.models import ClientConfig
from core.serp import buscar_serp, texto_concorrencia, selecionar_externos

_LLM_REDATOR = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})
_LLM_REVISOR = LLM(model="gemini/gemini-2.5-flash", temperature=0.4)  # com raciocínio: melhor julgamento


def _tom(cfg: ClientConfig) -> str:
    """Diretriz de tom/CTA derivada do segmento do cliente."""
    if cfg.is_etico:
        return (
            "Tom estritamente educativo e acolhedor (segmento regulado). NUNCA prometer "
            "resultado, dar tom de diagnóstico ou criar urgência ('agende agora', 'não "
            "adie', 'transforme'). Prefira 'pode estar associado', 'a avaliação "
            "profissional é recomendada', 'a conduta depende do caso'."
        )
    return (
        "Tom profissional e persuasivo, porém honesto. Pode usar CTA comercial leve e "
        "destacar benefícios, sem promessas exageradas nem alegações infundadas."
    )


def build_crew(cfg: ClientConfig, tema: str, palavra_chave: str) -> Crew:
    serp = buscar_serp(palavra_chave)                       # 1 única chamada à SERP
    concorrencia = texto_concorrencia(serp)
    externos = selecionar_externos(serp, cfg.whitelist_externos, max_links=2)

    p_min, p_max = cfg.target_palavras
    teto = cfg.teto_palavras
    tom = _tom(cfg)

    links_internos_txt = "\n".join(
        f"- {li.titulo}: {li.url} | âncora sugerida: {li.anchor}" for li in cfg.links_internos
    )
    links_externos_txt = "\n".join(
        f"- {e['titulo']}: {e['url']} | âncora: {e['anchor']}" for e in externos
    ) or "(nenhum externo autorizado encontrado)"

    # ── 1) Redator ────────────────────────────────────────────────────────────
    redator = Agent(
        role=f"Redator de Conteúdo SEO — {cfg.especialidade}",
        goal=(
            f"Escrever um post de blog completo e estruturado sobre o tema, com "
            f"introdução, exatamente 5 H2 numerados (máx. 1 H3 cada) e conclusão, "
            f"entre {p_min} e {p_max} palavras (jamais acima de {teto})."
        ),
        backstory=(
            f"Redator especializado em {cfg.especialidade}, referência em conteúdo "
            f"educativo de qualidade para {cfg.nome}. Escreve com profundidade, "
            f"clareza e precisão, conectando o tema à realidade do leitor."
        ),
        verbose=True, allow_delegation=False, llm=_LLM_REDATOR,
        max_iter=12, max_execution_time=300,
    )
    tarefa_redacao = Task(
        description=f"""
Escreva um POST DE BLOG completo em HTML (body only) sobre '{tema}', otimizado para a palavra-chave '{palavra_chave}'.

ESTRUTURA OBRIGATÓRIA (em uma única saída):
- Introdução: 2–3 <p> acolhedores, citando a palavra-chave 1x de forma natural.
- Corpo: EXATAMENTE 5 <h2> numerados (1., 2., ...), no máximo 1 <h3> por seção. Use <p> curtos e <ul><li> quando listar.
  Contemple: o que é, quem se beneficia, como funciona na prática, cuidados/critérios e quando buscar um especialista (inclua mitos e verdades).
- Conclusão: 1–2 <p> de síntese encorajadora, sem CTA.

EXTENSÃO: entre {p_min} e {p_max} palavras no total. NUNCA ultrapasse {teto}. Não repita conteúdo entre seções.

{REGRA_KEYWORD}

TOM: {tom}

QUALIDADE OBRIGATÓRIA:
- SEO local: insira "{cfg.localidade}" de forma natural no corpo (mínimo 2 menções, sem repetição artificial).
- Conexão com o serviço: relacione o tema aos serviços reais do cliente — {cfg.servicos_resumo}.
- Profundidade: traga causas, sinais, critérios de avaliação, exemplos práticos e orientações concretas. Evite generalidades vagas.
- Semântica/entidades: use sinônimos, termos correlatos e subtemas do domínio (reforça autoridade temática e intenção de busca).

PROIBIDO: <h1>, imagens, estilos inline, <html>/<head>/<body>, CTA comercial no corpo, blocos de assinatura/telefone/WhatsApp (anexados depois).
Comece a saída direto pela primeira tag de bloco.

Concorrência (referência de cobertura, não copie):
{concorrencia}""".strip(),
        expected_output="HTML body-only: intro em <p>, 5 <h2> numerados com <p>/<ul>, conclusão em <p>.",
        agent=redator,
    )

    # ── 2) Linkador ───────────────────────────────────────────────────────────
    linkador = Agent(
        role=f"Planejador de Linkagem — {cfg.nome}",
        goal="Inserir links internos e externos de forma natural, distribuída e relevante.",
        backstory="Especialista em internal linking e EEAT; prioriza fontes oficiais e autoritativas.",
        verbose=True, allow_delegation=False, llm=_LLM_REDATOR,
        max_iter=10, max_execution_time=240,
    )
    tarefa_linkagem = Task(
        description=f"""
Insira LINKAGEM no HTML recebido (saída do redator), sem reescrever o conteúdo.

Links internos (use >= 3):
{links_internos_txt}

Links externos (use >= 1 se listado; com target="_blank" rel="noopener noreferrer"):
{links_externos_txt}

REGRAS:
- Âncoras descritivas (nunca "clique aqui"); não linke em headings; sem inline style; sem imagens.
- PROIBIDO inventar URLs: use SOMENTE as URLs exatas listadas acima.
- Nunca crie caminhos relativos (ex.: /alguma-pagina), âncoras placeholder ou páginas fora do catálogo.
- Se um trecho não tem link interno adequado, deixe-o sem link em vez de inventar destino.
Devolva o HTML completo com os links aplicados.""".strip(),
        expected_output="HTML body-only com links internos/externos aplicados.",
        agent=linkador,
        context=[tarefa_redacao],
    )

    # ── 3) Revisor (revisa no lugar) ──────────────────────────────────────────
    revisor = Agent(
        role=f"Revisor Sênior — {cfg.especialidade}",
        goal="Revisar e entregar o HTML final polido, preservando estrutura e todos os links do catálogo.",
        backstory="Revisor PT-BR meticuloso; melhora clareza, tom e SEO sem quebrar a marcação nem remover links válidos.",
        verbose=True, allow_delegation=False, llm=_LLM_REVISOR,
        max_iter=10, max_execution_time=240,
    )
    tarefa_revisao = Task(
        description=f"""
Revise o HTML COM LINKS (saída da linkagem) e devolva a VERSÃO FINAL já corrigida (HTML, não JSON).

Aplique melhorias de: ortografia PT-BR, fluidez, tom adequado, distribuição dos links, alinhamento à intenção de busca e à palavra-chave '{palavra_chave}'.
{tom}

REGRA INEGOCIÁVEL SOBRE LINKS: mantenha TODOS os <a> que apontam para o domínio oficial '{cfg.dominio_oficial}'. Esses são links internos legítimos do catálogo — no máximo melhore o texto da âncora, NUNCA remova o link nem invente novas URLs.

Mantenha: 5 H2 numerados, ausência de <h1>/imagens, extensão entre {p_min} e {p_max} palavras (máx. {teto}).
NÃO adicione assinatura, telefone ou WhatsApp — isso é anexado depois, fora do seu escopo.
Comece a saída direto pela primeira tag de bloco.""".strip(),
        expected_output="HTML final (body only), revisado, com todos os links internos do catálogo preservados.",
        agent=revisor,
        context=[tarefa_linkagem],
    )

    return Crew(
        agents=[redator, linkador, revisor],
        tasks=[tarefa_redacao, tarefa_linkagem, tarefa_revisao],
        verbose=True,
    )

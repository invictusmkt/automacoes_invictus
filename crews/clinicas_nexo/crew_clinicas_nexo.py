# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from crewai import Crew, Agent, Task
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(temperature=0.4)

# -------------------------------
# Catálogo fixo de links internos (Instituto Nexo)
# -------------------------------
LINKS_INTERNOS_NEXO = [
    {
        "titulo": "Home — Instituto Nexo",
        "url": "https://vivanexo.com.br/",
        "anchor_sugerida": "Instituto Nexo de Psicologia Aplicada"
    },
    {
        "titulo": "O Nexo — Sobre o Instituto",
        "url": "https://vivanexo.com.br/o-nexo/",
        "anchor_sugerida": "conheça a missão e os valores do Instituto Nexo"
    },
    {
        "titulo": "Psicoterapia Individual",
        "url": "https://vivanexo.com.br/servico/psicoterapia-individual/",
        "anchor_sugerida": "psicoterapia para crianças, adultos e idosos"
    },
    {
        "titulo": "Terapia ABA para TEA",
        "url": "https://vivanexo.com.br/servico/psicoterapia-aba/",
        "anchor_sugerida": "terapia ABA para pessoas com autismo"
    },
    {
        "titulo": "Avaliação Neuropsicológica",
        "url": "https://vivanexo.com.br/servico/avaliacao-neuropsicologica/",
        "anchor_sugerida": "avaliação neuropsicológica completa"
    },
    {
        "titulo": "Socialização TEA",
        "url": "https://vivanexo.com.br/servico/socializacao/",
        "anchor_sugerida": "grupos de socialização para pessoas com TEA"
    },
    {
        "titulo": "Atividades da Vida Diária (AVD/AIVD)",
        "url": "https://vivanexo.com.br/servico/atividade-da-vida-diaria-avd-e-atividade-instrumental-da-vida-diaria-aivd/",
        "anchor_sugerida": "desenvolvimento de habilidades para a vida diária"
    },
    {
        "titulo": "Notícias e Blog",
        "url": "https://vivanexo.com.br/noticias/",
        "anchor_sugerida": "conteúdos sobre saúde mental e psicologia"
    },
    {
        "titulo": "Unidades",
        "url": "https://vivanexo.com.br/unidades/",
        "anchor_sugerida": "encontre uma unidade Nexo perto de você"
    },
]

WHATSAPP_NEXO = "https://api.whatsapp.com/send/?phone=551934065984&text=Oi!%20Encontrei%20o%20Instituto%20Nexo%20no%20Google%20e%20gostaria%20de%20mais%20informações.&type=phone_number&app_absent=0"

# -------------------------------
# SERP helper + whitelist para externos (saúde mental / psicologia)
# -------------------------------
WHITELIST_EXTERNOS = [
    # Autoridades governamentais / saúde
    ".gov", ".gov.br", ".edu", ".edu.br",
    "saude.gov.br", "who.int", "nih.gov",
    # Conselhos profissionais de psicologia
    "cfp.org.br", "crp.org.br",
    # Referências sobre autismo e saúde mental no Brasil
    "autismo.org.br", "ama.org.br", "abda.org.br",
    # Google / SEO
    "developers.google.com", "support.google.com",
    "schema.org", "w3.org",
    "moz.com", "ahrefs.com", "semrush.com",
]

def _usa_whitelist(url: str) -> bool:
    url_l = (url or "").lower()
    return any(dom in url_l for dom in WHITELIST_EXTERNOS)

def buscar_concorrentes_serpapi_struct(palavra_chave: str) -> list[dict]:
    search = GoogleSearch({
        "q": palavra_chave,
        "hl": "pt-br",
        "gl": "br",
        "num": 10,
        "api_key": os.getenv("SERPAPI_API_KEY")
    })
    d = search.get_dict()
    return d.get("organic_results", []) or []

def selecionar_links_externos_autoritativos(resultados_serp: list[dict], max_links: int = 2) -> list[dict]:
    candidatos, vistos = [], set()
    for r in resultados_serp:
        url = r.get("link") or r.get("url") or ""
        titulo = (r.get("title") or "").strip()
        if not url or url in vistos:
            continue
        if _usa_whitelist(url):
            candidatos.append({
                "titulo": titulo[:90] or "Fonte externa",
                "url": url,
                "anchor_sugerida": (titulo[:70].lower() or "fonte oficial")
            })
            vistos.add(url)
        if len(candidatos) >= max_links:
            break
    return candidatos

def buscar_concorrentes_serpapi_texto(palavra_chave: str) -> str:
    results = buscar_concorrentes_serpapi_struct(palavra_chave)
    output = []
    for res in results:
        titulo = res.get("title", "")
        snippet = res.get("snippet", "")
        link = res.get("link", "") or res.get("url", "")
        output.append(f"Título: {titulo}\nTrecho: {snippet}\nURL: {link}\n")
    return "\n".join(output)

# -------------------------------
# Função principal — Instituto Nexo de Psicologia Aplicada
# -------------------------------
def build_crew_clinicasnexo(tema: str, palavra_chave: str):
    """
    Gera SOMENTE o conteúdo do post (HTML do body), pronto para WordPress,
    no tom do Instituto Nexo: acolhedor, profissional, baseado em evidências.

    Público: crianças, adolescentes, adultos, idosos, atletas, vestibulandos,
    pessoas com TEA e seus familiares.

    Estilo de saída:
    - Introdução com 1–2 links naturais em <p>.
    - <h2> numerados: "1. ...", "2. ..."; <h3> opcionais.
    - Parágrafos curtos (2–4 linhas); listas <ul><li> quando fizer sentido.
    - Pelo menos UM heading contém a palavra-chave.
    - Sem <h1> e sem imagens.
    - Mínimo 1200 palavras.
    - Linkagem: >=3 internos distribuídos e >=1 externo (se disponível na whitelist).
    - Âncoras descritivas; externos com target="_blank" rel="noopener noreferrer".
    - Conclusão sem CTA comercial; CTA na assinatura ao final.
    - Linguagem empática, sem julgamentos, baseada em evidências científicas.
    """
    llm_local = llm

    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_NEXO[:]
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    # ==== Agentes ====
    agente_intro = Agent(
        role="Redator de Introdução — Saúde Mental e Psicologia",
        goal="Escrever introdução acolhedora e empática (2–3 parágrafos), citando a palavra-chave 1x, sem estigmatizar e sem promessas de cura.",
        backstory="Profissional de comunicação em saúde mental que traduz conceitos técnicos com linguagem acessível, inclusiva e não-julgadora.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) — Psicologia e TEA",
        goal="Definir 5–7 H2 numerados com H3 opcionais; contemplar jornada do paciente/família, evidências científicas, indicações e próximos passos.",
        backstory="Especialista em outline SEO para clínicas de saúde mental; foca na intenção de busca de familiares e pacientes.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento — Psicologia Aplicada",
        goal="Preencher cada seção com <p> curtos e listas, cobrindo: o que é, indicações, como funciona o processo, expectativas realistas, evidências e dicas práticas.",
        backstory="Conteúdo baseado em evidências, empático e acessível para leigos; sem linguagem clínica excessiva e sem promessas.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_conclusao = Agent(
        role="Redator de Conclusão — Próximos Passos em Saúde Mental",
        goal="Encerrar com síntese objetiva, próximos passos práticos e encorajamento gentil para buscar apoio profissional.",
        backstory="Foco em empoderamento, redução de estigma e decisão informada.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (apenas body), coerente, sem redundância, com numeração dos H2 e sem imagens.",
        backstory="Editor técnico focado em semântica, legibilidade e consistência.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_linkagem = Agent(
        role="Planejador e Implementador de Linkagem — Instituto Nexo",
        goal="Inserir links internos/externos de forma natural, distribuída e compatível com EEAT em saúde.",
        backstory="Especialista em internal linking para institutos de saúde; prioriza fontes oficiais (CFP, CRP, gov.br) e páginas de serviços do Nexo.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_assinatura = Agent(
        role="Responsável por Assinatura — Instituto Nexo",
        goal="Anexar assinatura institucional ao final (CTA/WhatsApp), sem alterar o conteúdo anterior.",
        backstory="Padronização acolhedora, linguagem gentil e objetiva, alinhada aos valores do Nexo.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_revisor = Agent(
        role="Revisor Sênior — Conteúdo de Saúde Mental",
        goal="Listar melhorias objetivas (bullets) em clareza, empatia, tom não-estigmatizador, distribuição de links e regras SEO.",
        backstory="Revisor PT-BR especializado em saúde; zela por linguagem inclusiva, não-julgadora e livre de promessas.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_executor = Agent(
        role="Executor de Revisões",
        goal="Aplicar todas as melhorias preservando estrutura semântica e linkagem.",
        backstory="Editor/Dev de HTML limpo.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    # ==== Tarefas ====
    tarefa_intro = Task(
        description=f"""
Escreva a INTRODUÇÃO (2–3 <p>) para '{tema}' usando a palavra-chave '{palavra_chave}' apenas 1 vez.
Tom: acolhedor, empático, profissional — alinhado aos valores do Instituto Nexo (gentileza, autenticidade, cuidado).
Regras:
- PT-BR; parágrafos curtos (2–4 linhas).
- Sem estigmatização, sem julgamentos, sem promessas de cura ou resultado garantido.
- PROIBIDO: <h1> e imagens.
- Sem headings na introdução; só <p>.
- Se houver âncora compatível, inclua 1 link interno natural no 2º parágrafo (anchor descritiva).
Concorrência (inspiração – NÃO copiar):
{dados_concorrencia_txt}
""".strip(),
        expected_output="HTML com 2–3 <p> (sem imagens) e possivelmente 1 link interno natural.",
        agent=agente_intro
    )

    tarefa_outline = Task(
        description=f"""
Crie a ESTRUTURA (apenas headings) para '{tema}':
- 5–7 <h2> numerados com prefixo '1. ', '2. ', '3. ' ...
- Até 2 <h3> por <h2> quando fizer sentido (sem numeração).
- Pelo menos UM heading (<h2> ou <h3>) deve conter a palavra-chave '{palavra_chave}' naturalmente.
- Incluir um H2 de "Mitos e equívocos comuns" (redução de estigma) e um H2 de "Como funciona na prática / o que esperar".
- Incluir H2 sobre quando buscar ajuda profissional, sinais de alerta ou indicações.
- Títulos específicos, claros e não genéricos; foco na jornada do paciente/família e SEO local.
- Nunca usar <h1>. Não incluir conteúdo; só <h2>/<h3>.
Baseie a cobertura na intenção de busca e em lacunas/oportunidades dos concorrentes:
{dados_concorrencia_txt}
""".strip(),
        expected_output="Lista hierárquica com <h2> numerados e <h3> opcionais (sem conteúdo).",
        agent=agente_outline
    )

    tarefa_desenvolvimento = Task(
        description=f"""
Desenvolva o CORPO a partir dos H2/H3 definidos, mantendo a numeração dos H2:
- Mínimo de 1200 palavras no post completo (será validado no unificador).
- <p> curtos (2–4 linhas); usar <ul><li> quando listar.
- Cobrir: o que é, como funciona, indicações, processo terapêutico, expectativas realistas, evidências científicas, dicas práticas para famílias e pacientes.
- Variar semântica de '{palavra_chave}' sem stuffing.
- Zero promessas de cura; preferir "pode ajudar", "contribui para", "é indicado para".
- PROIBIDO inserir imagens.
- Não inventar novos headings; usar apenas os fornecidos.
- Quando fizer sentido, inclua links internos naturais no corpo (anchors descritivas).
Concorrência (inspiração – NÃO copiar):
{dados_concorrencia_txt}
""".strip(),
        expected_output="HTML com <h2> numerados, <h3> opcionais, <p> e <ul><li> (sem imagens).",
        agent=agente_desenvolvimento
    )

    tarefa_conclusao = Task(
        description="""
Escreva a CONCLUSÃO:
- 1–2 <p> resumindo aprendizados, reforçando a importância do acompanhamento profissional e encorajando o leitor a dar o próximo passo.
- Tom gentil e encorajador; sem CTA (o CTA fica na assinatura).
- Inclua 1 link interno natural se ainda não houver link na conclusão.
- Não inserir imagens.
""".strip(),
        expected_output="Conclusão em <p>, possivelmente com 1 link interno.",
        agent=agente_conclusao
    )

    tarefa_unificar = Task(
        description="""
Una introdução, corpo e conclusão em um único HTML (conteúdo do body, sem <body>).
Regras:
- Garantir coerência, zero repetição e manter a NUMERAÇÃO dos <h2> (1., 2., 3., ...).
- Mínimo 1200 palavras no total.
- Usar apenas: <h2>, <h3>, <p>, <ul>, <li>, <a>, <strong>, <em>.
- PROIBIDO: <h1>, <html>, <head>, <title>, meta, estilos inline, QUALQUER tag de imagem.
Saída: somente o conteúdo do body.
""".strip(),
        expected_output="HTML WordPress-ready (apenas conteúdo do body, sem imagens).",
        agent=agente_unificador
    )

    links_internos_txt = "\n".join(
        f"- {li['titulo']}: {li['url']} | âncora sugerida: {li['anchor_sugerida']}"
        for li in links_internos
    )
    links_externos_txt = "\n".join(
        f"- {le['titulo']}: {le['url']} | âncora sugerida: {le['anchor_sugerida']}"
        for le in links_externos
    ) or "(nenhum externo autorizado encontrado)"

    tarefa_linkagem = Task(
        description=f"""
Insira LINKAGEM no HTML unificado (intro/corpo/conclusão) seguindo as regras.

Links internos disponíveis (use pelo menos 3, distribuídos):
{links_internos_txt}

Links externos candidatos (use >=1, se listado; com target="_blank" rel="noopener noreferrer"):
{links_externos_txt}

Regras:
- Distribuição sugerida: 1 link interno na intro, 1–2 no corpo, 1 na conclusão (se aplicável).
- Âncoras naturais e descritivas; nunca usar "clique aqui".
- Não linkar em headings; apenas <p> e <li>.
- Não quebrar HTML semântico; sem inline style.
- Não adicionar imagens.
Saída: HTML com linkagem aplicada.
""".strip(),
        expected_output="HTML com links internos/externos aplicados (sem imagens).",
        agent=agente_linkagem
    )

    tarefa_assinatura = Task(
        description=f"""
Anexe ao FINAL do HTML a assinatura institucional do Instituto Nexo (sem alterar o conteúdo anterior):

<p><strong>Quer saber mais ou agendar uma avaliação? Entre em contato com o Instituto Nexo.</strong></p>
<p><a href="{WHATSAPP_NEXO}" target="_blank" rel="noopener noreferrer">Fale conosco pelo WhatsApp</a></p>
<p><strong>Instituto Nexo — Psicologia Aplicada</strong><br>Unidades em Americana, Campinas, Piracicaba, Sumaré e Limeira — SP.<br>Contato: (19) 3406-5984 | contato@vivanexo.com.br</p>
""".strip(),
        expected_output="HTML final com assinatura adicionada.",
        agent=agente_assinatura
    )

    tarefa_revisar = Task(
        description=f"""
Revise o HTML final quanto a:
- Ortografia/gramática PT-BR; clareza; tom Nexo (acolhedor, empático, profissional, sem estigma).
- Estilo: H2 numerados, parágrafos curtos, listas quando úteis, distribuição de links.
- Linguagem inclusiva e não-julgadora; ausência de promessas de resultado garantido.
- Coerência e distribuição de links; âncoras descritivas; ausência de overstuffing de '{palavra_chave}'.
- Respeito às proibições de imagens e de <h1>.
Saída: lista de melhorias acionáveis em bullets JSON-like:
- {{"campo":"trecho/resumo","problema":"...","acao":"..."}}
""".strip(),
        expected_output="Bullets com melhorias acionáveis.",
        agent=agente_revisor
    )

    tarefa_corrigir = Task(
        description="""
Aplique TODAS as melhorias propostas, preservando:
- Estrutura semântica (<h2> numerados/<h3>/<p>/<ul><li>/<a>).
- Linkagem já aplicada (ajuste âncora só se necessário).
- Ausência de imagens e de <h1>.
Saída: HTML final (somente conteúdo do body).
""".strip(),
        expected_output="HTML final revisado (body only, sem imagens).",
        agent=agente_executor
    )

    # ==== Crew ====
    crew_nexo = Crew(
        agents=[
            agente_intro, agente_outline, agente_desenvolvimento, agente_conclusao,
            agente_unificador, agente_linkagem, agente_assinatura,
            agente_revisor, agente_executor
        ],
        tasks=[
            tarefa_intro, tarefa_outline, tarefa_desenvolvimento, tarefa_conclusao,
            tarefa_unificar, tarefa_linkagem, tarefa_assinatura,
            tarefa_revisar, tarefa_corrigir
        ],
        verbose=True
    )
    return crew_nexo

# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from crewai import Crew, Agent, Task, LLM

load_dotenv()

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "ITC Vertebral Jundiaí (Dra. Sílvia Canevari)",
    "especialidade": "Fisioterapia Especializada em Coluna Vertebral",
    "credenciais":   "CREFITO 8801-F",
    "cidade":        "Jundiaí",
    "estado":        "SP",
    "bairro":        "Jardim Brasil",
    "servicos":      [
        "tratamento não cirúrgico de hérnia de disco e dor ciática",
        "reabilitação de artrose, dor lombar e dor cervical",
        "programa de reconstrução músculo-articular (RMA da coluna)",
        "quiroprática e osteopatia",
    ],
    "publico":       "pessoas com dores, lesões ou patologias na coluna que buscam tratamentos eficazes e não invasivos",
    "diferencial":   "método exclusivo RMA (Reconstrução Músculo Articular), tecnologia avançada (mesas de tração eletrônicas) e direção da Dra. Sílvia Canevari",
    "segmento":      "saúde",
    "assinatura":    "ITC Vertebral Jundiaí — Fisioterapia Especializada na Coluna em Jundiaí/SP | CREFITO 8801-F",
}
_localidade = (CLIENTE["bairro"] + ", " if CLIENTE["bairro"] else "") + CLIENTE["cidade"] + "/" + CLIENTE["estado"]
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
llm_thinking = LLM(model="gemini/gemini-2.5-flash", temperature=0.4)
llm_no_think = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})
llm_fast     = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})

# -------------------------------
# Catálogo fixo de links internos (ITC Vertebral Jundiaí)
# -------------------------------
LINKS_INTERNOS_ITCVERTEBRAL = [
    {"titulo": "Home — ITC Vertebral Jundiaí", "url": "https://www.itcvertebraljundiai.com.br/viva-sem-dor/",
     "anchor_sugerida": "fisioterapia especializada em coluna em Jundiaí"},
    {"titulo": "Sobre Nós", "url": "https://www.itcvertebraljundiai.com.br/sobre-nos/",
     "anchor_sugerida": "conheça a equipe do ITC Vertebral Jundiaí"},
    {"titulo": "Nossos Tratamentos", "url": "https://www.itcvertebraljundiai.com.br/nossos-tratamentos/",
     "anchor_sugerida": "tratamentos especializados para coluna vertebral"},
    {"titulo": "Blog", "url": "https://www.itcvertebraljundiai.com.br/blog/",
     "anchor_sugerida": "artigos sobre saúde da coluna e fisioterapia"},
    {"titulo": "Contato", "url": "https://www.itcvertebraljundiai.com.br/contato/",
     "anchor_sugerida": "agende sua avaliação no ITC Vertebral Jundiaí"},
]

WHATSAPP_ITCVERTEBRAL = "https://wa.link/f1zyei"

# -------------------------------
# SERP helper + whitelist para externos (fisioterapia / coluna)
# -------------------------------
WHITELIST_EXTERNOS = [
    ".gov", ".gov.br", ".edu", ".edu.br",
    "saude.gov.br", "who.int", "nih.gov",
    "coffito.gov.br", "crefito.org.br",
    "developers.google.com", "schema.org", "w3.org",
    "moz.com", "ahrefs.com", "semrush.com",
]

def _usa_whitelist(url: str) -> bool:
    return any(dom in (url or "").lower() for dom in WHITELIST_EXTERNOS)

def buscar_concorrentes_serpapi_struct(palavra_chave: str) -> list[dict]:
    search = GoogleSearch({"q": palavra_chave, "hl": "pt-br", "gl": "br", "num": 10,
                           "api_key": os.getenv("SERPAPI_API_KEY")})
    return search.get_dict().get("organic_results", []) or []

def selecionar_links_externos_autoritativos(resultados_serp: list[dict], max_links: int = 2) -> list[dict]:
    candidatos, vistos = [], set()
    for r in resultados_serp:
        url = r.get("link") or r.get("url") or ""
        titulo = (r.get("title") or "").strip()
        if not url or url in vistos:
            continue
        if _usa_whitelist(url):
            candidatos.append({"titulo": titulo[:90] or "Fonte externa", "url": url,
                                "anchor_sugerida": titulo[:70].lower() or "fonte oficial"})
            vistos.add(url)
        if len(candidatos) >= max_links:
            break
    return candidatos

def buscar_concorrentes_serpapi_texto(palavra_chave: str) -> str:
    results = buscar_concorrentes_serpapi_struct(palavra_chave)
    return "\n".join(f"Título: {r.get('title','')}\nTrecho: {r.get('snippet','')}\nURL: {r.get('link','')}\n"
                     for r in results)

# -------------------------------
# Função principal — ITC Vertebral Jundiaí (dra_silvia)
# -------------------------------
from crews._common import sanitizar_links as _sanitizar_base


def sanitizar_links(html: str) -> str:
    return _sanitizar_base(html, LINKS_INTERNOS_ITCVERTEBRAL, WHITELIST_EXTERNOS)


def build_crew_drasilvia(tema: str, palavra_chave: str):
    """
    Gera conteúdo HTML body-only para WordPress no tom do ITC Vertebral Jundiaí:
    profissional, acolhedor e baseado em evidências — fisioterapia especializada
    em coluna vertebral, com foco em alternativas não-cirúrgicas.
    """
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_ITCVERTEBRAL[:]
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    agente_intro = Agent(
        role="Redator de Introdução — Fisioterapia e Saúde da Coluna",
        goal="Escrever introdução empática e profissional (2–3 parágrafos), citando a palavra-chave 1x, com foco em alívio da dor e alternativas seguras à cirurgia.",
        backstory="Comunicador em saúde que transmite esperança realista a pacientes com dor crônica na coluna.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) — Coluna Vertebral",
        goal="Definir 5–7 H2 numerados com H3 opcionais; contemplar causas, sintomas, quando buscar tratamento, como funciona a fisioterapia e expectativas realistas.",
        backstory="Especialista em outline SEO para clínicas de reabilitação; foca na dúvida do paciente que quer evitar cirurgia.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )
    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento — Fisioterapia Vertebral",
        goal="Preencher cada seção com <p> curtos e listas; cobrir causas, diagnóstico, protocolo de tratamento, exercícios, cuidados e quando buscar avaliação profissional.",
        backstory="Conteúdo baseado em evidências; ~90% de resultados positivos quando bem indicado; sem promessas de cura.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_conclusao = Agent(
        role="Redator de Conclusão — Fisioterapia",
        goal="Encerrar com síntese encorajadora e próximos passos (avaliação clínica, sinais de alerta), sem CTA comercial.",
        backstory="Foco em empoderamento do paciente e redução do medo da dor crônica.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (body only), coerente, com numeração dos H2 e sem imagens.",
        backstory="Editor técnico focado em semântica e limpeza.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_linkagem = Agent(
        role="Planejador de Linkagem — ITC Vertebral",
        goal="Inserir links internos/externos de forma natural, distribuída e compatível com EEAT em saúde.",
        backstory="Especialista em internal linking para clínicas de reabilitação; prioriza COFFITO, gov.br e pesquisas científicas.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_assinatura = Agent(
        role="Responsável por Assinatura — ITC Vertebral Jundiaí",
        goal="Anexar assinatura institucional ao final, sem alterar o conteúdo anterior.",
        backstory="Padronização profissional e acolhedora.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_revisor = Agent(
        role="Revisor Sênior — Conteúdo de Fisioterapia",
        goal="Listar melhorias em clareza, tom empático, distribuição de links, ausência de promessas e regras SEO.",
        backstory="Revisor PT-BR especializado em saúde; sem linguagem alarmista ou promessas de cura.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )
    agente_executor = Agent(
        role="Executor de Revisões",
        goal="Aplicar todas as melhorias preservando estrutura semântica e linkagem.",
        backstory="Editor/Dev de HTML limpo.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )

    tarefa_intro = Task(
        description=f"""
Escreva a INTRODUÇÃO (2–3 <p>) para '{tema}' usando a palavra-chave '{palavra_chave}' apenas 1 vez.
Tom: empático e profissional — paciente com dor na coluna buscando alternativas à cirurgia.
Regras: PT-BR; sem alarmismo; sem promessas; PROIBIDO <h1> e imagens; só <p>.
Se houver âncora compatível, inclua 1 link interno natural no 2º parágrafo.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com 2–3 <p> e possivelmente 1 link interno.",
        agent=agente_intro
    )
    tarefa_outline = Task(
        description=f"""
Crie a ESTRUTURA para '{tema}': 5–7 <h2> numerados, até 2 <h3> por seção.
Inclua H2 sobre "Quando buscar tratamento / sinais de alerta", H2 "Mitos sobre cirurgia de coluna" e H2 "Como funciona o protocolo de fisioterapia".
Pelo menos 1 heading com '{palavra_chave}'. Nunca <h1>. Só headings.
- Alinhar os H2 com a intenção de busca: responder diretamente o que o usuário quer saber sobre o tema.
- Trabalhar entidades semânticas: incluir nos headings termos correlatos, sinônimos e subtemas que reforcem a autoridade temática.

Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="Lista hierárquica com <h2> numerados.",
        agent=agente_outline
    )
    tarefa_desenvolvimento = Task(
        description=f"""
Desenvolva o CORPO (mín. 1200 palavras): <p> curtos, <ul><li> quando listar.
Cubra: causas, sintomas, diagnóstico clínico, protocolo de fisioterapia, exercícios indicados, cuidados do dia a dia, quando a cirurgia é realmente necessária.
Variar semântica de '{palavra_chave}' sem stuffing. Zero imagens. Zero CTA.
Diretrizes de qualidade obrigatórias:
- SEO local: inserir de forma natural "{_localidade}" no corpo do texto (mínimo 2 menções). Evitar repetição artificial.
- Conexão com serviço: conectar o tema aos serviços reais do cliente — {_servicos_resumo}.
- Profundidade: incluir causas, sinais, critérios de avaliação, exemplos práticos e orientações concretas. Evitar generalidades vagas.
- Semântica/entidades: usar variações e termos correlatos à keyword (sinônimos, subtemas, entidades do domínio).
- Linguagem ética: evitar tom de diagnóstico, promessa de resultado ou urgência. Usar "pode estar associado", "a avaliação profissional é recomendada".

Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com <h2> numerados, <h3>, <p> e <ul><li>.",
        agent=agente_desenvolvimento
    )
    tarefa_conclusao = Task(
        description="Escreva CONCLUSÃO (1–2 <p>): aprendizados e próximos passos (ex.: agendar avaliação clínica). Zero CTA. 1 link interno natural se possível. Sem imagens.",
        expected_output="Conclusão em <p> com possível link interno.",
        agent=agente_conclusao
    )
    tarefa_unificar = Task(
        description="Una tudo em HTML único (body only). Mín. 1200 palavras. Tags: <h2>,<h3>,<p>,<ul>,<li>,<a>,<strong>,<em>. PROIBIDO: <h1>,<html>,<head>,meta,estilos inline,imagens.",
        expected_output="HTML WordPress-ready (body only).",
        agent=agente_unificador
    )

    links_internos_txt = "\n".join(f"- {li['titulo']}: {li['url']} | âncora: {li['anchor_sugerida']}" for li in links_internos)
    links_externos_txt = "\n".join(f"- {le['titulo']}: {le['url']} | âncora: {le['anchor_sugerida']}" for le in links_externos) or "(nenhum externo autorizado encontrado)"

    tarefa_linkagem = Task(
        description=f"""
Insira LINKAGEM no HTML unificado.
Links internos (use >=3):\n{links_internos_txt}
Links externos (use >=1, se listado; target="_blank" rel="noopener noreferrer"):\n{links_externos_txt}
Regras: âncoras descritivas; não linkar em headings; sem inline style; sem imagens.""".strip(),
        expected_output="HTML com links aplicados.",
        agent=agente_linkagem
    )
    tarefa_assinatura = Task(
        description=f"""
Anexe ao FINAL do HTML a assinatura do ITC Vertebral Jundiaí:
<p><strong>Quer viver sem dor? Agende sua avaliação clínica no ITC Vertebral Jundiaí.</strong></p>
<p><a href="{WHATSAPP_ITCVERTEBRAL}" target="_blank" rel="noopener noreferrer">Fale conosco pelo WhatsApp</a></p>
<p><strong>ITC Vertebral Jundiaí</strong><br>R. São Lázaro, 197 – Jardim Brasil – Jundiaí – SP<br>(11) 93214-2995 | jundiai@itcvertebral.com.br</p>""".strip(),
        expected_output="HTML final com assinatura.",
        agent=agente_assinatura
    )
    tarefa_revisar = Task(
        description=f"""
Revise: ortografia PT-BR, tom empático e não-alarmista, H2 numerados, distribuição de links, ausência de promessas e de imagens/<h1>.
Checklist de qualidade obrigatório — verificar TODOS os itens antes de finalizar:
- CTA ético: evitar "agende agora", "não adie", "invista na sua saúde", "transformação". Preferir linguagem educativa e neutra.
- Assinatura: está personalizada e profissional (com CRM/CREFITO/OAB quando aplicável)?
- Linguagem ética: ausência de promessas de resultado, tom de diagnóstico ou urgência. Usar "pode estar associado", "a avaliação profissional é recomendada", "a conduta depende do caso".
- SEO local: cidade/bairro/região do cliente aparecem de forma natural no corpo (mínimo 2 ocorrências)?
- Conexão com serviço: o artigo conecta o tema ao serviço/especialidade real do cliente?
- Profundidade: há causas, sinais, critérios de avaliação, exemplos práticos e orientações concretas?
- Intenção de busca: os H2s respondem ao que o usuário busca? Alinhamento com a palavra-chave e entidades do tema?
- Links internos: levam a páginas reais e relevantes? Âncoras descritivas (nunca "clique aqui")?

Saída: bullets JSON-like: {{"campo":"...","problema":"...","acao":"..."}}""".strip(),
        expected_output="Bullets com melhorias acionáveis.",
        agent=agente_revisor
    )
    tarefa_corrigir = Task(
        description="Aplique TODAS as melhorias. Preserve estrutura semântica, linkagem, ausência de imagens e <h1>. Saída: HTML final (body only).",
        expected_output="HTML final revisado (body only).",
        agent=agente_executor
    )

    return Crew(
        agents=[agente_intro, agente_outline, agente_desenvolvimento, agente_conclusao,
                agente_unificador, agente_linkagem, agente_assinatura, agente_revisor, agente_executor],
        tasks=[tarefa_intro, tarefa_outline, tarefa_desenvolvimento, tarefa_conclusao,
               tarefa_unificar, tarefa_linkagem, tarefa_assinatura, tarefa_revisar, tarefa_corrigir],
        verbose=True
    )
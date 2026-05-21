# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from crewai import Crew, Agent, Task, LLM

load_dotenv()
llm_thinking = LLM(model="gemini/gemini-2.5-flash", temperature=0.4)
llm_no_think = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})
llm_fast     = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})

# -------------------------------
# Catálogo fixo de links internos (Dr. Daniel Rebolledo)
# -------------------------------
LINKS_INTERNOS_DRDANIEL = [
    {"titulo": "Home — Dr. Daniel Rebolledo", "url": "https://www.danielrebolledo.com.br/",
     "anchor_sugerida": "Dr. Daniel Rebolledo — cirurgião de quadril e oncologia ortopédica"},
    {"titulo": "Perfil do Médico", "url": "https://www.danielrebolledo.com.br/perfil/",
     "anchor_sugerida": "conheça o perfil e a experiência do Dr. Daniel Rebolledo"},
    {"titulo": "Consultórios", "url": "https://www.danielrebolledo.com.br/clinicas/",
     "anchor_sugerida": "locais de atendimento em São Paulo e Santo André"},
    {"titulo": "Blog", "url": "https://www.danielrebolledo.com.br/blog/",
     "anchor_sugerida": "artigos sobre quadril e oncologia ortopédica"},
    {"titulo": "Patologias do Quadril", "url": "https://www.danielrebolledo.com.br/quadril/patologias/",
     "anchor_sugerida": "principais patologias do quadril"},
    {"titulo": "Artrose de Quadril", "url": "https://www.danielrebolledo.com.br/quadril/patologias/atrose-quadril/",
     "anchor_sugerida": "artrose de quadril: causas e tratamentos"},
    {"titulo": "Artroplastia do Quadril", "url": "https://www.danielrebolledo.com.br/quadril/tratamentos/artroplastia-do-quadril-proteses/",
     "anchor_sugerida": "artroplastia do quadril e próteses"},
    {"titulo": "Artroscopia de Quadril", "url": "https://www.danielrebolledo.com.br/quadril/tratamentos/artroscopia-de-quadril/",
     "anchor_sugerida": "artroscopia de quadril minimamente invasiva"},
    {"titulo": "Viscossuplementação", "url": "https://www.danielrebolledo.com.br/quadril/tratamentos/viscossuplementacao-acido-hialuronico/",
     "anchor_sugerida": "viscossuplementação com ácido hialurônico no quadril"},
    {"titulo": "Oncologia Ortopédica", "url": "https://www.danielrebolledo.com.br/oncologia-ortopedica/",
     "anchor_sugerida": "oncologia ortopédica: tumores ósseos e de partes moles"},
    {"titulo": "Tumores Benignos", "url": "https://www.danielrebolledo.com.br/oncologia-ortopedica/tumores-benignos/",
     "anchor_sugerida": "tumores ósseos benignos: diagnóstico e tratamento"},
    {"titulo": "Metástases Ósseas", "url": "https://www.danielrebolledo.com.br/oncologia-ortopedica/tumores-malignos/metastases-osseas/",
     "anchor_sugerida": "tratamento de metástases ósseas"},
]

WHATSAPP_DRDANIEL = "https://api.whatsapp.com/send/?phone=5511933870542&text=Oi!%20Encontrei%20o%20Dr.%20Daniel%20Rebolledo%20no%20Google%20e%20gostaria%20de%20mais%20informações.&type=phone_number&app_absent=0"

# -------------------------------
# SERP helper + whitelist (ortopedia / oncologia ortopédica)
# -------------------------------
WHITELIST_EXTERNOS = [
    ".gov", ".gov.br", ".edu", ".edu.br",
    "saude.gov.br", "who.int", "nih.gov",
    "inca.gov.br", "oncoguia.org.br",
    "sbot.org.br", "sbco.org.br",
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
# Função principal — Dr. Daniel Rebolledo
# -------------------------------
def build_crew_drdaniel(tema: str, palavra_chave: str):
    """
    Gera conteúdo HTML body-only para WordPress no tom do Dr. Daniel Rebolledo:
    altamente técnico e humanizado — especialista em cirurgia de quadril e
    oncologia ortopédica com atuação em hospitais de referência (Sírio-Libanês,
    Albert Einstein, Oswaldo Cruz, Santa Catarina).
    """
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_DRDANIEL[:]
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    agente_intro = Agent(
        role="Redator de Introdução — Cirurgia de Quadril e Oncologia Ortopédica",
        goal="Escrever introdução técnica e humanizada (2–3 parágrafos), citando a palavra-chave 1x, transmitindo autoridade médica e cuidado ao paciente.",
        backstory="Profissional de conteúdo médico especializado em ortopedia; equilibra tecnicidade e acolhimento.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) — Ortopedia e Oncologia",
        goal="Definir 5–7 H2 numerados com H3 opcionais; contemplar anatomia, causas, diagnóstico, opções de tratamento, cirurgia e recuperação.",
        backstory="Especialista em outline SEO para cirurgiões ortopédicos; foca na jornada do paciente do diagnóstico ao pós-operatório.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )
    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento — Ortopedia e Oncologia Ortopédica",
        goal="Preencher cada seção com <p> curtos e listas; cobrir: anatomia, causas, diagnóstico clínico/imagem, opções conservadoras, indicação cirúrgica, técnicas, recuperação e prognóstico.",
        backstory="Conteúdo médico de alta precisão, baseado em evidências, sem prometer resultados garantidos.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_conclusao = Agent(
        role="Redator de Conclusão — Ortopedia",
        goal="Encerrar com síntese objetiva, importância do diagnóstico precoce e próximos passos (consulta especializada), sem CTA.",
        backstory="Foco em decisão informada e importância do acompanhamento especializado.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (body only), coerente, com numeração dos H2 e sem imagens.",
        backstory="Editor técnico focado em semântica e limpeza.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_linkagem = Agent(
        role="Planejador de Linkagem — Dr. Daniel Rebolledo",
        goal="Inserir links internos/externos de forma natural, distribuída e compatível com EEAT médico.",
        backstory="Especialista em internal linking para cirurgiões; prioriza INCA, SBOT, gov.br e artigos científicos.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_assinatura = Agent(
        role="Responsável por Assinatura — Dr. Daniel Rebolledo",
        goal="Anexar assinatura institucional ao final, sem alterar o conteúdo anterior.",
        backstory="Padronização profissional e humanizada.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_revisor = Agent(
        role="Revisor Sênior — Conteúdo Médico-Cirúrgico",
        goal="Listar melhorias em precisão técnica, tom humanizado, distribuição de links e regras SEO.",
        backstory="Revisor PT-BR especializado em ortopedia; sem promessas e sem linguagem alarmista.",
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
Tom: técnico e humanizado — Dr. Daniel Rebolledo, desde 2006, hospitais de referência (Sírio-Libanês, Einstein).
Regras: PT-BR; sem promessas; PROIBIDO <h1> e imagens; só <p>.
Se houver âncora compatível, inclua 1 link interno natural no 2º parágrafo.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com 2–3 <p> e possivelmente 1 link interno.",
        agent=agente_intro
    )
    tarefa_outline = Task(
        description=f"""
Crie a ESTRUTURA para '{tema}': 5–7 <h2> numerados, até 2 <h3> por seção.
Inclua H2 sobre "Diagnóstico: como é feito", H2 "Opções de tratamento: conservador vs cirúrgico" e H2 "Recuperação e prognóstico".
Pelo menos 1 heading com '{palavra_chave}'. Nunca <h1>. Só headings.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="Lista hierárquica com <h2> numerados.",
        agent=agente_outline
    )
    tarefa_desenvolvimento = Task(
        description=f"""
Desenvolva o CORPO (mín. 1200 palavras): <p> curtos, <ul><li> quando listar.
Cubra: anatomia relevante, causas/fatores de risco, sintomas, diagnóstico (clínico + imagem), tratamento conservador, indicação cirúrgica, técnicas disponíveis, recuperação e quando procurar especialista.
Variar semântica de '{palavra_chave}' sem stuffing. Zero imagens. Zero CTA.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com <h2> numerados, <h3>, <p> e <ul><li>.",
        agent=agente_desenvolvimento
    )
    tarefa_conclusao = Task(
        description="Escreva CONCLUSÃO (1–2 <p>): importância do diagnóstico precoce e acompanhamento especializado. Zero CTA. 1 link interno natural se possível. Sem imagens.",
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
Anexe ao FINAL do HTML a assinatura do Dr. Daniel Rebolledo:
<p><strong>Precisa de uma avaliação especializada? Fale com o Dr. Daniel Rebolledo.</strong></p>
<p><a href="{WHATSAPP_DRDANIEL}" target="_blank" rel="noopener noreferrer">Entre em contato pelo WhatsApp</a></p>
<p><strong>Dr. Daniel Rebolledo</strong> — Cirurgia de Quadril e Oncologia Ortopédica<br>São Paulo: Rua Haddock Lobo, 131, cj 1509 – Cerqueira César | (11) 3151-2825<br>Santo André: Rua das Paineiras, 161 – Jardim | (11) 2677-5711</p>""".strip(),
        expected_output="HTML final com assinatura.",
        agent=agente_assinatura
    )
    tarefa_revisar = Task(
        description=f"""
Revise: ortografia PT-BR, precisão técnica, tom humanizado, H2 numerados, distribuição de links, ausência de promessas e de imagens/<h1>.
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
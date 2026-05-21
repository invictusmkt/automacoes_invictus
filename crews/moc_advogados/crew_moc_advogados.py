# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from crewai import Crew, Agent, Task, LLM

load_dotenv()
llm_thinking = LLM(model="gemini/gemini-2.5-flash", temperature=0.4)
llm_no_think = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})
llm_fast     = LLM(model="gemini/gemini-2.0-flash", temperature=0.4)

# -------------------------------
# Catálogo fixo de links internos (MOC Advogados)
# -------------------------------
LINKS_INTERNOS_MOC = [
    {"titulo": "Home — MOC Advogados", "url": "https://mocadvogados.com.br/moc-2/",
     "anchor_sugerida": "escritório de advocacia MOC Advogados"},
    {"titulo": "Sobre Nós", "url": "https://mocadvogados.com.br/sobre-nos/",
     "anchor_sugerida": "conheça a equipe e o método MOC"},
    {"titulo": "Para Empresas", "url": "https://mocadvogados.com.br/para-empresas/",
     "anchor_sugerida": "soluções jurídicas para empresas"},
    {"titulo": "Para Você", "url": "https://mocadvogados.com.br/para-voce/",
     "anchor_sugerida": "assessoria jurídica para pessoas físicas"},
    {"titulo": "Direito Tributário", "url": "https://mocadvogados.com.br/direito-tributario/",
     "anchor_sugerida": "consultoria em direito tributário"},
    {"titulo": "Direito Trabalhista e Bancário", "url": "https://mocadvogados.com.br/trabalhista-bancario/",
     "anchor_sugerida": "assessoria trabalhista e bancária"},
    {"titulo": "Direito Previdenciário", "url": "https://mocadvogados.com.br/direito-previdenciario/",
     "anchor_sugerida": "planejamento e direito previdenciário"},
    {"titulo": "Direito Civil", "url": "https://mocadvogados.com.br/civel-contencioso-e-consultivo/",
     "anchor_sugerida": "direito civil contencioso e consultivo"},
    {"titulo": "Planos de Saúde", "url": "https://mocadvogados.com.br/bariatrica/",
     "anchor_sugerida": "direitos em planos de saúde"},
]

WHATSAPP_MOC = "https://api.whatsapp.com/send/?phone=5517996611109&text=Oi!%20Encontrei%20a%20MOC%20Advogados%20no%20Google%20e%20gostaria%20de%20mais%20informações.&type=phone_number&app_absent=0"

# -------------------------------
# SERP helper + whitelist (direito / legislação)
# -------------------------------
WHITELIST_EXTERNOS = [
    ".gov", ".gov.br", ".edu", ".edu.br",
    "planalto.gov.br", "stj.jus.br", "stf.jus.br", "tst.jus.br", "trf.jus.br",
    "oab.org.br", "cfp.org.br",
    "receita.fazenda.gov.br", "previdencia.gov.br",
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
# Função principal — MOC Advogados
# -------------------------------
def build_crew_mocadvogados(tema: str, palavra_chave: str):
    """
    Gera conteúdo HTML body-only para WordPress no tom da MOC Advogados:
    estratégico, humanizado e técnico — "Think like business. Feel like people.
    Act with technique." Atua em direito tributário, trabalhista, previdenciário,
    civil e planos de saúde. Escritórios em Rio Preto, Marília e Santos.
    """
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_MOC[:]
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    agente_intro = Agent(
        role="Redator de Introdução — Advocacia Estratégica",
        goal="Escrever introdução profissional e acessível (2–3 parágrafos), citando a palavra-chave 1x, no tom MOC: técnico, humano e estratégico.",
        backstory="Comunicador jurídico que traduz o direito em linguagem clara para empresas e pessoas físicas.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) — Direito",
        goal="Definir 5–7 H2 numerados com H3 opcionais; contemplar: o que é, legislação aplicável, direitos e deveres, como agir, erros comuns e quando contratar um advogado.",
        backstory="Especialista em outline SEO para escritórios de advocacia; foca na dúvida prática do cliente.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )
    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento — Conteúdo Jurídico",
        goal="Preencher cada seção com <p> curtos e listas; cobrir: conceito legal, base normativa, direitos e deveres, como funciona na prática, erros comuns e dicas preventivas.",
        backstory="Conteúdo jurídico acessível e preciso; sem dar consultoria individualizada; sempre recomendar advogado.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_conclusao = Agent(
        role="Redator de Conclusão — Advocacia",
        goal="Encerrar com síntese objetiva e importância de contar com assessoria jurídica especializada, sem CTA comercial.",
        backstory="Foco em prevenção de riscos e decisão informada.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (body only), coerente, com numeração dos H2 e sem imagens.",
        backstory="Editor técnico focado em semântica e limpeza.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_linkagem = Agent(
        role="Planejador de Linkagem — MOC Advogados",
        goal="Inserir links internos/externos de forma natural, distribuída; priorizar fontes legislativas e jurisprudência.",
        backstory="Especialista em internal linking para escritórios; prioriza Planalto, STJ, TST e OAB.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_assinatura = Agent(
        role="Responsável por Assinatura — MOC Advogados",
        goal="Anexar assinatura institucional ao final, sem alterar o conteúdo anterior.",
        backstory="Padronização profissional alinhada ao método MOC.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_revisor = Agent(
        role="Revisor Sênior — Conteúdo Jurídico",
        goal="Listar melhorias em clareza, precisão legal, tom estratégico e humanizado, distribuição de links e SEO.",
        backstory="Revisor PT-BR; sem afirmações absolutas sobre resultados jurídicos; sempre 'pode' ou 'em regra'.",
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
Tom: MOC Advogados — "Think like business. Feel like people. Act with technique." Profissional, claro e acessível.
Regras: PT-BR; sem afirmações absolutas de resultado; PROIBIDO <h1> e imagens; só <p>.
Se houver âncora compatível, inclua 1 link interno natural no 2º parágrafo.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com 2–3 <p> e possivelmente 1 link interno.",
        agent=agente_intro
    )
    tarefa_outline = Task(
        description=f"""
Crie a ESTRUTURA para '{tema}': 5–7 <h2> numerados, até 2 <h3> por seção.
Inclua H2 de "Erros comuns e armadilhas jurídicas", H2 "O que diz a legislação" e H2 "Quando contratar um advogado".
Pelo menos 1 heading com '{palavra_chave}'. Nunca <h1>. Só headings.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="Lista hierárquica com <h2> numerados.",
        agent=agente_outline
    )
    tarefa_desenvolvimento = Task(
        description=f"""
Desenvolva o CORPO (mín. 1200 palavras): <p> curtos, <ul><li> quando listar.
Cubra: conceito legal, base normativa (cite leis e artigos quando relevante), direitos, deveres, prazos, como agir na prática e prevenção de riscos.
Variar semântica de '{palavra_chave}' sem stuffing. Zero imagens. Zero CTA. Nunca prometer resultado.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com <h2> numerados, <h3>, <p> e <ul><li>.",
        agent=agente_desenvolvimento
    )
    tarefa_conclusao = Task(
        description="Escreva CONCLUSÃO (1–2 <p>): síntese, importância da assessoria jurídica especializada e prevenção. Zero CTA. 1 link interno natural se possível. Sem imagens.",
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
Anexe ao FINAL do HTML a assinatura da MOC Advogados:
<p><strong>Precisa de assessoria jurídica? A MOC Advogados está pronta para ajudar.</strong></p>
<p><a href="{WHATSAPP_MOC}" target="_blank" rel="noopener noreferrer">Fale com um advogado pelo WhatsApp</a></p>
<p><strong>MOC Advogados</strong><br>São José do Rio Preto | Marília | Santos</p>""".strip(),
        expected_output="HTML final com assinatura.",
        agent=agente_assinatura
    )
    tarefa_revisar = Task(
        description=f"""
Revise: ortografia PT-BR, precisão jurídica, tom MOC (técnico e humano), H2 numerados, distribuição de links, ausência de promessas e de imagens/<h1>.
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
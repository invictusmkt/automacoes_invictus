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
# Catálogo fixo de links internos (Clínica Dr. Raimundo Nunes)
# -------------------------------
LINKS_INTERNOS_DRRAIMUNDO = [
    {"titulo": "Home — Clínica Dr. Raimundo Nunes",
     "url": "https://clinicadrraimundonunes.com.br/",
     "anchor_sugerida": "Clínica de Ginecologia e Obstetrícia Dr. Raimundo Nunes em São Paulo"},
    {"titulo": "Quem Somos",
     "url": "https://clinicadrraimundonunes.com.br/quem-somos/",
     "anchor_sugerida": "conheça a história e o compromisso com a saúde da mulher"},
    {"titulo": "Corpo Clínico",
     "url": "https://clinicadrraimundonunes.com.br/corpo-clinico/",
     "anchor_sugerida": "equipe de ginecologistas e obstetras especialistas"},
    {"titulo": "DIU e Implanon — Dúvidas Frequentes",
     "url": "https://clinicadrraimundonunes.com.br/diu-e-implanon/",
     "anchor_sugerida": "perguntas frequentes sobre DIU e Implanon em São Paulo"},
    {"titulo": "DIU Mirena",
     "url": "https://clinicadrraimundonunes.com.br/diu-mirena/",
     "anchor_sugerida": "vantagens, eficácia e indicações do DIU hormonal Mirena"},
    {"titulo": "Pré-natal — Orientações Parte 1",
     "url": "https://clinicadrraimundonunes.com.br/pre-natal-1/",
     "anchor_sugerida": "dúvidas e exames no acompanhamento pré-natal"},
    {"titulo": "Pré-natal — Orientações Parte 2",
     "url": "https://clinicadrraimundonunes.com.br/pre-natal-2/",
     "anchor_sugerida": "orientações médicas sobre as fases do pré-natal"},
    {"titulo": "Gestação — Primeira Fase",
     "url": "https://clinicadrraimundonunes.com.br/gestacao-1/",
     "anchor_sugerida": "mudanças no corpo e desenvolvimento do bebê na gestação"},
    {"titulo": "Parto",
     "url": "https://clinicadrraimundonunes.com.br/parto/",
     "anchor_sugerida": "tipos de parto e plano de parto ideal"},
    {"titulo": "Pós-parto",
     "url": "https://clinicadrraimundonunes.com.br/pos-parto/",
     "anchor_sugerida": "cuidados com a saúde da mulher no pós-parto"},
    {"titulo": "Cirurgia Ginecológica",
     "url": "https://clinicadrraimundonunes.com.br/cirurgia/",
     "anchor_sugerida": "como funciona a cirurgia ginecológica e a laparoscopia"},
    {"titulo": "Publicações e Blog",
     "url": "https://clinicadrraimundonunes.com.br/publicacoes/",
     "anchor_sugerida": "artigos informativos sobre ginecologia e saúde da mulher"},
    {"titulo": "Contato e Agendamento",
     "url": "https://clinicadrraimundonunes.com.br/contato/",
     "anchor_sugerida": "agende sua consulta com a equipe da clínica"},
]

WHATSAPP_DRRAIMUNDO = "https://wa.me/5511973071245?text=Gostaria%20de%20tirar%20uma%20dúvida%20e%20marcar%20uma%20consulta"

# -------------------------------
# SERP helper + whitelist (ginecologia / obstetrícia / saúde feminina)
# -------------------------------
WHITELIST_EXTERNOS = [
    ".gov", ".gov.br", ".edu", ".edu.br",
    "saude.gov.br", "anvisa.gov.br", "who.int", "nih.gov",
    "cfm.org.br",         # Conselho Federal de Medicina
    "febrasgo.org.br",    # Federação Brasileira de Ginecologia e Obstetrícia
    "inca.gov.br",        # Instituto Nacional do Câncer
    "sbra.com.br",        # Sociedade Brasileira de Reprodução Assistida
    "endometriose.org.br",
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
# Função principal — Clínica Dr. Raimundo Nunes
# -------------------------------
def build_crew_drraimundo(tema: str, palavra_chave: str):
    """
    Gera conteúdo HTML body-only para WordPress no tom da Clínica Dr. Raimundo Nunes:
    humanizado, acolhedor e técnico-autoritativo — referência nacional em ginecologia
    e obstetrícia com 30+ anos de atuação em São Paulo. Pioneiros no Brasil na
    implantação de DIU hormonal (Mirena/Kyleena) desde 2000.

    Tom: conteúdo estritamente educativo (alinhado ao CFM); nunca prometer resultado;
    enfatizar avaliação individualizada e escuta ativa.
    """
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_DRRAIMUNDO[:]
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    agente_intro = Agent(
        role="Redatora de Introdução — Ginecologia e Saúde da Mulher",
        goal="Escrever introdução humanizada e acolhedora (2–3 parágrafos), citando a palavra-chave 1x, com foco na saúde integral da mulher em todas as fases da vida.",
        backstory="Comunicadora médica especializada em saúde feminina; transmite autoridade clínica com escuta ativa e cuidado personalizado. Conteúdo estritamente educativo (CFM).",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) — Ginecologia e Obstetrícia",
        goal="Definir 5–7 H2 numerados com H3 opcionais; contemplar: o que é, quem se beneficia, como é feito, cuidados, mitos e quando buscar um especialista.",
        backstory="Especialista em outline SEO para clínicas ginecológicas de referência; foca na jornada da paciente do diagnóstico ao acompanhamento.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )
    agente_desenvolvimento = Agent(
        role="Redatora de Desenvolvimento — Saúde Feminina Integral",
        goal="Preencher cada seção com <p> curtos e listas; cobrir: conceito, indicações, como funciona, cuidados, expectativas realistas, mitos e quando consultar um ginecologista.",
        backstory="Conteúdo ginecológico preciso, acolhedor e educativo; alinhado ao CFM — sem prometer resultados, sempre recomendando consulta especializada.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_conclusao = Agent(
        role="Redatora de Conclusão — Saúde da Mulher",
        goal="Encerrar com síntese encorajadora e importância do acompanhamento ginecológico regular, sem CTA comercial.",
        backstory="Foco em empoderamento feminino, prevenção e decisão informada.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (body only), coerente, com numeração dos H2 e sem imagens.",
        backstory="Editor técnico focado em semântica e limpeza.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_linkagem = Agent(
        role="Planejador de Linkagem — Clínica Dr. Raimundo Nunes",
        goal="Inserir links internos/externos de forma natural, distribuída e compatível com EEAT médico.",
        backstory="Especialista em internal linking para clínicas ginecológicas; prioriza FEBRASGO, CFM, INCA e gov.br.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_assinatura = Agent(
        role="Responsável por Assinatura — Clínica Dr. Raimundo Nunes",
        goal="Anexar assinatura institucional ao final, sem alterar o conteúdo anterior.",
        backstory="Padronização humanizada e acolhedora, alinhada aos 30+ anos de tradição da clínica.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_revisor = Agent(
        role="Revisora Sênior — Conteúdo Ginecológico",
        goal="Listar melhorias em clareza, tom acolhedor e ético, distribuição de links, conformidade CFM e SEO.",
        backstory="Revisora PT-BR especializada em saúde feminina; sem promessas; linguagem inclusiva e não-alarmista.",
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
Tom: Clínica Dr. Raimundo Nunes — humanizado, acolhedor e técnico. Referência em ginecologia há 30+ anos em SP.
Conteúdo estritamente educativo (alinhado ao CFM); nunca prometer resultado; sem afirmações absolutas.
Regras: PT-BR; PROIBIDO <h1> e imagens; só <p>.
Se houver âncora compatível, inclua 1 link interno natural no 2º parágrafo.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com 2–3 <p> e possivelmente 1 link interno.",
        agent=agente_intro
    )
    tarefa_outline = Task(
        description=f"""
Crie a ESTRUTURA para '{tema}': 5–7 <h2> numerados, até 2 <h3> por seção.
Inclua H2 de "Mitos e verdades", H2 "Como é feito o procedimento / acompanhamento" e H2 "Quando consultar um ginecologista".
Pelo menos 1 heading com '{palavra_chave}'. Nunca <h1>. Só headings.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="Lista hierárquica com <h2> numerados.",
        agent=agente_outline
    )
    tarefa_desenvolvimento = Task(
        description=f"""
Desenvolva o CORPO (mín. 1200 palavras): <p> curtos, <ul><li> quando listar.
Cubra: conceito, indicações, contraindicações, como funciona na prática, cuidados antes/durante/depois, expectativas realistas, mitos comuns e quando buscar ginecologista.
Usar linguagem empática; nunca prometer resultado; sempre recomendar avaliação individualizada.
Variar semântica de '{palavra_chave}' sem stuffing. Zero imagens. Zero CTA.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com <h2> numerados, <h3>, <p> e <ul><li>.",
        agent=agente_desenvolvimento
    )
    tarefa_conclusao = Task(
        description="Escreva CONCLUSÃO (1–2 <p>): síntese e importância do acompanhamento ginecológico regular para a saúde integral da mulher. Zero CTA. 1 link interno natural se possível. Sem imagens.",
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
Anexe ao FINAL do HTML a assinatura da Clínica Dr. Raimundo Nunes (sem alterar o conteúdo anterior):
<p><strong>Cuide da sua saúde com quem tem mais de 30 anos de experiência em ginecologia e obstetrícia.</strong></p>
<p><a href="{WHATSAPP_DRRAIMUNDO}" target="_blank" rel="noopener noreferrer">Agende sua consulta pelo WhatsApp</a></p>
<p><strong>Clínica Dr. Raimundo Nunes</strong><br>
Unidade Bela Vista: Rua Itapeva, 490 – 5º Andar, Cj. 51 – São Paulo/SP | (11) 3251-1245<br>
Unidade Itaim Bibi: Rua Joaquim Floriano, 940 – Cj. 41 – São Paulo/SP</p>""".strip(),
        expected_output="HTML final com assinatura.",
        agent=agente_assinatura
    )
    tarefa_revisar = Task(
        description=f"""
Revise: ortografia PT-BR, tom humanizado e ético (CFM), H2 numerados, distribuição de links, ausência de promessas e de imagens/<h1>.
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
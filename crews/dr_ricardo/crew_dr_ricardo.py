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
# Catálogo fixo de links internos (Dr. Ricardo Vieira Ferreira — Uroclínica Jaraguá)
# -------------------------------
LINKS_INTERNOS_DRRICARDO = [
    {"titulo": "Home — Dr. Ricardo Vieira Ferreira", "url": "https://drricardoferreira.com.br/",
     "anchor_sugerida": "Dr. Ricardo Vieira Ferreira — urologista em Jaraguá do Sul"},
    {"titulo": "Sobre o Dr. Ricardo", "url": "https://drricardoferreira.com.br/sobre/",
     "anchor_sugerida": "trajetória e formação do Dr. Ricardo Vieira Ferreira"},
    {"titulo": "Contato e Agendamento", "url": "https://drricardoferreira.com.br/contato/",
     "anchor_sugerida": "agende sua consulta particular com o Dr. Ricardo"},
    {"titulo": "Blog — Saúde Hormonal e Qualidade de Vida", "url": "https://drricardoferreira.com.br/blog",
     "anchor_sugerida": "artigos sobre saúde hormonal e envelhecimento saudável"},
    {"titulo": "7 Sinais de Testosterona Baixa em Homens", "url": "https://drricardoferreira.com.br/7-sinais-de-testosterona-baixa-em-homens-quando-procurar-avaliacao-medica/",
     "anchor_sugerida": "os principais sinais de testosterona baixa em homens"},
    {"titulo": "Massa Muscular e Hormônios", "url": "https://drricardoferreira.com.br/massa-muscular-e-hormonios-qual-a-relacao-e-quando-investigar/",
     "anchor_sugerida": "relação entre perda de massa muscular e desequilíbrio hormonal"},
    {"titulo": "Perda de Ereção Frequente — Quando Investigar", "url": "https://drricardoferreira.com.br/perda-de-erecao-frequente-quando-investigar/",
     "anchor_sugerida": "quando investigar clinicamente a perda de ereção frequente"},
]

WHATSAPP_DRRICARDO = "https://api.whatsapp.com/send?phone=5547999556456&text=Olá!%20Vim%20do%20site%20e%20gostaria%20de%20mais%20informações."

# -------------------------------
# SERP helper + whitelist (urologia / saúde hormonal / longevidade)
# -------------------------------
WHITELIST_EXTERNOS = [
    ".gov", ".gov.br", ".edu", ".edu.br",
    "saude.gov.br", "anvisa.gov.br", "who.int", "nih.gov",
    "cfm.org.br",        # Conselho Federal de Medicina
    "sbu.org.br",        # Sociedade Brasileira de Urologia
    "sbem.org.br",       # Sociedade Brasileira de Endocrinologia e Metabologia
    "febrasgo.org.br",   # Federação Brasileira das Associações de Ginecologia e Obstetrícia
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
# Função principal — Dr. Ricardo Vieira Ferreira
# -------------------------------
def build_crew_drricardo(tema: str, palavra_chave: str):
    """
    Gera conteúdo HTML body-only para WordPress no tom do Dr. Ricardo Vieira Ferreira:
    formal, empático e altamente responsável — urologista com 35+ anos de experiência,
    especializado em reposição hormonal masculina e feminina, implantes hormonais e
    envelhecimento saudável. Atendimento particular em Jaraguá do Sul – SC.

    Tom: nunca prometer resultados; sempre enfatizar avaliação médica criteriosa,
    exames laboratoriais e conduta individualizada.
    """
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_DRRICARDO[:]
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    agente_intro = Agent(
        role="Redator de Introdução — Saúde Hormonal e Longevidade",
        goal="Escrever introdução formal, empática e responsável (2–3 parágrafos), citando a palavra-chave 1x, com foco em qualidade de vida e envelhecimento saudável.",
        backstory="Comunicador médico especializado em saúde hormonal; equilibra acolhimento com rigor científico e nunca faz promessas terapêuticas.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) — Urologia e Medicina do Envelhecimento",
        goal="Definir 5–7 H2 numerados com H3 opcionais; contemplar: o que é, sintomas, quando investigar, como funciona o diagnóstico, opções de tratamento e expectativas realistas.",
        backstory="Especialista em outline SEO para médicos; foca na dúvida do paciente que quer entender seus sintomas antes da consulta.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )
    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento — Saúde Hormonal Masculina e Feminina",
        goal="Preencher cada seção com <p> curtos e listas; cobrir: conceito, causas, sintomas, diagnóstico laboratorial, opções de tratamento, cuidados e quando buscar avaliação médica.",
        backstory="Conteúdo médico preciso e acessível; enfatiza sempre que a conduta depende de avaliação individualizada; nunca generaliza ou promete resultado.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_conclusao = Agent(
        role="Redator de Conclusão — Medicina Preventiva e Longevidade",
        goal="Encerrar com síntese objetiva e encorajamento gentil para buscar avaliação médica especializada, sem CTA comercial.",
        backstory="Foco em prevenção, autonomia e qualidade de vida ao longo do envelhecimento.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (body only), coerente, com numeração dos H2 e sem imagens.",
        backstory="Editor técnico focado em semântica e limpeza.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_linkagem = Agent(
        role="Planejador de Linkagem — Dr. Ricardo Ferreira",
        goal="Inserir links internos/externos de forma natural, distribuída e compatível com EEAT médico.",
        backstory="Especialista em internal linking para médicos; prioriza CFM, SBU, SBEM e gov.br.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_assinatura = Agent(
        role="Responsável por Assinatura — Dr. Ricardo Vieira Ferreira",
        goal="Anexar assinatura institucional ao final, sem alterar o conteúdo anterior.",
        backstory="Padronização formal e acolhedora, alinhada ao modelo de atendimento particular e exclusivo.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_revisor = Agent(
        role="Revisor Sênior — Conteúdo Médico-Hormonal",
        goal="Listar melhorias em precisão técnica, tom responsável (sem promessas), distribuição de links e SEO.",
        backstory="Revisor PT-BR especializado em medicina; zela por linguagem ética, sem afirmações absolutas de resultado.",
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
Tom: Dr. Ricardo Ferreira — formal, empático e responsável. Foco em envelhecimento saudável, longevidade e qualidade de vida.
Regras: PT-BR; sem promessas; nunca afirmar que algum tratamento "cura" ou "garante" resultado; PROIBIDO <h1> e imagens; só <p>.
Se houver âncora compatível, inclua 1 link interno natural no 2º parágrafo.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com 2–3 <p> e possivelmente 1 link interno.",
        agent=agente_intro
    )
    tarefa_outline = Task(
        description=f"""
Crie a ESTRUTURA para '{tema}': 5–7 <h2> numerados, até 2 <h3> por seção.
Inclua H2 de "Sintomas e sinais de alerta", H2 "Como é feito o diagnóstico" e H2 "Quando buscar avaliação médica especializada".
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
Cubra: o que é, causas e fatores de risco, sintomas, diagnóstico laboratorial e clínico, opções de tratamento (reposição hormonal, implantes, nutrição), cuidados do dia a dia e quando buscar avaliação médica.
Sempre usar "pode contribuir", "em alguns casos", "dependendo da avaliação clínica" — nunca prometer resultado.
Variar semântica de '{palavra_chave}' sem stuffing. Zero imagens. Zero CTA.
Diretrizes de qualidade obrigatórias:
- SEO local: inserir cidade/bairro/região do cliente de forma natural (mínimo 2 menções no corpo).
- Conexão com serviço: mencionar como o tema se relaciona ao serviço/especialidade real do cliente.
- Profundidade: incluir causas, sinais, critérios de avaliação, exemplos práticos e orientações concretas. Evitar generalidades vagas.
- Semântica/entidades: usar variações e termos correlatos à keyword (sinônimos, subtemas, entidades do domínio).
- Linguagem ética: evitar tom de diagnóstico, promessa de resultado ou urgência. Usar "pode estar associado", "a avaliação profissional é recomendada".

Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com <h2> numerados, <h3>, <p> e <ul><li>.",
        agent=agente_desenvolvimento
    )
    tarefa_conclusao = Task(
        description="Escreva CONCLUSÃO (1–2 <p>): importância do diagnóstico individualizado e do acompanhamento médico contínuo para envelhecer com qualidade. Zero CTA. 1 link interno natural se possível. Sem imagens.",
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
Anexe ao FINAL do HTML a assinatura do Dr. Ricardo Vieira Ferreira (sem alterar o conteúdo anterior):
<p><strong>Quer envelhecer com saúde e qualidade de vida? Agende uma consulta com o Dr. Ricardo Vieira Ferreira.</strong></p>
<p><a href="{WHATSAPP_DRRICARDO}" target="_blank" rel="noopener noreferrer">Fale pelo WhatsApp e agende sua consulta</a></p>
<p><strong>Dr. Ricardo Vieira Ferreira — CRM-SC 13164</strong><br>Uroclínica Jaraguá — Av. Mal. Deodoro da Fonseca, 1188, Salas 208 e 209 – Centro – Jaraguá do Sul – SC<br>Atendimento particular | Consultas às quartas-feiras pela manhã, mediante agendamento prévio.</p>""".strip(),
        expected_output="HTML final com assinatura.",
        agent=agente_assinatura
    )
    tarefa_revisar = Task(
        description=f"""
Revise: ortografia PT-BR, tom formal e responsável (sem promessas, sem afirmações absolutas), H2 numerados, distribuição de links, ausência de imagens/<h1>.
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
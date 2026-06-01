# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from crewai import Crew, Agent, Task, LLM

load_dotenv()

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "People Partner",
    "especialidade": "Consultoria de Recursos Humanos e Gestão de Pessoas",
    "credenciais":   "",
    "cidade":        "Belo Horizonte",
    "estado":        "MG",
    "bairro":        "",
    "servicos":      [
        "HR as a Service (RH como serviço)",
        "estruturação e aprimoramento de processos internos de RH",
        "recrutamento e seleção de talentos",
        "programas de mentoria corporativa e individual",
        "estratégias de engajamento e retenção profissional",
    ],
    "publico":       "empresas de pequeno e médio porte que desejam implantar ou aprimorar RH estratégico, e profissionais em transição",
    "diferencial":   "consultoria imparcial pioneira no modelo HR as a Service, focada em maximizar o potencial humano como motor de crescimento das empresas",
    "segmento":      "corporativo",
    "assinatura":    "People Partner — Recursos Humanos e Gestão de Pessoas | HR as a Service",
}
_localidade = CLIENTE["cidade"] + "/" + CLIENTE["estado"]
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
llm_thinking = LLM(model="gemini/gemini-2.5-flash", temperature=0.4)
llm_no_think = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})
llm_fast     = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})

# -------------------------------
# Catálogo fixo de links internos (People Partner)
# -------------------------------
LINKS_INTERNOS_PEOPLEPARTNER = [
    {"titulo": "Home — People Partner", "url": "https://peoplepartner.com.br/",
     "anchor_sugerida": "consultoria de RH People Partner"},
    {"titulo": "Serviços", "url": "https://peoplepartner.com.br/#servicos",
     "anchor_sugerida": "serviços de consultoria em recursos humanos"},
    {"titulo": "Sobre Nós", "url": "https://peoplepartner.com.br#sobre",
     "anchor_sugerida": "conheça a People Partner e nossa história"},
    {"titulo": "Clientes", "url": "https://peoplepartner.com.br/#clientes",
     "anchor_sugerida": "empresas atendidas pela People Partner"},
    {"titulo": "Vagas", "url": "https://peoplepartner.com.br/vagas",
     "anchor_sugerida": "vagas disponíveis via People Partner"},
    {"titulo": "Blog", "url": "https://peoplepartner.com.br/blog/",
     "anchor_sugerida": "conteúdos sobre gestão de pessoas e RH"},
]

WHATSAPP_PEOPLEPARTNER = "https://api.whatsapp.com/send/?phone=5531995373137&text=Oi!%20Encontrei%20a%20People%20Partner%20no%20Google%20e%20gostaria%20de%20mais%20informações.&type=phone_number&app_absent=0"

# -------------------------------
# SERP helper + whitelist (RH / gestão de pessoas)
# -------------------------------
WHITELIST_EXTERNOS = [
    ".gov", ".gov.br", ".edu", ".edu.br",
    "mte.gov.br", "trabalho.gov.br", "ibge.gov.br",
    "who.int", "ilo.org",
    "shrm.org", "hbr.org",
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
# Função principal — People Partner
# -------------------------------
from crews._common import sanitizar_links as _sanitizar_base


def sanitizar_links(html: str) -> str:
    return _sanitizar_base(html, LINKS_INTERNOS_PEOPLEPARTNER, WHITELIST_EXTERNOS)


def build_crew_peoplepartner(tema: str, palavra_chave: str):
    """
    Gera conteúdo HTML body-only para WordPress no tom da People Partner:
    profissional, empático e orientado a soluções — "o maior ativo de uma empresa
    são as pessoas." Consultoria de RH com +100 empresas atendidas (Brasil e EUA)
    e CEO com 12+ anos de experiência.
    """
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_PEOPLEPARTNER[:]
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    agente_intro = Agent(
        role="Redator de Introdução — Consultoria de RH e Gestão de Pessoas",
        goal="Escrever introdução profissional e empática (2–3 parágrafos), citando a palavra-chave 1x, com foco em pessoas como ativo estratégico das organizações.",
        backstory="Comunicador especializado em RH que conecta estratégia empresarial com desenvolvimento humano.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) — RH e Cultura Organizacional",
        goal="Definir 5–7 H2 numerados com H3 opcionais; contemplar: conceito, impacto no negócio, como implementar, erros comuns, métricas e tendências.",
        backstory="Especialista em outline SEO para consultorias; foca na dúvida do gestor de RH e do empresário.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )
    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento — Gestão de Pessoas e RH Estratégico",
        goal="Preencher cada seção com <p> curtos e listas; cobrir: conceito, benefícios, como aplicar na prática, erros, métricas de sucesso e tendências do mercado.",
        backstory="Conteúdo orientado a resultados e impacto sustentável; linguagem acessível para gestores e empresários.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_conclusao = Agent(
        role="Redator de Conclusão — RH",
        goal="Encerrar com síntese e próximos passos práticos para o gestor, sem CTA comercial.",
        backstory="Foco em ação imediata e perspectiva externa como diferencial competitivo.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (body only), coerente, com numeração dos H2 e sem imagens.",
        backstory="Editor técnico focado em semântica e limpeza.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_linkagem = Agent(
        role="Planejador de Linkagem — People Partner",
        goal="Inserir links internos/externos de forma natural e distribuída.",
        backstory="Especialista em internal linking para consultorias de RH; prioriza MTE, OIT e referências acadêmicas.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_assinatura = Agent(
        role="Responsável por Assinatura — People Partner",
        goal="Anexar assinatura institucional ao final, sem alterar o conteúdo anterior.",
        backstory="Padronização profissional e orientada a propósito.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_revisor = Agent(
        role="Revisor Sênior — Conteúdo de RH",
        goal="Listar melhorias em clareza, tom empático e estratégico, distribuição de links e SEO.",
        backstory="Revisor PT-BR; sem promessas de resultado garantido; linguagem inclusiva e orientada a dados.",
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
Tom: People Partner — empático, estratégico e orientado a impacto. "O maior ativo de uma empresa são as pessoas."
Regras: PT-BR; sem clichês; sem promessas; PROIBIDO <h1> e imagens; só <p>.
Se houver âncora compatível, inclua 1 link interno natural no 2º parágrafo.
Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com 2–3 <p> e possivelmente 1 link interno.",
        agent=agente_intro
    )
    tarefa_outline = Task(
        description=f"""
Crie a ESTRUTURA para '{tema}': 5–7 <h2> numerados, até 2 <h3> por seção.
Inclua H2 de "Erros comuns na gestão de pessoas", H2 "Como implementar na prática" e H2 "Métricas para medir resultados".
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
Cubra: conceito e por que importa para o negócio, como implementar passo a passo, erros comuns, métricas de sucesso, tendências e dicas práticas para gestores.
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
        description="Escreva CONCLUSÃO (1–2 <p>): síntese e próximos passos práticos para o gestor. Zero CTA. 1 link interno natural se possível. Sem imagens.",
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
Anexe ao FINAL do HTML a assinatura da People Partner:
<p><strong>Quer transformar sua gestão de pessoas? Fale com a People Partner.</strong></p>
<p><a href="{WHATSAPP_PEOPLEPARTNER}" target="_blank" rel="noopener noreferrer">Entre em contato pelo WhatsApp</a></p>
<p><strong>People Partner — Consultoria de RH</strong><br>contato@peoplepartner.com.br | (31) 9 9537-3137<br>Atendimento em todo o Brasil e EUA.</p>""".strip(),
        expected_output="HTML final com assinatura.",
        agent=agente_assinatura
    )
    tarefa_revisar = Task(
        description=f"""
Revise: ortografia PT-BR, tom People Partner (empático e estratégico), H2 numerados, distribuição de links, ausência de promessas e de imagens/<h1>.
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
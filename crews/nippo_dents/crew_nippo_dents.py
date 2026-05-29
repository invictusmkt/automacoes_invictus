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
# Catálogo fixo de links internos (Nippodents)
# -------------------------------
LINKS_INTERNOS_NIPPODENTS = [
    {"titulo": "Home — Nippodents", "url": "https://nippodents.com.br/",
     "anchor_sugerida": "clínica odontológica Nippodents na Zona Sul de São Paulo"},
    {"titulo": "A Clínica", "url": "https://nippodents.com.br/clinica-odontologica/",
     "anchor_sugerida": "conheça a clínica Nippodents"},
    {"titulo": "Tratamentos Odontológicos", "url": "https://nippodents.com.br/tratamentos-odontologicos/",
     "anchor_sugerida": "tratamentos odontológicos especializados"},
    {"titulo": "Clínico Geral", "url": "https://nippodents.com.br/clinico-geral-odontologia/",
     "anchor_sugerida": "atendimento odontológico clínico geral"},
    {"titulo": "Implantes Dentários", "url": "https://nippodents.com.br/clinica-implantes-dentarios/",
     "anchor_sugerida": "implantes dentários na Zona Sul de SP"},
    {"titulo": "Próteses Dentárias", "url": "https://nippodents.com.br/clinica-proteses-dentarias/",
     "anchor_sugerida": "próteses dentárias com tecnologia digital"},
    {"titulo": "Lentes de Contato Dental", "url": "https://nippodents.com.br/lentes-de-contato-dental-sao-paulo/",
     "anchor_sugerida": "lentes de contato dental em São Paulo"},
    {"titulo": "Ortodontia", "url": "https://nippodents.com.br/clinica-ortodontia/",
     "anchor_sugerida": "tratamento ortodôntico personalizado"},
    {"titulo": "Check-up Odontológico Digital", "url": "https://nippodents.com.br/clinica-check-up-odontologico-digital/",
     "anchor_sugerida": "check-up odontológico digital completo"},
    {"titulo": "Periodontia", "url": "https://nippodents.com.br/clinica-periodontia/",
     "anchor_sugerida": "tratamento periodontal especializado"},
    {"titulo": "Endodontia", "url": "https://nippodents.com.br/clinica-endodontia/",
     "anchor_sugerida": "endodontia e tratamento de canal"},
    {"titulo": "Odontopediatria", "url": "https://nippodents.com.br/clinica-de-odontopediatria/",
     "anchor_sugerida": "odontopediatria para crianças"},
    {"titulo": "Tratamento Miofuncional", "url": "https://nippodents.com.br/clinica-tratamento-miofuncional/",
     "anchor_sugerida": "terapia miofuncional oral"},
]

WHATSAPP_NIPPODENTS = "https://api.whatsapp.com/send/?phone=5511963263528&text=Oi!%20Encontrei%20a%20Nippodents%20no%20Google%20e%20gostaria%20de%20mais%20informações.&type=phone_number&app_absent=0"

# -------------------------------
# SERP helper + whitelist para externos (odontologia)
# -------------------------------
WHITELIST_EXTERNOS = [
    ".gov", ".gov.br", ".edu", ".edu.br",
    "saude.gov.br", "anvisa.gov.br", "who.int", "nih.gov",
    "cfo.org.br", "cro.org.br",
    "developers.google.com", "support.google.com",
    "schema.org", "w3.org",
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
# Função principal — Nippodents
# -------------------------------
def build_crew_nippodents(tema: str, palavra_chave: str):
    """
    Gera conteúdo HTML body-only para WordPress no tom da Nippodents:
    humanizado, emotivo e técnico — centro de excelência em odontologia digital
    na Zona Sul de São Paulo desde 1998.
    """
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_NIPPODENTS[:]
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    agente_intro = Agent(
        role="Redator de Introdução — Odontologia Digital",
        goal="Escrever introdução humanizada e emotiva (2–3 parágrafos), citando a palavra-chave 1x, com tom de cuidado e paixão pelo trabalho.",
        backstory="Comunicador especializado em saúde bucal que transmite a cultura de amor e excelência da Nippodents.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) — Odontologia",
        goal="Definir 5–7 H2 numerados com H3 opcionais; contemplar tecnologia, indicações, como funciona, cuidados pós-tratamento e expectativas.",
        backstory="Especialista em outline SEO para clínicas odontológicas premium; foca na jornada do paciente.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )
    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento — Odontologia Estética e Funcional",
        goal="Preencher cada seção com <p> curtos e listas, cobrindo: o que é, indicações, tecnologia utilizada, processo, cuidados e resultados realistas.",
        backstory="Conteúdo técnico e acessível, sem promessas de resultado garantido; destaca inovação e cuidado.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_conclusao = Agent(
        role="Redator de Conclusão — Próximos Passos Odontológicos",
        goal="Encerrar com síntese objetiva e encorajamento gentil para agendar avaliação, sem CTA comercial direto.",
        backstory="Fechamentos naturais que reforçam confiança e cuidado.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )
    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (apenas body), coerente, com numeração dos H2 e sem imagens.",
        backstory="Editor técnico focado em semântica e limpeza.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_linkagem = Agent(
        role="Planejador de Linkagem — Nippodents",
        goal="Inserir links internos/externos de forma natural, distribuída e compatível com EEAT em saúde.",
        backstory="Especialista em internal linking para clínicas; prioriza fontes do CFO, CRO e gov.br.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_assinatura = Agent(
        role="Responsável por Assinatura — Nippodents",
        goal="Anexar assinatura institucional ao final (CTA/WhatsApp), sem alterar o conteúdo anterior.",
        backstory="Padronização humanizada e objetiva.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )
    agente_revisor = Agent(
        role="Revisor Sênior — Conteúdo Odontológico",
        goal="Listar melhorias em clareza, tom humanizado, distribuição de links e regras SEO.",
        backstory="Revisor PT-BR; zela por linguagem acessível, técnica e sem promessas.",
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
Tom: humanizado, emotivo e técnico — como a Nippodents ("quando fazemos o que gostamos, fazemos com amor").
Regras: PT-BR; sem clichês; sem promessas; PROIBIDO <h1> e imagens; só <p>.
Se houver âncora compatível, inclua 1 link interno natural no 2º parágrafo.
Concorrência (inspiração – NÃO copiar):\n{dados_concorrencia_txt}""".strip(),
        expected_output="HTML com 2–3 <p> e possivelmente 1 link interno.",
        agent=agente_intro
    )
    tarefa_outline = Task(
        description=f"""
Crie a ESTRUTURA para '{tema}': 5–7 <h2> numerados, até 2 <h3> por seção.
Inclua H2 de "Erros comuns e mitos" e H2 de "Como funciona na prática / o que esperar".
Pelo menos 1 heading com '{palavra_chave}'. Nunca <h1>. Só headings.
- Alinhar os H2 com a intenção de busca: responder diretamente o que o usuário quer saber sobre o tema.
- Trabalhar entidades semânticas: incluir nos headings termos correlatos, sinônimos e subtemas que reforcem a autoridade temática.

Concorrência:\n{dados_concorrencia_txt}""".strip(),
        expected_output="Lista hierárquica com <h2> numerados e <h3> opcionais.",
        agent=agente_outline
    )
    tarefa_desenvolvimento = Task(
        description=f"""
Desenvolva o CORPO (mín. 1200 palavras): <p> curtos, <ul><li> quando listar.
Cubra: o que é, indicações, tecnologia, processo, cuidados pós, expectativas realistas.
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
        description="Escreva CONCLUSÃO (1–2 <p>): aprendizados e próximos passos. Zero CTA. 1 link interno natural se possível. Sem imagens.",
        expected_output="Conclusão em <p> com possível link interno.",
        agent=agente_conclusao
    )
    tarefa_unificar = Task(
        description="Una tudo em HTML único (body only). Mín. 1200 palavras. Tags permitidas: <h2>,<h3>,<p>,<ul>,<li>,<a>,<strong>,<em>. PROIBIDO: <h1>,<html>,<head>,meta,estilos inline,imagens.",
        expected_output="HTML WordPress-ready (body only).",
        agent=agente_unificador
    )

    links_internos_txt = "\n".join(f"- {li['titulo']}: {li['url']} | âncora: {li['anchor_sugerida']}" for li in links_internos)
    links_externos_txt = "\n".join(f"- {le['titulo']}: {le['url']} | âncora: {le['anchor_sugerida']}" for le in links_externos) or "(nenhum externo autorizado encontrado)"

    tarefa_linkagem = Task(
        description=f"""
Insira LINKAGEM no HTML unificado.
Links internos (use >=3, distribuídos):\n{links_internos_txt}
Links externos (use >=1, se listado; target="_blank" rel="noopener noreferrer"):\n{links_externos_txt}
Regras: âncoras descritivas; não linkar em headings; sem inline style; sem imagens.""".strip(),
        expected_output="HTML com links aplicados.",
        agent=agente_linkagem
    )
    tarefa_assinatura = Task(
        description=f"""
Anexe ao FINAL do HTML a assinatura da Nippodents (sem alterar o conteúdo anterior):
<p><strong>Quer cuidar do seu sorriso com quem faz com amor? Fale com a Nippodents.</strong></p>
<p><a href="{WHATSAPP_NIPPODENTS}" target="_blank" rel="noopener noreferrer">Agende pelo WhatsApp</a></p>
<p><strong>Nippodents — Centro de Excelência em Odontologia Digital</strong><br>Av. Fagundes Filho, 141, cj66 – São Judas – São Paulo – SP<br>Seg-Sex 9h-18h | Sáb 9h-13h</p>""".strip(),
        expected_output="HTML final com assinatura.",
        agent=agente_assinatura
    )
    tarefa_revisar = Task(
        description=f"""
Revise: ortografia PT-BR, tom humanizado Nippodents, H2 numerados, distribuição de links, ausência de promessas e de imagens/h1.
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
        description="Aplique TODAS as melhorias. Preserve estrutura semântica, linkagem, ausência de imagens e de <h1>. Saída: HTML final (body only).",
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
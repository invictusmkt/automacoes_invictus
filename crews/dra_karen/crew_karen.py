import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from crewai import Crew, Agent, Task, LLM

load_dotenv()
llm_thinking = LLM(model="gemini/gemini-2.5-flash", temperature=0.4)
llm_no_think = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})
llm_fast     = LLM(model="gemini/gemini-2.0-flash", temperature=0.4)

# -------------------------------
# Catálogo fixo de links internos (Dra. Karen Voltan)
# -------------------------------
LINKS_INTERNOS_KAREN = [
    {"titulo": "Home — Dra. Karen Voltan", "url": "https://drakarenvoltan.com",
     "anchor_sugerida": "Ortopedia Oncológica em São Paulo"},
    {"titulo": "Lipossarcomas de Partes Moles",
     "url": "https://drakarenvoltan.com/lipossarcomas-de-partes-moles-na-ortopedia-oncologica",
     "anchor_sugerida": "lipossarcomas de partes moles"},
    {"titulo": "Tratamento do Mieloma Múltiplo",
     "url": "https://drakarenvoltan.com/tratamento-do-mieloma-multiplo",
     "anchor_sugerida": "tratamento do mieloma múltiplo"},
    {"titulo": "Câncer nos Ossos: sintomas iniciais e diagnóstico",
     "url": "https://drakarenvoltan.com/cancer-nos-ossos-sintomas-iniciais-diagnostico-e-cuidados-em-ortopedia-oncologica",
     "anchor_sugerida": "sintomas iniciais do câncer nos ossos"},
    {"titulo": "Ortopedia Oncológica: tratamento do câncer nos ossos",
     "url": "https://drakarenvoltan.com/ortopedia-oncologica-tratamento-do-cancer-nos-ossos",
     "anchor_sugerida": "tratamento do câncer nos ossos"},
    {"titulo": "Agendamento",
     "url": "https://drakarenvoltan.com/agendamento",
     "anchor_sugerida": "agendar avaliação com a Dra. Karen Voltan"},
]

# -------------------------------
# SERP helper + whitelist para externos (autoridades)
# -------------------------------
WHITELIST_EXTERNOS = [
    # TLDs de confiança
    ".gov", ".gov.br", ".edu", ".edu.br",
    # Buscas/SEO quando necessário
    "developers.google.com", "support.google.com", "search.google.com",
    "schema.org", "w3.org",
    # Autoridades em oncologia/ortopedia/saúde
    "who.int", "nih.gov", "ncbi.nlm.nih.gov", "medlineplus.gov",
    "cancer.gov", "nccn.org", "aacr.org",
    "sbot.org.br", "inca.gov.br", "ms.gov.br",
    "nice.org.uk", "bmj.com", "nejm.org", "nature.com"
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

def buscar_concorrentes_serpapi_texto(palavra_chave: str) -> str:
    """Versão textual para inspiração (NÃO copiar conteúdo)."""
    results = buscar_concorrentes_serpapi_struct(palavra_chave)
    output = []
    for res in results:
        titulo = res.get("title", "")
        snippet = res.get("snippet", "")
        link = res.get("link", "") or res.get("url", "")
        output.append(f"Título: {titulo}\nTrecho: {snippet}\nURL: {link}\n")
    return "\n".join(output)

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

# -------------------------------
# Função principal (Dra. Karen Voltan)
# -------------------------------
def build_crew_karen(tema: str, palavra_chave: str):
    """
    Gera SOMENTE o conteúdo do post (HTML do body), pronto para WordPress,
    para a Dra. Karen Voltan (Ortopedia Oncológica).

    Estilo de saída:
    - Introdução com 1–2 links naturais em <p>.
    - <h2> numerados: "1. ...", "2. ..."; <h3> opcionais.
    - Parágrafos curtos (2–4 linhas); listas <ul><li> quando fizer sentido.
    - Pelo menos UM heading contém a palavra-chave.
    - Sem <h1> e sem imagens.
    - Mínimo 1200 palavras.
    - Linkagem: >=3 internos (intro/corpo/conclusão) e >=1 externo (whitelist).
    - Externos com target="_blank" rel="noopener noreferrer".
    - Conclusão sem CTA; CTA só na assinatura final.
    - Tom informativo, responsável e empático (sem promessas de cura).
    """

    # Monta referências e links automaticamente
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_KAREN[:]  # catálogo fixo
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    # ==== Agentes ====
    agente_intro = Agent(
        role="Redator de Introdução (Ortopedia Oncológica)",
        goal="Escrever introdução acolhedora (2–3 parágrafos) citando a palavra-chave 1x.",
        backstory="Copywriter sênior em saúde; linguagem acessível e responsável para pacientes oncológicos.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )

    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) com numeração",
        goal="Definir 5–7 H2 numerados; H3 opcionais; incluir a palavra-chave em pelo menos um heading.",
        backstory="Especialista em outline SEO em saúde; títulos específicos e éticos.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )

    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento (Educação em Saúde Oncológica)",
        goal="Desenvolver cada seção com <p> curtos e listas; variar semântica sem stuffing; sem imagens.",
        backstory="Produz conteúdo claro, prático e empático; sem autopromoção.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )

    agente_conclusao = Agent(
        role="Redator de Conclusão (sem CTA)",
        goal="Encerrar resumindo aprendizados e próximos passos práticos.",
        backstory="Fechamentos objetivos e humanos.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )

    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (apenas body), coerente, sem redundância, mantendo numeração.",
        backstory="Editor técnico focado em semântica e limpeza para WordPress.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )

    agente_linkagem = Agent(
        role="Planejador e Implementador de Linkagem (EEAT/Oncologia)",
        goal="Inserir links internos/externos de forma natural e distribuída conforme regras.",
        backstory="Especialista em internal linking e autoridade clínica.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )

    agente_contato = Agent(
        role="Responsável por Assinatura (Dra. Karen Voltan)",
        goal="Anexar assinatura institucional ao final do HTML (CTA/Agendamento), sem alterar o conteúdo anterior.",
        backstory="Padronização e identidade da Dra. Karen.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )

    agente_revisor = Agent(
        role="Revisor Sênior PT-BR (Oncologia)",
        goal="Listar melhorias objetivas em clareza, gramática, estilo, linkagem e SEO.",
        backstory="Revisor de saúde; corta redundâncias e mantém consistência.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )

    agente_executor = Agent(
        role="Executor de Revisões",
        goal="Aplicar todas as melhorias preservando estrutura e linkagem.",
        backstory="Editor/Dev de HTML limpo.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )

    # ==== Tarefas ====
    tarefa_intro = Task(
        description=f"""
Escreva a INTRODUÇÃO (2–3 <p>) para '{tema}' usando a palavra-chave '{palavra_chave}' apenas 1 vez.
Contexto: ortopedia oncológica (pacientes e familiares).
Regras:
- PT-BR; parágrafos curtos (2–4 linhas); tom empático e responsável.
- Sem clichês e sem promessas.
- PROIBIDO: <h1> e qualquer imagem.
- Não usar headings; apenas <p>.
- Inclua 1 link interno natural no 2º parágrafo (anchor descritiva), se compatível.
Concorrência (inspiração – NÃO copiar):
{dados_concorrencia_txt}
""".strip(),
        expected_output="HTML com 2–3 <p> e possivelmente 1 link interno natural.",
        agent=agente_intro
    )

    tarefa_outline = Task(
        description=f"""
Crie a ESTRUTURA (apenas headings) para '{tema}':
- 5–7 <h2> numerados ('1. ', '2. ', ...).
- Até 2 <h3> por <h2> quando fizer sentido.
- Pelo menos UM heading deve conter a palavra-chave '{palavra_chave}' de forma natural.
- Incluir um H2 de "Erros comuns e armadilhas" e outro de "Exemplos práticos / aplicação".
- Nunca usar <h1>. Não incluir conteúdo; só <h2>/<h3>.
Baseie a cobertura na intenção de busca dos pacientes e nas lacunas dos concorrentes:
{dados_concorrencia_txt}
""".strip(),
        expected_output="Lista hierárquica com <h2> numerados e <h3> opcionais (sem conteúdo).",
        agent=agente_outline
    )

    tarefa_desenvolvimento = Task(
        description=f"""
Desenvolva o CORPO a partir dos H2/H3 definidos, mantendo a numeração dos H2:
- Mínimo 1200 palavras no post completo.
- <p> curtos (2–4 linhas); usar <ul><li> quando listar.
- Explicar: o que é, por que importa, como fazer, exemplos/rotina do paciente.
- Variar semântica de '{palavra_chave}' sem keyword stuffing.
- Sem autopromoção e sem CTA.
- PROIBIDO inserir imagens.
- Não inventar novos headings; usar apenas os fornecidos.
- Quando fizer sentido, inclua links internos naturais no corpo (anchors descritivas).
Concorrência (inspiração – NÃO copiar):
{dados_concorrencia_txt}
""".strip(),
        expected_output="HTML com <h2> numerados, <h3> opcionais, <p> e <ul><li>.",
        agent=agente_desenvolvimento
    )

    tarefa_conclusao = Task(
        description="""
Escreva a CONCLUSÃO:
- 1–2 <p> resumindo aprendizados e próximos passos práticos (acompanhamento, sinais de alerta, adesão ao plano).
- Zero CTA (o CTA fica na assinatura).
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
- Garantir coerência, zero repetição e manter a NUMERAÇÃO dos <h2>.
- Mínimo 1200 palavras no total.
- Usar apenas: <h2>, <h3>, <p>, <ul>, <li>, <a>, <strong>, <em>.
- PROIBIDO: <h1>, <html>, <head>, <title>, meta, estilos inline, QUALQUER imagem.
Saída: somente o conteúdo do body.
""".strip(),
        expected_output="HTML WordPress-ready (apenas conteúdo do body).",
        agent=agente_unificador
    )

    # >>> links colados na descrição (padrão dos outros arquivos)
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
Insira LINKAGEM no HTML unificado (intro/corpo/conclusão) no estilo da Dra. Karen Voltan.

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
        expected_output="HTML com links internos/externos aplicados.",
        agent=agente_linkagem
    )

    tarefa_contato = Task(
        description="""
Anexar ao FINAL do HTML a assinatura da Dra. Karen (sem alterar o conteúdo anterior):
<p><strong>👉 Agende sua consulta com a Dra. Karen Voltan</strong></p>
<p><a href="https://drakarenvoltan.com/agendamento" target="_blank" rel="noopener noreferrer">Agende sua avaliação online</a></p>
<p><strong>Dra. Karen Voltan — Ortopedista Oncológica</strong><br>Atendimento em São Paulo</p>
""".strip(),
        expected_output="HTML final com assinatura adicionada.",
        agent=agente_contato
    )

    tarefa_revisar = Task(
        description=f"""
Revise o HTML final quanto a:
- Ortografia/gramática PT-BR; clareza; tom empático e responsável.
- Estilo: H2 numerados, parágrafos curtos, listas quando úteis, distribuição de links.
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
- Linkagem já aplicada (ajuste de âncora apenas se necessário).
- Ausência de imagens e de <h1>.
Saída: HTML final (somente conteúdo do body).
""".strip(),
        expected_output="HTML final revisado (body only).",
        agent=agente_executor
    )

    # ==== Crew ====
    crew_karen = Crew(
        agents=[
            agente_intro, agente_outline, agente_desenvolvimento, agente_conclusao,
            agente_unificador, agente_linkagem, agente_contato,
            agente_revisor, agente_executor
        ],
        tasks=[
            tarefa_intro, tarefa_outline, tarefa_desenvolvimento, tarefa_conclusao,
            tarefa_unificar, tarefa_linkagem, tarefa_contato,
            tarefa_revisar, tarefa_corrigir
        ],
        verbose=True
    )
    return crew_karen
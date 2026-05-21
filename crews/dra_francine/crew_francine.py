import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from crewai import Crew, Agent, Task, LLM

load_dotenv()
llm = LLM(model="gemini/gemini-2.5-flash", temperature=0.4)

# -------------------------------
# Catálogo fixo de links internos (Francine)
# -------------------------------
LINKS_INTERNOS_FRANCINE = [
    {
        "titulo": "Clínica Francine Dermatologia (Home)",
        "url": "https://francinedermatologia.com.br",
        "anchor_sugerida": "Clínica Francine Dermatologia em Porto Alegre"
    },
    {
        "titulo": "Sobre a Dra. Francine Costa",
        "url": "https://francinedermatologia.com.br/dra-francine-costa-dermatologia-clinica-e-estetica-em-porto-alegre/",
        "anchor_sugerida": "conheça a Dra. Francine Costa"
    },
    {
        "titulo": "Tratamentos",
        "url": "https://francinedermatologia.com.br/tratamentos/",
        "anchor_sugerida": "tratamentos dermatológicos na clínica"
    },
    {
        "titulo": "Blog",
        "url": "https://francinedermatologia.com.br/blog/",
        "anchor_sugerida": "conteúdos sobre saúde e beleza da pele"
    }
]

# -------------------------------
# SERP helper + whitelist para externos (autoridades médicas)
# -------------------------------
WHITELIST_EXTERNOS_FRANCINE = [
    # TLDs de confiança
    ".gov", ".gov.br", ".edu", ".edu.br",
    # Autoridades médicas e de saúde
    "sbd.org.br",              # Sociedade Brasileira de Dermatologia
    "aad.org",                 # American Academy of Dermatology
    "who.int",                 # OMS
    "nhs.uk",                  # National Health Service (UK)
    "cdc.gov",                 # CDC (EUA)
    "nih.gov", "ncbi.nlm.nih.gov", "medlineplus.gov",  # NIH / PubMed / Medline
    "cochranelibrary.com",     # Revisões sistemáticas
    "dermnetnz.org",           # DermNet
    # Padrões web/SEO úteis quando apropriado
    "schema.org", "w3.org", "developers.google.com", "support.google.com"
]

def _usa_whitelist_francine(url: str) -> bool:
    url_l = (url or "").lower()
    return any(dom in url_l for dom in WHITELIST_EXTERNOS_FRANCINE)

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
        if _usa_whitelist_francine(url):
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
    """Versão textual só para inspiração (NÃO copiar)."""
    results = buscar_concorrentes_serpapi_struct(palavra_chave)
    output = []
    for res in results:
        titulo = res.get("title", "")
        snippet = res.get("snippet", "")
        link = res.get("link", "") or res.get("url", "")
        output.append(f"Título: {titulo}\nTrecho: {snippet}\nURL: {link}\n")
    return "\n".join(output)

# -------------------------------
# Função principal (Francine)
# -------------------------------
def build_crew_francine(tema: str, palavra_chave: str):
    """
    Gera SOMENTE o conteúdo do post (HTML do body), pronto para WordPress, para a
    Clínica Francine Dermatologia.

    Estilo de saída:
    - Introdução com 1–2 links naturais em <p>.
    - <h2> numerados: "1. ...", "2. ..."; <h3> opcionais.
    - Parágrafos curtos (2–4 linhas); listas <ul><li> quando fizer sentido.
    - Pelo menos UM heading contém a palavra‑chave.
    - Sem <h1> e sem imagens.
    - Mínimo 1200 palavras.
    - Linkagem: >=3 internos distribuídos (intro/corpo/conclusão) e >=1 externo de autoridade.
    - Anchors descritivas; externos com target="_blank" rel="noopener noreferrer".
    - Conclusão sem CTA comercial; CTA na assinatura final da Dra. Francine.
    """
    llm_local = llm

    # Monta referências e links automaticamente
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_FRANCINE[:]  # catálogo fixo (Francine)
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    # ==== Agentes ====
    agente_intro = Agent(
        role="Redator de Introdução (Dermatologia)",
        goal="Escrever introdução clara e acolhedora (2–3 parágrafos) no tom da clínica, citando a palavra‑chave 1x.",
        backstory="Copywriter sênior em saúde; parágrafos curtos, linguagem acessível e responsável; sem imagens.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) numerada",
        goal="Definir 5–7 H2 numerados (1., 2., 3., ...), com H3 opcionais; cobrir intenção de busca do paciente e incluir a palavra‑chave em pelo menos um heading.",
        backstory="Especialista em outline SEO para saúde; nunca usa H1; títulos informativos e específicos.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento (Educação em Saúde)",
        goal="Preencher cada seção com orientação prática, sem promessas; variar semântica da keyword sem stuffing e sem inserir imagens.",
        backstory="Produz conteúdo útil, com exemplos, listas e linguagem clara; sem autopromoção.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_conclusao = Agent(
        role="Redator de Conclusão (sem CTA)",
        goal="Encerrar resumindo aprendizados e próximos passos práticos, sem CTA comercial.",
        backstory="Fechamentos objetivos e empáticos.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (apenas body), coerente, sem redundância, mantendo numeração e sem imagens.",
        backstory="Editor técnico focado em semântica limpa para WordPress.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_linkagem = Agent(
        role="Planejador e Implementador de Linkagem (EEAT)",
        goal="Inserir links internos/externos de forma natural e distribuída, priorizando autoridade médica.",
        backstory="Especialista em internal linking e EEAT para área da saúde.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_contato = Agent(
        role="Responsável por Assinatura (Clínica Francine)",
        goal="Anexar assinatura institucional da clínica ao final do HTML (CTA/WhatsApp), sem alterar o conteúdo anterior.",
        backstory="Padronização e identidade da Dra. Francine.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_revisor = Agent(
        role="Revisor Sênior PT-BR",
        goal="Listar melhorias objetivas (bullets) em clareza, gramática, estilo, linkagem e regras SEO.",
        backstory="Revisor de saúde; corta redundâncias e mantém consistência.",
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
Escreva a INTRODUÇÃO (2–3 <p>) para '{tema}' usando a palavra‑chave '{palavra_chave}' apenas 1 vez.
Estilo: acolhedor, informativo, sem jargões.
Regras:
- PT‑BR; parágrafos curtos (2–4 linhas).
- Sem clichês e sem promessas.
- PROIBIDO: <h1> e qualquer imagem.
- Não usar headings; apenas <p>.
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
- Pelo menos UM heading (<h2> ou <h3>) deve conter a palavra‑chave '{palavra_chave}' de forma natural.
- Incluir um H2 equivalente a "Erros comuns e armadilhas" e outro a "Exemplos práticos / aplicação".
- Títulos específicos para dermatologia, claros e não genéricos.
- Nunca usar <h1>. Não incluir conteúdo; só <h2>/<h3>.
Baseie a cobertura na intenção de busca do paciente e lacunas dos concorrentes:
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
- Explique: o que é, por que importa, como fazer, exemplos reais.
- Variar semântica de '{palavra_chave}' sem keyword stuffing.
- Sem autopromoção e sem CTA.
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
- 1–2 <p> resumindo aprendizados e próximos passos práticos.
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
- Garantir coerência, zero repetição e manter a NUMERAÇÃO dos <h2> (1., 2., 3., ...).
- Mínimo 1200 palavras no total.
- Usar apenas: <h2>, <h3>, <p>, <ul>, <li>, <a>, <strong>, <em>.
- PROIBIDO: <h1>, <html>, <head>, <title>, meta, estilos inline, QUALQUER tag de imagem.
Saída: somente o conteúdo do body.
""".strip(),
        expected_output="HTML WordPress-ready (apenas conteúdo do body, sem imagens).",
        agent=agente_unificador
    )

    # Links colados na descrição (seguindo padrão Invictus)
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
Insira LINKAGEM no HTML unificado (intro/corpo/conclusão) no estilo da Clínica Francine.

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

    tarefa_contato = Task(
        description="""
Anexar ao FINAL do HTML a assinatura da clínica (sem alterar o conteúdo anterior):
<p><strong>👉 Agende sua consulta com a Dra. Francine Costa</strong></p>
<p><a href="https://api.whatsapp.com/send?phone=5551999114348&text=Oi!%20Encontrei%20seu%20site%20e%20gostaria%20de%20mais%20informações." target="_blank" rel="noopener noreferrer">Fale pelo WhatsApp: (51) 99911‑4348</a></p>
<p><strong>Clínica Francine Dermatologia</strong><br>R. 24 de Outubro, 1440 – Sala 1107 – Auxiliadora, Porto Alegre – RS</p>
""".strip(),
        expected_output="HTML final com assinatura adicionada.",
        agent=agente_contato
    )

    tarefa_revisar = Task(
        description=f"""
Revise o HTML final quanto a:
- Ortografia/gramática PT‑BR; clareza; tom acolhedor e profissional da clínica.
- Estilo: H2 numerados, parágrafos curtos, listas quando úteis, distribuição de links.
- Coerência e distribuição de links; âncoras descritivas; ausência de overstuffing de '{palavra_chave}'.
- Respeito às proibições de imagens e de <h1>.
Saída: lista de melhorias acionáveis em bullets JSON‑like:
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
    crew_francine = Crew(
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
    return crew_francine
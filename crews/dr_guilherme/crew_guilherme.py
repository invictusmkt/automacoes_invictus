import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from crewai import Crew, Agent, Task, LLM

load_dotenv()
llm_thinking = LLM(model="gemini/gemini-2.5-flash", temperature=0.4)
llm_no_think = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})
llm_fast     = LLM(model="gemini/gemini-2.5-flash", temperature=0.4, thinking={"type": "disabled"})

# -------------------------------
# Catálogo fixo de links internos (Dr. Guilherme Gadens)
# -------------------------------
LINKS_INTERNOS_GADENS = [
    {"titulo": "Início", "url": "https://drguilhermegadens.com.br",
     "anchor_sugerida": "conheça a clínica do Dr. Guilherme Gadens"},
    {"titulo": "Sobre o Dr. Guilherme Gadens", "url": "https://drguilhermegadens.com.br/sobre/",
     "anchor_sugerida": "conheça a formação e experiência do Dr. Guilherme Gadens"},
    {"titulo": "Cirurgia de Mohs", "url": "https://drguilhermegadens.com.br/cirurgia-de-mohs/",
     "anchor_sugerida": "entenda como funciona a cirurgia de Mohs"},
    {"titulo": "Mapeamento Corporal Total", "url": "https://drguilhermegadens.com.br/mapeamento-corporal/",
     "anchor_sugerida": "mapeamento corporal total para prevenção do câncer de pele"},
    {"titulo": "Diferenciais da Clínica", "url": "https://drguilhermegadens.com.br/diferenciais/",
     "anchor_sugerida": "diferenciais em dermatoscopia digital e diagnóstico precoce"},
    {"titulo": "Conteúdos e Artigos", "url": "https://drguilhermegadens.com.br/conteudos/",
     "anchor_sugerida": "leia conteúdos e artigos sobre câncer de pele"},
    {"titulo": "Agende pelo WhatsApp", "url": "https://api.whatsapp.com/send/?phone=5541992221412&text=Olá%21+Vim+do+site+e+preciso+de+mais+informações.&type=phone_number&app_absent=0",
     "anchor_sugerida": "fale com a equipe pelo WhatsApp"}
]

# -------------------------------
# SERP helper + whitelist para externos (foco saúde/dermatologia/oncologia)
# -------------------------------
WHITELIST_EXTERNOS = [
    ".gov", ".gov.br", ".edu", ".edu.br",
    "who.int", "cdc.gov", "cancer.org", "aad.org", "sbd.org.br", "inca.gov.br",
    "nih.gov", "ncbi.nlm.nih.gov", "jamanetwork.com", "nejm.org",
    "oecd.org", "unesco.org", "iso.org",
    "developers.google.com", "support.google.com", "search.google.com",
    "schema.org", "w3.org",
    "moz.com", "ahrefs.com", "semrush.com", "data.gov"
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
# Função principal (Dr. Guilherme Gadens)
# -------------------------------
def build_crew_guilherme(tema: str, palavra_chave: str):
    """
    Gera SOMENTE o conteúdo do post (HTML do body), pronto para WordPress, no estilo do Dr. Guilherme Gadens.

    Estilo de saída:
    - Introdução com 1–2 links naturais em <p>.
    - <h2> numerados: "1. ...", "2. ..."; <h3> opcionais.
    - Parágrafos curtos (2–4 linhas); listas <ul><li> quando fizer sentido.
    - Pelo menos UM heading contém a palavra-chave.
    - Sem <h1> e sem imagens.
    - Mínimo 1200 palavras.
    - Linkagem: >=3 internos distribuídos (intro/corpo/conclusão) e >=1 externo (se houver whitelist).
    - Anchors descritivas; externos com target="_blank" rel="noopener noreferrer".
    - Conclusão sem CTA; CTA na assinatura ao final.
    - Tom: médico, claro e acessível; foco em prevenção, diagnóstico precoce, dermatoscopia digital e Cirurgia de Mohs quando pertinente.
    """

    # Monta referências e links automaticamente
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_GADENS[:]  # catálogo fixo
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    # ==== Agentes ====
    agente_intro = Agent(
        role="Redator de Introdução",
        goal="Escrever introdução clara e confiável (2–3 parágrafos) no tom médico do Dr. Gadens, citando a palavra-chave 1x.",
        backstory="Dermatologia oncológica; evita sensacionalismo; linguagem acessível e precisa.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )

    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) com numeração",
        goal="Definir 5–7 H2 numerados; cobrir intenção de busca; incluir a palavra-chave em pelo menos um heading.",
        backstory="Especialista em outline SEO para conteúdos médicos; títulos específicos e orientados a decisão clínica do paciente.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )

    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento",
        goal="Preencher cada seção com <p> curtos e listas úteis, variar semântica da keyword sem stuffing e sem inserir imagens.",
        backstory="Explicações objetivas, prevenção, sinais de alarme, quando procurar o especialista, e diferenças entre abordagens diagnósticas (ex.: dermatoscopia digital, biópsia, Cirurgia de Mohs).",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )

    agente_conclusao = Agent(
        role="Redator de Conclusão (sem CTA)",
        goal="Encerrar resumindo aprendizados e próximos passos práticos para o leitor/paciente, sem convite comercial.",
        backstory="Fechamentos naturais, objetivos e empáticos.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )

    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (apenas body), coerente, sem redundância, com numeração dos H2 e sem imagens.",
        backstory="Editor técnico focado em semântica, acessibilidade e limpeza de HTML.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )

    agente_linkagem = Agent(
        role="Planejador e Implementador de Linkagem",
        goal="Inserir links internos/externos de forma natural e distribuída, respeitando todas as regras.",
        backstory="Especialista em internal linking e EEAT em saúde.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )

    agente_contato = Agent(
        role="Responsável por Contato e Assinatura",
        goal="Anexar assinatura institucional do Dr. Guilherme Gadens ao final do HTML (CTA/WhatsApp), sem alterar o conteúdo anterior.",
        backstory="Padronização e identidade médica.",
        verbose=True, allow_delegation=False, llm=llm_fast,
    )

    agente_revisor = Agent(
        role="Revisor Sênior",
        goal="Listar melhorias objetivas (bullets) em clareza, gramática, tom médico, distribuição de links e regras SEO.",
        backstory="Revisor PT-BR para conteúdos médicos; elimina ambiguidades e redundâncias.",
        verbose=True, allow_delegation=False, llm=llm_thinking,
    )

    agente_executor = Agent(
        role="Executor de Revisões",
        goal="Aplicar todas as melhorias preservando estrutura semântica e linkagem.",
        backstory="Editor/Dev de HTML limpo.",
        verbose=True, allow_delegation=False, llm=llm_no_think,
    )

    # ==== Tarefas ====
    tarefa_intro = Task(
        description=f"""
Escreva a INTRODUÇÃO (2–3 <p>) para '{tema}' usando a palavra-chave '{palavra_chave}' apenas 1 vez.
Tom médico, acessível e preciso.
Regras:
- PT-BR; parágrafos curtos (2–4 linhas).
- Sem clichês e sem promessas; linguagem empática e baseada em evidências.
- PROIBIDO: <h1> e qualquer imagem.
- Não usar headings na introdução; só <p>.
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
- Pelo menos UM heading (<h2> ou <h3>) deve conter a palavra-chave '{palavra_chave}' de forma natural.
- Incluir um H2 equivalente a "Erros comuns e armadilhas" e outro a "Exemplos práticos / aplicação".
- Títulos específicos, claros e orientados a tomada de decisão do paciente.
- Nunca usar <h1>. Não incluir conteúdo; só <h2>/<h3>.
- Alinhar os H2 com a intenção de busca: responder diretamente o que o usuário quer saber sobre o tema.
- Trabalhar entidades semânticas: incluir nos headings termos correlatos, sinônimos e subtemas que reforcem a autoridade temática.

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
- Explicar: o que é, sinais de alerta, prevenção, diagnóstico (ex.: dermatoscopia digital, biópsia), tratamento (ex.: Cirurgia de Mohs quando pertinente) e acompanhamento.
- Variar semântica de '{palavra_chave}' sem stuffing.
- Sem autopromoção e sem CTA.
- PROIBIDO inserir imagens.
- Não inventar novos headings; usar apenas os fornecidos.
- Quando fizer sentido, inclua links internos naturais no corpo (anchors descritivas).
Diretrizes de qualidade obrigatórias:
- SEO local: inserir cidade/bairro/região do cliente de forma natural (mínimo 2 menções no corpo).
- Conexão com serviço: mencionar como o tema se relaciona ao serviço/especialidade real do cliente.
- Profundidade: incluir causas, sinais, critérios de avaliação, exemplos práticos e orientações concretas. Evitar generalidades vagas.
- Semântica/entidades: usar variações e termos correlatos à keyword (sinônimos, subtemas, entidades do domínio).
- Linguagem ética: evitar tom de diagnóstico, promessa de resultado ou urgência. Usar "pode estar associado", "a avaliação profissional é recomendada".

Concorrência (inspiração – NÃO copiar):
{dados_concorrencia_txt}
""".strip(),
        expected_output="HTML com <h2> numerados, <h3> opcionais, <p> e <ul><li> (sem imagens).",
        agent=agente_desenvolvimento
    )

    tarefa_conclusao = Task(
        description="""
Escreva a CONCLUSÃO:
- 1–2 <p> resumindo aprendizados e próximos passos práticos (ex.: observar lesões, quando procurar especialista).
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

    # Links disponíveis para a etapa de linkagem
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
Insira LINKAGEM no HTML unificado (intro/corpo/conclusão).

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
Anexar ao FINAL do HTML a assinatura institucional (sem alterar o conteúdo anterior):

<p><strong>👉 Clique em saiba mais e agende sua consulta com o Dr. Guilherme Gadens!</strong></p>
<p><a href="https://api.whatsapp.com/send/?phone=5541992221412&text=Olá%21+Vim+do+site+e+preciso+de+mais+informações.&type=phone_number&app_absent=0" target="_blank" rel="noopener noreferrer">Link para WhatsApp</a></p>
<p><strong>Dr. Guilherme Gadens</strong><br>Dermatologista — Cirurgia de Mohs e Dermatoscopia Digital em Curitiba</p>
""".strip(),
        expected_output="HTML final com assinatura adicionada.",
        agent=agente_contato
    )

    tarefa_revisar = Task(
        description=f"""
Revise o HTML final quanto a:
- Ortografia/gramática PT-BR; clareza; tom médico (preciso, acessível).
- Estilo: H2 numerados, parágrafos curtos, listas quando úteis, distribuição de links.
- Coerência e distribuição de links; âncoras descritivas; ausência de overstuffing de '{palavra_chave}'.
- Respeito às proibições de imagens e de <h1>.
Checklist de qualidade obrigatório — verificar TODOS os itens antes de finalizar:
- CTA ético: evitar "agende agora", "não adie", "invista na sua saúde", "transformação". Preferir linguagem educativa e neutra.
- Assinatura: está personalizada e profissional (com CRM/CREFITO/OAB quando aplicável)?
- Linguagem ética: ausência de promessas de resultado, tom de diagnóstico ou urgência. Usar "pode estar associado", "a avaliação profissional é recomendada", "a conduta depende do caso".
- SEO local: cidade/bairro/região do cliente aparecem de forma natural no corpo (mínimo 2 ocorrências)?
- Conexão com serviço: o artigo conecta o tema ao serviço/especialidade real do cliente?
- Profundidade: há causas, sinais, critérios de avaliação, exemplos práticos e orientações concretas?
- Intenção de busca: os H2s respondem ao que o usuário busca? Alinhamento com a palavra-chave e entidades do tema?
- Links internos: levam a páginas reais e relevantes? Âncoras descritivas (nunca "clique aqui")?

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
    crew_gadens = Crew(
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
    return crew_gadens
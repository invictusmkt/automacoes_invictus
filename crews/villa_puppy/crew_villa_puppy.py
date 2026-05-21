import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from crewai import Crew, Agent, Task, LLM

load_dotenv()
llm = LLM(model="gemini/gemini-2.5-flash", temperature=0.4)

# -------------------------------
# Catálogo fixo de links internos (Villa Puppy)
# -------------------------------
LINKS_INTERNOS_VILLAPUPPY = [
    {
        "titulo": "Home — Villa Puppy",
        "url": "https://villapuppy.com.br/#home",
        "anchor_sugerida": "conheça a Villa Puppy Pet Shop no Shopping VillaLobos"
    },
    {
        "titulo": "Posicionamento",
        "url": "https://villapuppy.com.br/#posicionamento",
        "anchor_sugerida": "nossa filosofia de carinho e cuidado com os pets"
    },
    {
        "titulo": "Serviços",
        "url": "https://villapuppy.com.br/#servicos",
        "anchor_sugerida": "banho e tosa, clínica veterinária e muito mais"
    },
    {
        "titulo": "Marcas",
        "url": "https://villapuppy.com.br/#marcas",
        "anchor_sugerida": "marcas de ração e acessórios que trabalhamos"
    },
    {
        "titulo": "Depoimentos",
        "url": "https://villapuppy.com.br/#depoimentos",
        "anchor_sugerida": "o que os tutores dizem sobre a Villa Puppy"
    },
    {
        "titulo": "Localização",
        "url": "https://villapuppy.com.br/#localizacao",
        "anchor_sugerida": "como chegar na nossa loja no Shopping VillaLobos"
    },
    {
        "titulo": "Propósito",
        "url": "https://villapuppy.com.br/#proposito",
        "anchor_sugerida": "nosso propósito de cuidado e bem-estar animal"
    },
    {
        "titulo": "Contato",
        "url": "https://villapuppy.com.br/#contato",
        "anchor_sugerida": "fale com a equipe da Villa Puppy"
    },
]

WHATSAPP_VILLAPUPPY = "https://api.whatsapp.com/send?phone=5511917411212&text=Ol%C3%A1,%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es%20sobre%20a%20Villa%20Puppy"

# -------------------------------
# SERP helper + whitelist para externos
# -------------------------------
WHITELIST_EXTERNOS = [
    ".gov", ".gov.br", ".edu", ".edu.br",
    "crmv.org.br", "crmvsp.gov.br", "saude.sp.gov.br",
    "who.int", "oie.int", "mapa.gov.br", "agricultura.gov.br",
    "developers.google.com", "support.google.com", "search.google.com",
    "schema.org", "w3.org",
    "moz.com", "ahrefs.com", "semrush.com",
    "oecd.org", "iso.org", "data.gov"
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
# Função principal — Villa Puppy
# -------------------------------
def build_crew_villapuppy(tema: str, palavra_chave: str):
    """
    Gera SOMENTE o conteúdo do post (HTML do body), pronto para WordPress, no tom Villa Puppy:
    acessível, empático e voltado a tutores, destacando carinho, profissionalismo e bem-estar animal.

    Estilo de saída:
    - Introdução com 1–2 links naturais em <p>.
    - <h2> numerados: "1. ...", "2. ..."; <h3> opcionais.
    - Parágrafos curtos (2–4 linhas); listas <ul><li> quando fizer sentido.
    - Pelo menos UM heading contém a palavra‑chave.
    - Sem <h1> e sem imagens.
    - Mínimo 1200 palavras.
    - Linkagem: >=3 internos distribuídos (intro/corpo/conclusão) e >=1 externo (se houver whitelist).
    - Anchors descritivas; externos com target="_blank" rel="noopener noreferrer".
    - Conclusão sem CTA comercial; CTA/assinatura ao final (padrão Villa Puppy, personalizado ao tema).
    """
    llm_local = llm

    # Monta referências e links automaticamente
    dados_concorrencia_txt = buscar_concorrentes_serpapi_texto(palavra_chave)
    serp_struct = buscar_concorrentes_serpapi_struct(palavra_chave)
    links_internos = LINKS_INTERNOS_VILLAPUPPY[:]  # catálogo fixo
    links_externos = selecionar_links_externos_autoritativos(serp_struct, max_links=2)

    # ==== Agentes (adaptados ao setor pet) ====
    agente_intro = Agent(
        role="Redator de Introdução (Pet)",
        goal="Escrever introdução clara e acolhedora (2–3 parágrafos), mencionando a palavra‑chave 1x.",
        backstory="Especialista em conteúdo para tutores; tom empático, prático e confiável.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_outline = Agent(
        role="Arquiteto de Estrutura (H2/H3) com numeração",
        goal="Definir 5–7 H2 numerados (1., 2., 3., ...), com H3 opcionais; cobrir a intenção de busca e incluir a palavra‑chave em pelo menos um heading.",
        backstory="Especialista em outline SEO para varejo pet; nunca usa H1; títulos específicos.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_desenvolvimento = Agent(
        role="Redator de Desenvolvimento (Pet)",
        goal="Preencher cada seção com <p> curtos e listas, com orientações práticas de cuidado, higiene, alimentação e bem‑estar.",
        backstory="Conteúdo útil, direto, com exemplos reais e linguagem acessível para tutores.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_conclusao = Agent(
        role="Redator de Conclusão (sem CTA)",
        goal="Encerrar resumindo aprendizados e próximos passos práticos (checklist simples para o tutor).",
        backstory="Fechamentos objetivos e acolhedores.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_unificador = Agent(
        role="Unificador de Conteúdo HTML",
        goal="Unir tudo em HTML único (apenas body), coerente, sem redundância, com numeração dos H2 e sem imagens.",
        backstory="Editor técnico focado em semântica e limpeza de HTML.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_linkagem = Agent(
        role="Planejador e Implementador de Linkagem",
        goal="Inserir links internos/externos de forma natural e distribuída, respeitando todas as regras e o tom Villa Puppy.",
        backstory="Especialista em internal linking e EEAT no universo pet.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_contato = Agent(
        role="Responsável por Contato e Assinatura (Villa Puppy)",
        goal=(
            "Gerar e anexar uma assinatura personalizada ao TEMA, seguindo o padrão Villa Puppy: "
            "1) linha de convite com um destaque relacionado ao tema, "
            "2) endereço fixo da loja, "
            "3) link de WhatsApp fornecido, "
            "4) linha final com uma chamada relacionada ao tema."
        ),
        backstory="Padronização e identidade afetiva da marca, mantendo foco em conveniência para o tutor.",
        verbose=True, allow_delegation=False, llm=llm_local,
    )

    agente_revisor = Agent(
        role="Revisor Sênior",
        goal="Listar melhorias objetivas (bullets) em clareza, gramática, estilo, distribuição de links e regras SEO.",
        backstory="Revisor PT‑BR; corta redundâncias; mantém consistência.",
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
Tom Villa Puppy: acessível, positivo e acolhedor (sem infantilizar).
Regras:
- PT‑BR; parágrafos curtos (2–4 linhas).
- Sem clichês e sem promessas vazias.
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
- Pelo menos UM heading (<h2> ou <h3>) deve conter a palavra‑chave '{palavra_chave}' de forma natural.
- Incluir um H2 equivalente a "Erros comuns e armadilhas" e outro a "Exemplos práticos / aplicação".
- Títulos específicos, claros e não genéricos; foco em orientação para o tutor.
- Nunca usar <h1>. Não incluir conteúdo; só <h2>/<h3>.
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
- Explicar: o que é, por que importa, como fazer (passo a passo), cuidados, sinais de alerta, quando procurar o veterinário.
- Variar semântica de '{palavra_chave}' sem stuffing.
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
- 1–2 <p> resumindo aprendizados e próximos passos práticos (ex.: checklist simples de cuidados).
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
Insira LINKAGEM no HTML unificado (intro/corpo/conclusão) seguindo as regras.

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

    # Assinatura personalizada (seguir padrão solicitado em memória do projeto)
    tarefa_contato = Task(
        description=f"""
Crie e ANEXE ao FINAL do HTML a assinatura personalizada da Villa Puppy, adaptando o texto ao TEMA '{tema}' (sem alterar o conteúdo anterior):

<p><strong>Quer conhecer [destaque relacionado ao tema]?</strong> Agende sua visita na Villa Puppy Pet Shop:</p>
<p>📍 Shopping VillaLobos, Av. Dra. Ruth Cardoso, 4777 – Jardim Universidade Pinheiros, São Paulo/SP</p>
<p><strong><a href="{WHATSAPP_VILLAPUPPY}" target="_blank" rel="noopener noreferrer">Clique aqui e fale conosco agora pelo WhatsApp!</a></strong></p>
<p><strong>Villa Puppy</strong> – [chamada final relacionada ao tema]</p>

Regras:
- Substitua os colchetes [ ] com frases curtas e naturais baseadas no TEMA.
- Não repita a palavra‑chave em excesso; seja natural e acolhedor.
- Não inserir imagens nem estilos inline.
""".strip(),
        expected_output="HTML final com assinatura adicionada e personalizada ao tema.",
        agent=agente_contato
    )

    tarefa_revisar = Task(
        description=f"""
Revise o HTML final quanto a:
- Ortografia/gramática PT‑BR; clareza; tom Villa Puppy (acessível, empático, confiável).
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
    crew_villapuppy = Crew(
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
    return crew_villapuppy

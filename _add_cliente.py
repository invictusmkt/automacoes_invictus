# -*- coding: utf-8 -*-
"""
Script temporário — injeta bloco CLIENTE em cada crew e torna dinâmicos
os guidelines de SEO local e conexão com serviço nos prompts.
"""
import os

ROOT = r"D:\Users\Enzo\Documents\Trabalho\Invictus\Projetos\automacoes_invictus\crews"

# ──────────────────────────────────────────────────────────────────────────────
# Bloco CLIENTE para cada arquivo (nome do arquivo → texto a inserir)
# ──────────────────────────────────────────────────────────────────────────────
BLOCOS = {

"crew_tati.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "Dra. Tatiana Villas Boas Gabbi",
    "especialidade": "Médica Dermatologista",
    "credenciais":   "CRM-SP 104415 | RQE 31137",
    "cidade":        "São Paulo",
    "estado":        "SP",
    "bairro":        "Itaim Bibi",
    "servicos":      [
        "tratamento de doenças das unhas (onicopatias)",
        "queda de cabelo (tricologia)",
        "tratamentos dermatológicos para pele",
        "cirurgia ungueal",
    ],
    "publico":       "pessoas com patologias de unhas, cabelos e pele em busca de diagnóstico e tratamento especializado",
    "diferencial":   "referência nacional e internacional em doenças das unhas (onicopatias), formada pela USP e membro da European Nail Society",
    "segmento":      "saúde",
    "assinatura":    "Dra. Tatiana Villas Boas Gabbi — Dermatologista em São Paulo/SP | CRM-SP 104415 | RQE 31137",
}
_localidade = (CLIENTE["bairro"] + ", " if CLIENTE["bairro"] else "") + CLIENTE["cidade"] + "/" + CLIENTE["estado"]
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_nucleo_rural.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "Núcleo Rural Saúde Animal",
    "especialidade": "Suplementação e Nutrição Animal",
    "credenciais":   "",
    "cidade":        "São José do Rio Preto",
    "estado":        "SP",
    "bairro":        "",
    "servicos":      [
        "suplementos minerais para gado de corte",
        "suplementos minerais para gado de leite",
        "nutracêuticos para saúde animal",
    ],
    "publico":       "pecuaristas, produtores rurais e criadores de gado de corte e leite",
    "diferencial":   "soluções de alta tecnologia em suplementação e nutrição animal para aumento de produtividade no campo",
    "segmento":      "agronegócio",
    "assinatura":    "Núcleo Rural — Suplementação e Nutrição Animal em São José do Rio Preto/SP",
}
_localidade = (CLIENTE["bairro"] + ", " if CLIENTE["bairro"] else "") + CLIENTE["cidade"] + "/" + CLIENTE["estado"]
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_villa_puppy.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "Villa Puppy",
    "especialidade": "Pet Shop, Clínica Veterinária e Estética Pet",
    "credenciais":   "",
    "cidade":        "São Paulo",
    "estado":        "SP",
    "bairro":        "Alto de Pinheiros",
    "servicos":      [
        "estética pet (Puppy Spa - banho e tosa)",
        "consultas veterinárias",
        "venda de rações super premium e acessórios",
        "venda de filhotes selecionados com pedigree",
    ],
    "publico":       "tutores de cães e gatos em busca de serviços de estética, saúde animal de alto padrão e filhotes selecionados",
    "diferencial":   "estética pet com produtos hipoalergênicos e veganos, localizada no Shopping VillaLobos com estrutura integrada",
    "segmento":      "veterinário",
    "assinatura":    "Villa Puppy — Pet Shop, Clínica Veterinária e Estética Pet em Alto de Pinheiros, São Paulo/SP",
}
_localidade = (CLIENTE["bairro"] + ", " if CLIENTE["bairro"] else "") + CLIENTE["cidade"] + "/" + CLIENTE["estado"]
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_clinicas_nexo.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "Nexo - Instituto de Psicologia Aplicada",
    "especialidade": "Psicologia e Saúde Mental",
    "credenciais":   "",
    "cidade":        "Americana",
    "estado":        "SP",
    "bairro":        "",
    "servicos":      [
        "psicoterapia individual (infantil, adolescentes, adultos e idosos)",
        "atendimento especializado em TEA/ABA",
        "avaliação neuropsicológica",
        "fonoaudiologia e terapia ocupacional",
        "parcerias corporativas de saúde mental",
    ],
    "publico":       "crianças, adolescentes, adultos, idosos, pessoas com TEA/TDAH, empresas e profissionais da psicologia",
    "diferencial":   "referência em intervenção ABA para autismo e atendimento multidisciplinar integrado no interior de SP (Americana, Campinas, Piracicaba)",
    "segmento":      "saúde",
    "assinatura":    "Nexo — Instituto de Psicologia Aplicada em Americana/SP e Região",
}
_localidade = "Americana/SP e Região Metropolitana de Campinas"
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_dr_ricardo.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "Dr. Ricardo Vieira Ferreira",
    "especialidade": "Médico Urologista e Reposição Hormonal",
    "credenciais":   "CRM-SC 13164 | RQE Urologia 9029 | RQE Acupuntura 23022",
    "cidade":        "Jaraguá do Sul",
    "estado":        "SC",
    "bairro":        "",
    "servicos":      [
        "reposição hormonal masculina e feminina",
        "implantes hormonais",
        "tratamento urológico geral (andrologia, litíase renal, urologia feminina)",
        "saúde metabólica e controle de peso",
    ],
    "publico":       "homens e mulheres que buscam equilíbrio hormonal, melhora da disposição e envelhecimento saudável",
    "diferencial":   "médico urologista com mais de 35 anos de experiência, unindo urologia, acupuntura e medicina integrativa",
    "segmento":      "saúde",
    "assinatura":    "Dr. Ricardo Vieira Ferreira — Reposição Hormonal e Urologia em Jaraguá do Sul/SC | CRM-SC 13164 | RQE 9029",
}
_localidade = (CLIENTE["bairro"] + ", " if CLIENTE["bairro"] else "") + CLIENTE["cidade"] + "/" + CLIENTE["estado"]
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_dra_silvia.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "ITC Vertebral Jundiaí (Dra. Sílvia Canevari)",
    "especialidade": "Fisioterapia Especializada em Coluna Vertebral",
    "credenciais":   "CREFITO 8801-F",
    "cidade":        "Jundiaí",
    "estado":        "SP",
    "bairro":        "Jardim Brasil",
    "servicos":      [
        "tratamento não cirúrgico de hérnia de disco e dor ciática",
        "reabilitação de artrose, dor lombar e dor cervical",
        "programa de reconstrução músculo-articular (RMA da coluna)",
        "quiroprática e osteopatia",
    ],
    "publico":       "pessoas com dores, lesões ou patologias na coluna que buscam tratamentos eficazes e não invasivos",
    "diferencial":   "método exclusivo RMA (Reconstrução Músculo Articular), tecnologia avançada (mesas de tração eletrônicas) e direção da Dra. Sílvia Canevari",
    "segmento":      "saúde",
    "assinatura":    "ITC Vertebral Jundiaí — Fisioterapia Especializada na Coluna em Jundiaí/SP | CREFITO 8801-F",
}
_localidade = (CLIENTE["bairro"] + ", " if CLIENTE["bairro"] else "") + CLIENTE["cidade"] + "/" + CLIENTE["estado"]
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_dr_daniel.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "Dr. Daniel César Seguel Rebolledo",
    "especialidade": "Ortopedista e Traumatologista (Cirurgia do Quadril e Oncologia Ortopédica)",
    "credenciais":   "CRM-SP 104291 | RQE 10207",
    "cidade":        "São Paulo",
    "estado":        "SP",
    "bairro":        "",
    "servicos":      [
        "cirurgia do quadril (artroplastia/prótese de quadril)",
        "tratamento de tumores ósseos e de partes moles",
        "viscossuplementação e infiltrações no quadril",
        "artroscopia de quadril",
    ],
    "publico":       "pacientes com dores, lesões ou fraturas no quadril e pessoas com suspeita ou diagnóstico de tumores ósseos",
    "diferencial":   "dupla especialidade (Quadril e Oncologia Ortopédica), formado pela USP, aliando técnicas cirúrgicas modernas a atendimento humanizado",
    "segmento":      "saúde",
    "assinatura":    "Dr. Daniel César Seguel Rebolledo — Cirurgia do Quadril e Oncologia Ortopédica | CRM-SP 104291 | RQE 10207",
}
_localidade = "São Paulo/SP e Grande ABC"
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_emmen.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "Dra. Emmen Rocha",
    "especialidade": "Ginecologista e Obstetra",
    "credenciais":   "CRM-MG 72484 | RQE 53688",
    "cidade":        "Lavras",
    "estado":        "MG",
    "bairro":        "",
    "servicos":      [
        "parto humanizado e respeitoso",
        "pré-natal de risco habitual e alto risco",
        "colocação de DIU e implantes contraceptivos (Implanon)",
        "tratamento de endometriose",
        "cirurgias ginecológicas",
    ],
    "publico":       "mulheres em busca de saúde reprodutiva, métodos contraceptivos seguros e pré-natal ou parto humanizado",
    "diferencial":   "atendimento humanizado focado na autonomia da mulher, especialista em pré-natal de alto risco e parto humanizado respeitoso",
    "segmento":      "saúde",
    "assinatura":    "Dra. Emmen Rocha — Ginecologia e Obstetrícia em Lavras/MG | CRM-MG 72484 | RQE 53688",
}
_localidade = (CLIENTE["bairro"] + ", " if CLIENTE["bairro"] else "") + CLIENTE["cidade"] + "/" + CLIENTE["estado"]
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_nippo_dents.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "Nippo Dents Odontologia",
    "especialidade": "Clínica Odontológica",
    "credenciais":   "",
    "cidade":        "São Paulo",
    "estado":        "SP",
    "bairro":        "São Judas / Saúde",
    "servicos":      [
        "ortodontia geral e estética (Invisalign)",
        "implantes dentários e prótese protocolo",
        "odontologia miofuncional (Myobrace)",
        "harmonização orofacial",
        "sedação consciente para pacientes com fobia/medo",
    ],
    "publico":       "crianças, adultos e idosos em busca de cuidados odontológicos completos e especializados",
    "diferencial":   "mais de 25 anos de atuação, pioneira em odontologia miofuncional, sedação consciente para fobia e estrutura completa próximo ao metrô São Judas",
    "segmento":      "saúde",
    "assinatura":    "Nippo Dents Odontologia — Clínica Odontológica em São Paulo/SP",
}
_localidade = (CLIENTE["bairro"] + ", " if CLIENTE["bairro"] else "") + CLIENTE["cidade"] + "/" + CLIENTE["estado"]
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_dr_raimundo.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "Clínica Dr. Raimundo Nunes",
    "especialidade": "Ginecologista e Obstetra",
    "credenciais":   "CRM-SP 32658 | RQE 68794",
    "cidade":        "São Paulo",
    "estado":        "SP",
    "bairro":        "Bela Vista",
    "servicos":      [
        "inserção de DIU (Mirena, Kyleena, cobre e prata)",
        "colocação de Implanon",
        "pré-natal de alto e baixo risco",
        "acompanhamento de menopausa e climatério",
        "cirurgia ginecológica",
    ],
    "publico":       "mulheres em busca de métodos contraceptivos modernos e de longa duração, pré-natal especializado e cirurgias ginecológicas",
    "diferencial":   "clínica com mais de 30 anos de atuação em São Paulo, referência na colocação de DIU e Implanon com alto nível de resolutividade",
    "segmento":      "saúde",
    "assinatura":    "Clínica Dr. Raimundo Nunes — Ginecologia e Obstetrícia em São Paulo/SP | CRM-SP 32658 | RQE 68794",
}
_localidade = (CLIENTE["bairro"] + ", " if CLIENTE["bairro"] else "") + CLIENTE["cidade"] + "/" + CLIENTE["estado"]
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_moc_advogados.py": """\

# ── Configuração do cliente ───────────────────────────────────────────────────
CLIENTE = {
    "nome":          "MOC | Martins, Oliveira & Cruz Advogados",
    "especialidade": "Escritório de Advocacia",
    "credenciais":   "",
    "cidade":        "São José do Rio Preto",
    "estado":        "SP",
    "bairro":        "Jardim Maracanã",
    "servicos":      [
        "assessoria jurídica empresarial por assinatura",
        "planejamento tributário e recuperação de créditos",
        "defesa trabalhista para bancários",
        "planejamento previdenciário (INSS)",
        "negativas de planos de saúde",
    ],
    "publico":       "empresas em busca de gestão de risco jurídico e pessoas físicas em demandas trabalhistas, de saúde ou previdenciárias",
    "diferencial":   "suporte jurídico contemporâneo altamente especializado com atuação em São José do Rio Preto, Santos e Marília/SP",
    "segmento":      "jurídico",
    "assinatura":    "Martins, Oliveira & Cruz Advogados — Advocacia Contemporânea em São José do Rio Preto, Santos e Marília/SP",
}
_localidade = "São José do Rio Preto, Santos e Marília/SP"
_servicos_resumo = " | ".join(CLIENTE["servicos"][:4])
""",

"crew_people_partner.py": """\

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
""",

}

# ──────────────────────────────────────────────────────────────────────────────
# Substituições dinâmicas nos guidelines (mesmo texto em todos os arquivos)
# ──────────────────────────────────────────────────────────────────────────────
REPLACEMENTS = [
    (
        "inserir cidade/bairro/região do cliente de forma natural (mínimo 2 menções no corpo).",
        'inserir de forma natural "{_localidade}" no corpo do texto (mínimo 2 menções). Evitar repetição artificial.',
    ),
    (
        "mencionar como o tema se relaciona ao serviço/especialidade real do cliente.",
        "conectar o tema aos serviços reais do cliente — {_servicos_resumo}.",
    ),
    (
        "cidade/bairro/região do cliente aparecem de forma natural no corpo do texto (mínimo 2 ocorrências)?",
        '"{_localidade}" aparece de forma natural no corpo do texto (mínimo 2 ocorrências)?',
    ),
]

# ──────────────────────────────────────────────────────────────────────────────
# Processar arquivos
# ──────────────────────────────────────────────────────────────────────────────
for filename, bloco in BLOCOS.items():
    # Encontra o arquivo no diretório de crews
    filepath = None
    for dirpath, _, files in os.walk(ROOT):
        if filename in files:
            filepath = os.path.join(dirpath, filename)
            break

    if not filepath:
        print(f"ARQUIVO NÃO ENCONTRADO: {filename}")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 1. Inserir bloco CLIENTE após load_dotenv()
    anchor = "load_dotenv()\n"
    if anchor in content and "CLIENTE = {" not in content:
        content = content.replace(anchor, anchor + bloco, 1)

    # 2. Aplicar substituições dinâmicas
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"OK {filename}")
    else:
        print(f"~ {filename} (sem alteracao)")

print("\nConcluido.")

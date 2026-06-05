# -*- coding: utf-8 -*-
"""Dra. Ana Clara Cruz — Dermatologia Clínica, Estética e Cirúrgica (São Paulo/SP).

Catálogo de links internos: institucionais (Home, Tratamentos, Blog) + páginas-pilar
dos procedimentos principais. Posts secundários do blog foram omitidos para manter
o catálogo enxuto (12-14 itens recomendado).
"""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="dra_ana_clara",
    nome="Dra. Ana Clara Cruz",
    especialidade="Dermatologia Clínica, Estética e Cirúrgica",
    segmento="saude",
    dominio_oficial="draanaclaracruz.com.br",

    cidade="São Paulo",
    estado="SP",
    bairro="Vila Olímpia",
    credenciais="CRM-SP 218.598 | RQE 125.917",
    servicos=[
        "aplicação de toxina botulínica",
        "preenchimento com ácido hialurônico",
        "bioestimuladores de colágeno",
        "fios de PDO (lisos)",
        "microagulhamento",
        "peelings químicos",
    ],
    # publico: FALTA — não foi obtido do site
    diferencial="Dermatologia completa com ciência, empatia e sofisticação.",

    links_internos=[
        # ── Institucionais ───────────────────────────────────────────────────
        LinkInterno("Home — Dra. Ana Clara Cruz", "https://draanaclaracruz.com.br/",
                    "Dra. Ana Clara Cruz — dermatologista em São Paulo"),
        LinkInterno("Sobre — Dermatologista Especialista",
                    "https://draanaclaracruz.com.br/dermatologista-em-sao-paulo-especialista-em-dermatologia-clinica-estetica-e-cirurgica/",
                    "especialista em dermatologia clínica, estética e cirúrgica"),
        LinkInterno("Clínica na Vila Olímpia",
                    "https://draanaclaracruz.com.br/clinica-dermatologica-em-sao-paulo-cuidado-especializado-na-vila-olimpia/",
                    "clínica dermatológica especializada na Vila Olímpia"),
        LinkInterno("Tratamentos", "https://draanaclaracruz.com.br/tratamentos/",
                    "tratamentos dermatológicos disponíveis"),
        LinkInterno("Blog", "https://draanaclaracruz.com.br/blog/",
                    "conteúdos sobre saúde da pele e dermatologia"),

        # ── Páginas-pilar dos procedimentos ──────────────────────────────────
        LinkInterno("Toxina Botulínica — Quando começar",
                    "https://draanaclaracruz.com.br/toxina-botulinica-quando-comecar-e-como-funciona-o-tratamento/",
                    "tratamento com toxina botulínica"),
        LinkInterno("Preenchimento com Ácido Hialurônico",
                    "https://draanaclaracruz.com.br/preenchimento-com-acido-hialuronico-em-sao-paulo-guia-completo-para-resultados-naturais/",
                    "preenchimento com ácido hialurônico em São Paulo"),
        LinkInterno("Bioestimuladores de Colágeno",
                    "https://draanaclaracruz.com.br/bioestimuladores-de-colageno-qual-e-o-melhor-para-cada-tipo-de-flacidez/",
                    "bioestimuladores de colágeno para flacidez"),
        LinkInterno("Microagulhamento Facial",
                    "https://draanaclaracruz.com.br/microagulhamento-facial-renovacao-avancada-com-estimulo-de-colageno/",
                    "microagulhamento facial e estímulo de colágeno"),
        LinkInterno("Fios de PDO Lisos",
                    "https://draanaclaracruz.com.br/fios-de-pdo-lisos-rejuvenescimento-sutil-e-eficiente/",
                    "fios de PDO lisos para rejuvenescimento sutil"),
        LinkInterno("Ultraformer — Lifting sem cirurgia",
                    "https://draanaclaracruz.com.br/ultraformer-em-sao-paulo-lifting-sem-cirurgia-com-resultados-progressivos/",
                    "ultraformer e lifting sem cirurgia"),
        LinkInterno("Tratamento de Melasma",
                    "https://draanaclaracruz.com.br/tratamento-de-melasma-em-sao-paulo-o-que-realmente-funciona-para-clarear-as-manchas-da-pele/",
                    "tratamento de melasma em São Paulo"),
        LinkInterno("Manchas na Pele",
                    "https://draanaclaracruz.com.br/manchas-na-pele-principais-causas-e-tratamentos-mais-indicados/",
                    "causas e tratamentos para manchas na pele"),
        LinkInterno("Queda Capilar",
                    "https://draanaclaracruz.com.br/queda-capilar-causas-diagnostico-e-tratamentos-eficazes/",
                    "queda capilar: causas, diagnóstico e tratamentos"),
        LinkInterno("Procedimentos Dermatológicos Seguros",
                    "https://draanaclaracruz.com.br/procedimentos-dermatologicos-seguros-remocao-precisa-de-lesoes-e-cistos/",
                    "remoção precisa de lesões e cistos da pele"),
    ],
    whitelist_externos=[
        # Universal
        ".gov", ".gov.br", ".edu", ".edu.br",
        # Saúde — autoridades brasileiras
        "saude.gov.br", "anvisa.gov.br",
        # Conselho e sociedade da especialidade (confirmados pelo cliente)
        "cfm.org.br", "sbd.org.br",
        # Autoridades internacionais em dermatologia
        "who.int", "nih.gov", "ncbi.nlm.nih.gov", "medlineplus.gov",
        "aad.org", "dermnetnz.org",
        # SEO / técnicos
        "developers.google.com", "support.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
    ],

    whatsapp="https://wa.link/qu3dwh",
    enderecos=["R. Fidêncio Ramos, 160 – 8º Andar – Vila Olímpia – São Paulo/SP – CEP 04551-010"],
    assinatura="Dra. Ana Clara Cruz — Dermatologia Clínica, Estética e Cirúrgica em São Paulo/SP | CRM-SP 218.598 | RQE 125.917",
)

# -*- coding: utf-8 -*-
"""Clínica Dr. Raimundo Nunes — Ginecologia e Obstetrícia (São Paulo/SP).

Exemplo de cliente no modelo config-driven: apenas DADOS. O pipeline é compartilhado
(ver pipeline/builder.py). Para um cliente novo, copie este arquivo e ajuste os campos.
"""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="dr_raimundo",
    nome="Clínica Dr. Raimundo Nunes",
    especialidade="Ginecologia e Obstetrícia",
    segmento="saude",
    dominio_oficial="clinicadrraimundonunes.com.br",

    cidade="São Paulo",
    estado="SP",
    bairro="Bela Vista",
    credenciais="CRM-SP 32658 | RQE 68794",
    servicos=[
        "inserção de DIU (Mirena, Kyleena, cobre e prata)",
        "colocação de Implanon",
        "pré-natal de alto e baixo risco",
        "acompanhamento de menopausa e climatério",
        "cirurgia ginecológica",
    ],
    publico=(
        "mulheres em busca de métodos contraceptivos modernos e de longa duração, "
        "pré-natal especializado e cirurgias ginecológicas"
    ),
    diferencial=(
        "clínica com mais de 30 anos de atuação em São Paulo, referência na colocação "
        "de DIU e Implanon com alto nível de resolutividade"
    ),

    links_internos=[
        LinkInterno("Home — Clínica Dr. Raimundo Nunes", "https://clinicadrraimundonunes.com.br/",
                    "Clínica de Ginecologia e Obstetrícia Dr. Raimundo Nunes em São Paulo"),
        LinkInterno("Quem Somos", "https://clinicadrraimundonunes.com.br/quem-somos/",
                    "conheça a história e o compromisso com a saúde da mulher"),
        LinkInterno("Corpo Clínico", "https://clinicadrraimundonunes.com.br/corpo-clinico/",
                    "equipe de ginecologistas e obstetras especialistas"),
        LinkInterno("DIU e Implanon — Dúvidas Frequentes", "https://clinicadrraimundonunes.com.br/diu-e-implanon/",
                    "perguntas frequentes sobre DIU e Implanon em São Paulo"),
        LinkInterno("DIU Mirena", "https://clinicadrraimundonunes.com.br/diu-mirena/",
                    "vantagens, eficácia e indicações do DIU hormonal Mirena"),
        LinkInterno("Pré-natal — Orientações Parte 1", "https://clinicadrraimundonunes.com.br/pre-natal-1/",
                    "dúvidas e exames no acompanhamento pré-natal"),
        LinkInterno("Pré-natal — Orientações Parte 2", "https://clinicadrraimundonunes.com.br/pre-natal-2/",
                    "orientações médicas sobre as fases do pré-natal"),
        LinkInterno("Gestação — Primeira Fase", "https://clinicadrraimundonunes.com.br/gestacao-1/",
                    "mudanças no corpo e desenvolvimento do bebê na gestação"),
        LinkInterno("Parto", "https://clinicadrraimundonunes.com.br/parto/",
                    "tipos de parto e plano de parto ideal"),
        LinkInterno("Pós-parto", "https://clinicadrraimundonunes.com.br/pos-parto/",
                    "cuidados com a saúde da mulher no pós-parto"),
        LinkInterno("Cirurgia Ginecológica", "https://clinicadrraimundonunes.com.br/cirurgia/",
                    "como funciona a cirurgia ginecológica e a laparoscopia"),
        LinkInterno("Publicações e Blog", "https://clinicadrraimundonunes.com.br/publicacoes/",
                    "artigos informativos sobre ginecologia e saúde da mulher"),
        LinkInterno("Contato e Agendamento", "https://clinicadrraimundonunes.com.br/contato/",
                    "agende sua consulta com a equipe da clínica"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "saude.gov.br", "anvisa.gov.br", "who.int", "nih.gov",
        "cfm.org.br", "febrasgo.org.br", "inca.gov.br", "sbra.com.br",
        "endometriose.org.br",
        "developers.google.com", "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
    ],

    whatsapp="https://wa.me/5511973071245?text=Gostaria%20de%20tirar%20uma%20dúvida%20e%20marcar%20uma%20consulta",
    enderecos=[
        "Unidade Bela Vista: Rua Itapeva, 490 – 5º Andar, Cj. 51 – São Paulo/SP | (11) 3251-1245",
        "Unidade Itaim Bibi: Rua Joaquim Floriano, 940 – Cj. 41 – São Paulo/SP",
    ],
    assinatura="Clínica Dr. Raimundo Nunes — Ginecologia e Obstetrícia em São Paulo/SP | CRM-SP 32658 | RQE 68794",
    assinatura_intro=(
        "Para esclarecer dúvidas ou avaliar a melhor conduta para o seu caso, "
        "a equipe da clínica está à disposição."
    ),

    target_palavras=(1300, 1600),
    teto_palavras=1800,
)

# -*- coding: utf-8 -*-
"""Instituto Nexo — Psicologia Aplicada e Saúde Mental (Americana/SP)."""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="clinicas_nexo",
    nome="Nexo — Instituto de Psicologia Aplicada",
    especialidade="Psicologia e Saúde Mental",
    segmento="saude",
    dominio_oficial="vivanexo.com.br",

    cidade="Americana",
    estado="SP",
    servicos=[
        "psicoterapia individual (infantil, adolescentes, adultos e idosos)",
        "atendimento especializado em TEA/ABA",
        "avaliação neuropsicológica",
        "fonoaudiologia e terapia ocupacional",
        "parcerias corporativas de saúde mental",
    ],
    publico="crianças, adolescentes, adultos, idosos, pessoas com TEA/TDAH, empresas e profissionais da psicologia",
    diferencial="referência em intervenção ABA para autismo e atendimento multidisciplinar integrado no interior de SP (Americana, Campinas, Piracicaba)",

    links_internos=[
        LinkInterno("Home — Instituto Nexo", "https://vivanexo.com.br/",
                    "Instituto Nexo de Psicologia Aplicada"),
        LinkInterno("O Nexo — Sobre o Instituto", "https://vivanexo.com.br/o-nexo/",
                    "conheça a missão e os valores do Instituto Nexo"),
        LinkInterno("Psicoterapia Individual", "https://vivanexo.com.br/servico/psicoterapia-individual/",
                    "psicoterapia para crianças, adultos e idosos"),
        LinkInterno("Terapia ABA para TEA", "https://vivanexo.com.br/servico/psicoterapia-aba/",
                    "terapia ABA para pessoas com autismo"),
        LinkInterno("Avaliação Neuropsicológica", "https://vivanexo.com.br/servico/avaliacao-neuropsicologica/",
                    "avaliação neuropsicológica completa"),
        LinkInterno("Socialização TEA", "https://vivanexo.com.br/servico/socializacao/",
                    "grupos de socialização para pessoas com TEA"),
        LinkInterno("Atividades da Vida Diária (AVD/AIVD)",
                    "https://vivanexo.com.br/servico/atividade-da-vida-diaria-avd-e-atividade-instrumental-da-vida-diaria-aivd/",
                    "desenvolvimento de habilidades para a vida diária"),
        LinkInterno("Notícias e Blog", "https://vivanexo.com.br/noticias/",
                    "conteúdos sobre saúde mental e psicologia"),
        LinkInterno("Unidades", "https://vivanexo.com.br/unidades/",
                    "encontre uma unidade Nexo perto de você"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "saude.gov.br", "who.int", "nih.gov",
        "cfp.org.br", "crp.org.br",
        "autismo.org.br", "ama.org.br", "abda.org.br",
        "developers.google.com", "support.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
    ],

    whatsapp="https://api.whatsapp.com/send/?phone=551934065984&text=Oi!%20Encontrei%20o%20Instituto%20Nexo%20no%20Google%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es.&type=phone_number&app_absent=0",
    enderecos=["Rua Dom Pedro II, 1169 – Conserva – Americana/SP"],   # demais 7 unidades não estavam detalhadas no site
    assinatura="Nexo — Instituto de Psicologia Aplicada em Americana/SP e Região",
)

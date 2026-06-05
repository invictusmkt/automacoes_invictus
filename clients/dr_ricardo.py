# -*- coding: utf-8 -*-
"""Dr. Ricardo Vieira Ferreira — Urologia e Reposição Hormonal (Jaraguá do Sul/SC)."""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="dr_ricardo",
    nome="Dr. Ricardo Vieira Ferreira",
    especialidade="Urologia e Reposição Hormonal",
    segmento="saude",
    dominio_oficial="drricardoferreira.com.br",

    cidade="Jaraguá do Sul",
    estado="SC",
    bairro="Centro",
    credenciais="CRM-SC 13164 | RQE Urologia 9029 | RQE Acupuntura 23022",
    servicos=[
        "reposição hormonal masculina e feminina",
        "implantes hormonais",
        "tratamento urológico geral (andrologia, litíase renal, urologia feminina)",
        "saúde metabólica e controle de peso",
    ],
    publico="homens e mulheres que buscam equilíbrio hormonal, melhora da disposição e envelhecimento saudável",
    diferencial="médico urologista com mais de 35 anos de experiência, unindo urologia, acupuntura e medicina integrativa",

    links_internos=[
        LinkInterno("Home — Dr. Ricardo Vieira Ferreira", "https://drricardoferreira.com.br/",
                    "Dr. Ricardo Vieira Ferreira — urologista em Jaraguá do Sul"),
        LinkInterno("Sobre o Dr. Ricardo", "https://drricardoferreira.com.br/sobre/",
                    "trajetória e formação do Dr. Ricardo Vieira Ferreira"),
        LinkInterno("Contato e Agendamento", "https://drricardoferreira.com.br/contato/",
                    "agende sua consulta particular com o Dr. Ricardo"),
        LinkInterno("Blog — Saúde Hormonal e Qualidade de Vida", "https://drricardoferreira.com.br/blog",
                    "artigos sobre saúde hormonal e envelhecimento saudável"),
        LinkInterno("7 Sinais de Testosterona Baixa em Homens",
                    "https://drricardoferreira.com.br/7-sinais-de-testosterona-baixa-em-homens-quando-procurar-avaliacao-medica/",
                    "os principais sinais de testosterona baixa em homens"),
        LinkInterno("Massa Muscular e Hormônios",
                    "https://drricardoferreira.com.br/massa-muscular-e-hormonios-qual-a-relacao-e-quando-investigar/",
                    "relação entre perda de massa muscular e desequilíbrio hormonal"),
        LinkInterno("Perda de Ereção Frequente — Quando Investigar",
                    "https://drricardoferreira.com.br/perda-de-erecao-frequente-quando-investigar/",
                    "quando investigar clinicamente a perda de ereção frequente"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "saude.gov.br", "anvisa.gov.br", "who.int", "nih.gov",
        "cfm.org.br", "sbu.org.br", "sbem.org.br", "febrasgo.org.br",
        "developers.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
    ],

    whatsapp="https://api.whatsapp.com/send?phone=5547999556456&text=Ol%C3%A1!%20Vim%20do%20site%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es.",
    enderecos=["Av. Mal. Deodoro da Fonseca, 1188 – Salas 208 e 209 – Centro – Jaraguá do Sul/SC – CEP 89251-702"],
    assinatura="Dr. Ricardo Vieira Ferreira — Reposição Hormonal e Urologia em Jaraguá do Sul/SC | CRM-SC 13164 | RQE 9029",
)

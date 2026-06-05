# -*- coding: utf-8 -*-
"""Clínica Dra. Catarine Padoveze — Dermatologia Estética e Nutrologia (Santo André/SP).

Dados parciais — o crew legado não tinha dicionário CLIENTE estruturado.
Campos sem fonte explícita ficaram vazios (não foram inventados).
"""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="dra_catarine",
    nome="Clínica Dra. Catarine Padoveze",
    especialidade="Dermatologia Estética e Nutrologia",
    segmento="saude",
    dominio_oficial="dracatarinepadoveze.com.br",

    cidade="Santo André",
    estado="SP",
    # bairro, credenciais, servicos, publico, diferencial: FALTA — preencher manualmente

    links_internos=[
        LinkInterno("Home — Clínica Dra. Catarine Padoveze", "https://dracatarinepadoveze.com.br/",
                    "clínica boutique de dermatologia estética em Santo André"),
        LinkInterno("Alimentação e pele — Frutas e vegetais",
                    "https://dracatarinepadoveze.com.br/voce-e-o-que-voce-come-comer-frutas-e-vegetais-deixa-a-pele-mais-bonita/",
                    "impacto da alimentação na qualidade da pele"),
        LinkInterno("Pele madura — Cuidados essenciais",
                    "https://dracatarinepadoveze.com.br/pele-madura/",
                    "cuidados essenciais para pele madura"),
        LinkInterno("Sono e saúde da pele",
                    "https://dracatarinepadoveze.com.br/voce-dorme-bem-descubra-por-que-o-sono-e-a-chave-para-sua-saude/",
                    "importância do sono para a saúde da pele"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "saude.gov.br", "anvisa.gov.br", "who.int", "nih.gov",
        "sbd.org.br",
        "developers.google.com", "support.google.com", "search.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
    ],

    whatsapp="https://api.whatsapp.com/send/?phone=%2B5511971996599&text&type=phone_number&app_absent=0",
    enderecos=[],   # FALTA no crew legado — preencher manualmente
    assinatura="Clínica Dra. Catarine Padoveze — Dermatologia Estética e Nutrologia em Santo André/SP (ABC Paulista)",
)

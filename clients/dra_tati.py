# -*- coding: utf-8 -*-
"""Dra. Tatiana Villas Boas Gabbi — Dermatologia (São Paulo/SP)."""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="dra_tati",
    nome="Dra. Tatiana Villas Boas Gabbi",
    especialidade="Dermatologia",
    segmento="saude",
    dominio_oficial="tatianagabbi.com.br",

    cidade="São Paulo",
    estado="SP",
    bairro="Itaim Bibi",
    credenciais="CRM-SP 104415 | RQE 31137",
    servicos=[
        "tratamento de doenças das unhas (onicopatias)",
        "queda de cabelo (tricologia)",
        "tratamentos dermatológicos para pele",
        "cirurgia ungueal",
    ],
    publico="pessoas com patologias de unhas, cabelos e pele em busca de diagnóstico e tratamento especializado",
    diferencial="referência nacional e internacional em doenças das unhas (onicopatias), formada pela USP e membro da European Nail Society",

    links_internos=[
        LinkInterno("Home", "https://tatianagabbi.com.br",
                    "Dermatologia com foco em doenças das unhas em São Paulo"),
        LinkInterno("Sobre a Dra. Tatiana Gabbi", "https://tatianagabbi.com.br/sobre",
                    "saiba mais sobre a Dra. Tatiana Gabbi"),
        LinkInterno("Unhas Encravadas", "https://tatianagabbi.com.br/unhas-encravadas",
                    "tratamento para unhas encravadas"),
        LinkInterno("Unhas Irregulares", "https://tatianagabbi.com.br/unhas-irregulares",
                    "tratamento para unhas irregulares"),
        LinkInterno("Melanoníquia", "https://tatianagabbi.com.br/melanoniquia/",
                    "entenda o que é melanoníquia e como tratar"),
        LinkInterno("Unhas Fracas", "https://tatianagabbi.com.br/unhas-fracas/",
                    "tratamento para unhas fracas"),
        LinkInterno("Unhas Saudáveis", "https://tatianagabbi.com.br/unhas-saudaveis/",
                    "como manter unhas saudáveis"),
        LinkInterno("Detox das Unhas", "https://tatianagabbi.com.br/detox-das-unhas/",
                    "detox das unhas: benefícios e cuidados"),
        LinkInterno("Bases Fortalecedoras", "https://tatianagabbi.com.br/bases-fortalecedoras/",
                    "melhores bases fortalecedoras para unhas"),
        LinkInterno("Blog", "https://tatianagabbi.com.br/blog",
                    "leia mais artigos no blog da Dra. Tatiana Gabbi"),
        LinkInterno("Contato", "https://tatianagabbi.com.br/contato",
                    "entre em contato com a Dra. Tatiana Gabbi"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "sbd.org.br", "aad.org", "who.int", "nhs.uk", "cdc.gov",
        "nih.gov", "ncbi.nlm.nih.gov", "medlineplus.gov",
        "cochranelibrary.com", "dermnetnz.org",
        "schema.org", "w3.org", "developers.google.com", "support.google.com",
    ],

    whatsapp="https://api.whatsapp.com/send?phone=5511991578420&text=Oi!%20Encontrei%20seu%20contato%20no%20site%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es",
    enderecos=[],   # endereço não estava na assinatura do crew legado
    assinatura="Dra. Tatiana Villas Boas Gabbi — Dermatologista em São Paulo/SP | CRM-SP 104415 | RQE 31137",
    cta_whatsapp_label="Agende sua consulta via WhatsApp para avaliação especializada",
)

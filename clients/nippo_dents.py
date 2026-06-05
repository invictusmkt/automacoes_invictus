# -*- coding: utf-8 -*-
"""Nippo Dents — Clínica Odontológica (São Paulo/SP, próximo ao metrô São Judas)."""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="nippo_dents",
    nome="Nippo Dents Odontologia",
    especialidade="Odontologia",
    segmento="odonto",
    dominio_oficial="nippodents.com.br",

    cidade="São Paulo",
    estado="SP",
    bairro="Saúde (próximo ao metrô São Judas)",
    servicos=[
        "ortodontia geral e estética (Invisalign)",
        "implantes dentários e prótese protocolo",
        "odontologia miofuncional (Myobrace)",
        "harmonização orofacial",
        "sedação consciente para pacientes com fobia",
    ],
    publico="crianças, adultos e idosos em busca de cuidados odontológicos completos e especializados",
    diferencial="mais de 25 anos de atuação, pioneira em odontologia miofuncional, sedação consciente para fobia e estrutura completa próximo ao metrô São Judas",

    links_internos=[
        LinkInterno("Home — Nippodents", "https://nippodents.com.br/",
                    "clínica odontológica Nippodents na Zona Sul de São Paulo"),
        LinkInterno("A Clínica", "https://nippodents.com.br/clinica-odontologica/",
                    "conheça a clínica Nippodents"),
        LinkInterno("Tratamentos Odontológicos", "https://nippodents.com.br/tratamentos-odontologicos/",
                    "tratamentos odontológicos especializados"),
        LinkInterno("Clínico Geral", "https://nippodents.com.br/clinico-geral-odontologia/",
                    "atendimento odontológico clínico geral"),
        LinkInterno("Implantes Dentários", "https://nippodents.com.br/clinica-implantes-dentarios/",
                    "implantes dentários na Zona Sul de SP"),
        LinkInterno("Próteses Dentárias", "https://nippodents.com.br/clinica-proteses-dentarias/",
                    "próteses dentárias com tecnologia digital"),
        LinkInterno("Lentes de Contato Dental", "https://nippodents.com.br/lentes-de-contato-dental-sao-paulo/",
                    "lentes de contato dental em São Paulo"),
        LinkInterno("Ortodontia", "https://nippodents.com.br/clinica-ortodontia/",
                    "tratamento ortodôntico personalizado"),
        LinkInterno("Check-up Odontológico Digital", "https://nippodents.com.br/clinica-check-up-odontologico-digital/",
                    "check-up odontológico digital completo"),
        LinkInterno("Periodontia", "https://nippodents.com.br/clinica-periodontia/",
                    "tratamento periodontal especializado"),
        LinkInterno("Endodontia", "https://nippodents.com.br/clinica-endodontia/",
                    "endodontia e tratamento de canal"),
        LinkInterno("Odontopediatria", "https://nippodents.com.br/clinica-de-odontopediatria/",
                    "odontopediatria para crianças"),
        LinkInterno("Tratamento Miofuncional", "https://nippodents.com.br/clinica-tratamento-miofuncional/",
                    "terapia miofuncional oral"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "saude.gov.br", "anvisa.gov.br", "who.int", "nih.gov",
        "cfo.org.br", "cro.org.br",
        "developers.google.com", "support.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
    ],

    whatsapp="https://api.whatsapp.com/send/?phone=5511963263528&text=Oi!%20Encontrei%20a%20Nippodents%20no%20Google%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es.&type=phone_number&app_absent=0",
    enderecos=[],   # FALTA no crew legado — preencher manualmente
    assinatura="Nippo Dents Odontologia — Clínica Odontológica em São Paulo/SP",
)

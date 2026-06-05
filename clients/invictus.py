# -*- coding: utf-8 -*-
"""Invictus Marketing — Agência de Marketing Digital (São Paulo/SP)."""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="invictus",
    nome="Invictus Marketing",
    especialidade="Marketing Digital",
    segmento="marketing",
    dominio_oficial="invictusmarketing.com.br",

    cidade="São Paulo",
    estado="SP",
    bairro="Casa Verde",
    servicos=[
        "Business Intelligence",
        "tráfego pago",
        "SEO",
        "otimização do Google Meu Negócio",
    ],

    links_internos=[
        LinkInterno("Quem Somos", "https://invictusmarketing.com.br/quem-somos",
                    "conheça mais sobre a Invictus Marketing"),
        LinkInterno("Serviços", "https://invictusmarketing.com.br/servicos",
                    "nossos serviços de marketing digital"),
        LinkInterno("Blog", "https://invictusmarketing.com.br/blog",
                    "conteúdos e dicas de marketing no blog da Invictus"),
        LinkInterno("Contato", "https://invictusmarketing.com.br/contato",
                    "fale com especialistas da Invictus Marketing"),
        LinkInterno("Business Intelligence", "https://invictusmarketing.com.br/business-intelligence",
                    "soluções de Business Intelligence para seu negócio"),
        LinkInterno("Tráfego Pago", "https://invictusmarketing.com.br/trafego-pago",
                    "estratégias de tráfego pago para aumentar conversões"),
        LinkInterno("SEO", "https://invictusmarketing.com.br/seo",
                    "melhores práticas de SEO para seu site"),
        LinkInterno("Google Meu Negócio", "https://invictusmarketing.com.br/google-meu-negocio",
                    "otimização do Google Meu Negócio para atrair clientes"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "developers.google.com", "support.google.com", "search.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
        "who.int", "oecd.org", "unesco.org", "iso.org", "data.gov",
    ],

    whatsapp="https://api.whatsapp.com/send?phone=5511947974924&text=Oi!%20Encontrei%20seu%20site%20no%20Google%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es.",
    enderecos=["Av. Casa Verde, 751 – São Paulo/SP"],
    assinatura="Invictus Marketing",
    cta_whatsapp_label="Fale conosco pelo WhatsApp",
    assinatura_intro="Quer impulsionar sua marca? A equipe da Invictus está pronta para conversar.",
)

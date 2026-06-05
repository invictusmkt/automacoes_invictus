# -*- coding: utf-8 -*-
"""Núcleo Rural — Suplementação e Nutrição Animal (São José do Rio Preto/SP)."""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="nucleo_rural",
    nome="Núcleo Rural",
    especialidade="Suplementação e Nutrição Animal",
    segmento="agronegocio",
    dominio_oficial="nucleorural.com.br",

    cidade="São José do Rio Preto",
    estado="SP",
    servicos=[
        "suplementos minerais para gado de corte",
        "suplementos minerais para gado de leite",
        "nutracêuticos para saúde animal",
    ],
    publico="pecuaristas, produtores rurais e criadores de gado de corte e leite",
    diferencial="soluções de alta tecnologia em suplementação e nutrição animal para aumento de produtividade no campo",

    links_internos=[
        LinkInterno("Home — Núcleo Rural", "https://nucleorural.com.br/",
                    "soluções completas para produtividade no campo"),
        LinkInterno("Sobre Nós", "https://nucleorural.com.br/#sobrenos",
                    "conheça a história e a missão da Núcleo Rural"),
        LinkInterno("Soluções", "https://nucleorural.com.br/#solucoes",
                    "soluções para sanidade do rebanho e alta performance"),
        LinkInterno("Blog", "https://nucleorural.com.br/blog/",
                    "insights práticos de manejo e produtividade no blog"),
        LinkInterno("Contato", "https://nucleorural.com.br/contato/",
                    "fale com especialistas da Núcleo Rural"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "embrapa.br", "agricultura.gov.br", "mapa.gov.br",
        "developers.google.com", "support.google.com", "search.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
        "who.int", "oecd.org", "unesco.org", "iso.org", "data.gov",
    ],

    whatsapp="https://api.whatsapp.com/send?phone=551735139264&text=Oi!%20Encontrei%20seu%20site%20no%20Google%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es.",
    enderecos=[],   # endereço não estava no crew legado — preencher manualmente se desejar
    assinatura="Núcleo Rural — Suplementação e Nutrição Animal em São José do Rio Preto/SP",
)

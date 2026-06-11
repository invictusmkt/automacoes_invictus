# -*- coding: utf-8 -*-
"""Pousada Mazé — hospitalidade familiar à beira-mar (Itanhaém/SP).

Cliente no modelo config-driven: apenas DADOS. O pipeline é compartilhado
(ver pipeline/builder.py). Segmento comercial (não regulado) → tom persuasivo.
"""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="pousada_maze",
    nome="Pousada Mazé",
    especialidade="hospitalidade familiar à beira-mar",
    segmento="comercial",
    dominio_oficial="pousadamaze.com.br",

    cidade="Itanhaém",
    estado="SP",
    bairro="Cibratel",
    servicos=[
        "café da manhã caseiro",
        "acesso pé na areia",
        "WiFi gratuito",
        "área de lazer refrescante",
        "área gourmet",
        "segurança total",
    ],
    publico=(
        "famílias e casais que buscam conforto, simplicidade e momentos "
        "inesquecíveis perto do mar"
    ),
    diferencial=(
        "experiência de hospitalidade familiar à beira-mar em Itanhaém, "
        "no bairro de Cibratel, desde 2025"
    ),

    links_internos=[
        LinkInterno("Home — Pousada Mazé", "https://pousadamaze.com.br/",
                    "página inicial da pousada"),
        LinkInterno("Sobre Nós", "https://pousadamaze.com.br/sobre-nos/",
                    "conheça nossa história e refúgio"),
        LinkInterno("Blog", "https://pousadamaze.com.br/blog/",
                    "guia de descanso no litoral"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br",
        "itanhaem.sp.gov.br", "turismosp.com.br", "gov.br",
        "developers.google.com", "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
    ],

    whatsapp="https://wa.link/xwl8kg",
    enderecos=[
        "R. Profa. Dalva Dati Ruivo, 70 – Cibratel – Itanhaém/SP – CEP 11746-274",
    ],
    assinatura="Pousada Mazé — Hospitalidade familiar à beira-mar em Itanhaém/SP",
    assinatura_intro=(
        "Para conhecer a pousada, tirar dúvidas ou garantir sua reserva, "
        "a nossa equipe está à disposição."
    ),
    cta_whatsapp_label="Reserve sua estadia pelo WhatsApp",
    # target_palavras / teto_palavras herdados do default (700-850, teto 900)
)

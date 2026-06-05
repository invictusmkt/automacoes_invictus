# -*- coding: utf-8 -*-
"""ITC Vertebral Jundiaí (Dra. Sílvia Canevari) — Fisioterapia da Coluna (Jundiaí/SP)."""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="dra_silvia",
    nome="ITC Vertebral Jundiaí (Dra. Sílvia Canevari)",
    especialidade="Fisioterapia Especializada em Coluna Vertebral",
    segmento="saude",
    dominio_oficial="itcvertebraljundiai.com.br",

    cidade="Jundiaí",
    estado="SP",
    bairro="Jardim Brasil",
    credenciais="CREFITO 8801-F",
    servicos=[
        "tratamento não cirúrgico de hérnia de disco e dor ciática",
        "reabilitação de artrose, dor lombar e dor cervical",
        "programa de reconstrução músculo-articular (RMA da coluna)",
        "quiroprática e osteopatia",
    ],
    publico="pessoas com dores, lesões ou patologias na coluna que buscam tratamentos eficazes e não invasivos",
    diferencial="método exclusivo RMA (Reconstrução Músculo Articular), tecnologia avançada (mesas de tração eletrônicas) e direção da Dra. Sílvia Canevari",

    links_internos=[
        LinkInterno("Home — ITC Vertebral Jundiaí", "https://www.itcvertebraljundiai.com.br/viva-sem-dor/",
                    "fisioterapia especializada em coluna em Jundiaí"),
        LinkInterno("Sobre Nós", "https://www.itcvertebraljundiai.com.br/sobre-nos/",
                    "conheça a equipe do ITC Vertebral Jundiaí"),
        LinkInterno("Nossos Tratamentos", "https://www.itcvertebraljundiai.com.br/nossos-tratamentos/",
                    "tratamentos especializados para coluna vertebral"),
        LinkInterno("Blog", "https://www.itcvertebraljundiai.com.br/blog/",
                    "artigos sobre saúde da coluna e fisioterapia"),
        LinkInterno("Contato", "https://www.itcvertebraljundiai.com.br/contato/",
                    "agende sua avaliação no ITC Vertebral Jundiaí"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "saude.gov.br", "who.int", "nih.gov",
        "coffito.gov.br", "crefito.org.br",
        "developers.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
    ],

    whatsapp="https://wa.link/f1zyei",
    enderecos=["R. São Lázaro, 197 – Jardim Brasil – Jundiaí/SP"],
    assinatura="ITC Vertebral Jundiaí — Fisioterapia Especializada na Coluna em Jundiaí/SP | CREFITO 8801-F",
)

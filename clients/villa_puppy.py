# -*- coding: utf-8 -*-
"""Villa Puppy — Pet Shop, Clínica Veterinária e Estética Pet (São Paulo/SP)."""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="villa_puppy",
    nome="Villa Puppy",
    especialidade="Pet Shop, Clínica Veterinária e Estética Pet",
    segmento="veterinaria",
    dominio_oficial="villapuppy.com.br",

    cidade="São Paulo",
    estado="SP",
    bairro="Alto de Pinheiros",
    servicos=[
        "estética pet (Puppy Spa - banho e tosa)",
        "consultas veterinárias",
        "venda de rações super premium e acessórios",
        "venda de filhotes selecionados com pedigree",
    ],
    publico="tutores de cães e gatos em busca de serviços de estética, saúde animal de alto padrão e filhotes selecionados",
    diferencial="estética pet com produtos hipoalergênicos e veganos, localizada no Shopping VillaLobos com estrutura integrada",

    links_internos=[
        LinkInterno("Home — Villa Puppy", "https://villapuppy.com.br/#home",
                    "conheça a Villa Puppy Pet Shop no Shopping VillaLobos"),
        LinkInterno("Posicionamento", "https://villapuppy.com.br/#posicionamento",
                    "nossa filosofia de carinho e cuidado com os pets"),
        LinkInterno("Serviços", "https://villapuppy.com.br/#servicos",
                    "banho e tosa, clínica veterinária e muito mais"),
        LinkInterno("Marcas", "https://villapuppy.com.br/#marcas",
                    "marcas de ração e acessórios que trabalhamos"),
        LinkInterno("Depoimentos", "https://villapuppy.com.br/#depoimentos",
                    "o que os tutores dizem sobre a Villa Puppy"),
        LinkInterno("Localização", "https://villapuppy.com.br/#localizacao",
                    "como chegar na nossa loja no Shopping VillaLobos"),
        LinkInterno("Propósito", "https://villapuppy.com.br/#proposito",
                    "nosso propósito de cuidado e bem-estar animal"),
        LinkInterno("Contato", "https://villapuppy.com.br/#contato",
                    "fale com a equipe da Villa Puppy"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "crmv.org.br", "crmvsp.gov.br", "saude.sp.gov.br",
        "who.int", "oie.int", "mapa.gov.br", "agricultura.gov.br",
        "developers.google.com", "support.google.com", "search.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
        "oecd.org", "iso.org", "data.gov",
    ],

    whatsapp="https://api.whatsapp.com/send?phone=5511917411212&text=Ol%C3%A1,%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es%20sobre%20a%20Villa%20Puppy",
    enderecos=["Shopping VillaLobos: Av. Dra. Ruth Cardoso, 4777 – Jardim Universidade Pinheiros – São Paulo/SP"],
    assinatura="Villa Puppy — Pet Shop, Clínica Veterinária e Estética Pet em Alto de Pinheiros, São Paulo/SP",
)

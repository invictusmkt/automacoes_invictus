# -*- coding: utf-8 -*-
"""MOC — Martins, Oliveira & Cruz Advogados (São José do Rio Preto/SP)."""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="moc_advogados",
    nome="MOC | Martins, Oliveira & Cruz Advogados",
    especialidade="Advocacia (Empresarial, Tributária, Trabalhista, Previdenciária)",
    segmento="juridico",
    dominio_oficial="mocadvogados.com.br",

    cidade="São José do Rio Preto",
    estado="SP",
    bairro="Jardim Maracanã",
    servicos=[
        "assessoria jurídica empresarial por assinatura",
        "planejamento tributário e recuperação de créditos",
        "defesa trabalhista para bancários",
        "planejamento previdenciário (INSS)",
        "negativas de planos de saúde",
    ],
    publico="empresas em busca de gestão de risco jurídico e pessoas físicas em demandas trabalhistas, de saúde ou previdenciárias",
    diferencial="suporte jurídico contemporâneo altamente especializado com atuação em São José do Rio Preto, Santos e Marília/SP",

    links_internos=[
        LinkInterno("Home — MOC Advogados", "https://mocadvogados.com.br/moc-2/",
                    "escritório de advocacia MOC Advogados"),
        LinkInterno("Sobre Nós", "https://mocadvogados.com.br/sobre-nos/",
                    "conheça a equipe e o método MOC"),
        LinkInterno("Para Empresas", "https://mocadvogados.com.br/para-empresas/",
                    "soluções jurídicas para empresas"),
        LinkInterno("Para Você", "https://mocadvogados.com.br/para-voce/",
                    "assessoria jurídica para pessoas físicas"),
        LinkInterno("Direito Tributário", "https://mocadvogados.com.br/direito-tributario/",
                    "consultoria em direito tributário"),
        LinkInterno("Direito Trabalhista e Bancário", "https://mocadvogados.com.br/trabalhista-bancario/",
                    "assessoria trabalhista e bancária"),
        LinkInterno("Direito Previdenciário", "https://mocadvogados.com.br/direito-previdenciario/",
                    "planejamento e direito previdenciário"),
        LinkInterno("Direito Civil", "https://mocadvogados.com.br/civel-contencioso-e-consultivo/",
                    "direito civil contencioso e consultivo"),
        LinkInterno("Planos de Saúde", "https://mocadvogados.com.br/bariatrica/",
                    "direitos em planos de saúde"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "planalto.gov.br", "stj.jus.br", "stf.jus.br", "tst.jus.br", "trf.jus.br",
        "oab.org.br", "cfp.org.br",
        "receita.fazenda.gov.br", "previdencia.gov.br",
        "developers.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
    ],

    whatsapp="https://api.whatsapp.com/send/?phone=5517996611109&text=Oi!%20Encontrei%20a%20MOC%20Advogados%20no%20Google%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es.&type=phone_number&app_absent=0",
    enderecos=[
        "São José do Rio Preto: Edifício Onix Center Sul, R. Antônio José Martins Filho, 300 – Salas 122/123 – Jd. Maracanã – São José do Rio Preto/SP",
        "Marília: Complexo Empresarial Villas Boas, Av. das Esmeraldas, 821 – Sala 707 – Jd. Tangará – Marília/SP",
        "Santos: R. Luís de Camões, 212 – Vila Mathias – Santos/SP",
    ],
    assinatura="Martins, Oliveira & Cruz Advogados — Advocacia Contemporânea em São José do Rio Preto, Santos e Marília/SP",
)

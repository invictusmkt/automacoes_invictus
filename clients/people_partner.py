# -*- coding: utf-8 -*-
"""People Partner — Consultoria de RH e Gestão de Pessoas (Belo Horizonte/MG)."""
from core.models import ClientConfig, LinkInterno

CONFIG = ClientConfig(
    slug="people_partner",
    nome="People Partner",
    especialidade="Consultoria de Recursos Humanos e Gestão de Pessoas",
    segmento="corporativo",
    dominio_oficial="peoplepartner.com.br",

    cidade="Belo Horizonte",
    estado="MG",
    servicos=[
        "HR as a Service (RH como serviço)",
        "estruturação e aprimoramento de processos internos de RH",
        "recrutamento e seleção de talentos",
        "programas de mentoria corporativa e individual",
        "estratégias de engajamento e retenção profissional",
    ],
    publico="empresas de pequeno e médio porte que desejam implantar ou aprimorar RH estratégico, e profissionais em transição",
    diferencial="consultoria imparcial pioneira no modelo HR as a Service, focada em maximizar o potencial humano como motor de crescimento das empresas",

    links_internos=[
        LinkInterno("Home — People Partner", "https://peoplepartner.com.br/",
                    "consultoria de RH People Partner"),
        LinkInterno("Serviços", "https://peoplepartner.com.br/#servicos",
                    "serviços de consultoria em recursos humanos"),
        LinkInterno("Sobre Nós", "https://peoplepartner.com.br#sobre",
                    "conheça a People Partner e nossa história"),
        LinkInterno("Clientes", "https://peoplepartner.com.br/#clientes",
                    "empresas atendidas pela People Partner"),
        LinkInterno("Vagas", "https://peoplepartner.com.br/vagas",
                    "vagas disponíveis via People Partner"),
        LinkInterno("Blog", "https://peoplepartner.com.br/blog/",
                    "conteúdos sobre gestão de pessoas e RH"),
    ],
    whitelist_externos=[
        ".gov", ".gov.br", ".edu", ".edu.br",
        "mte.gov.br", "trabalho.gov.br", "ibge.gov.br",
        "who.int", "ilo.org",
        "shrm.org", "hbr.org",
        "developers.google.com",
        "schema.org", "w3.org",
        "moz.com", "ahrefs.com", "semrush.com",
    ],

    whatsapp="https://api.whatsapp.com/send/?phone=5531995373137&text=Oi!%20Encontrei%20a%20People%20Partner%20no%20Google%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es.&type=phone_number&app_absent=0",
    enderecos=[],   # FALTA no crew legado — preencher manualmente
    assinatura="People Partner — Recursos Humanos e Gestão de Pessoas | HR as a Service",
)

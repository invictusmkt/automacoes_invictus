# -*- coding: utf-8 -*-
"""Contrato de dados de um cliente (config-driven).

Um cliente é DADO, não código: cada cliente vive em `clients/<slug>.py` como uma
instância de `ClientConfig`. O pipeline (pasta `pipeline/`) é único e consome essa
config. Para cadastrar um cliente novo, basta criar um arquivo de config — nenhum
agente, task ou rota precisa ser escrito à mão.

Usa apenas a stdlib (dataclasses) de propósito: zero dependência extra e fácil de
validar/import sem subir crewai.
"""
from dataclasses import dataclass, field

# Segmentos regulados: exigem tom estritamente educativo, sem urgência/promessa.
SEGMENTOS_ETICOS = {
    "saude", "saúde", "odonto", "odontologia",
    "veterinaria", "veterinária", "juridico", "jurídico",
}


@dataclass(frozen=True)
class LinkInterno:
    """Uma página do site do cliente, elegível para linkagem interna."""
    titulo: str
    url: str
    anchor: str = ""


@dataclass
class ClientConfig:
    """Tudo que varia de um cliente para outro. O resto é pipeline compartilhado."""
    # Identidade / rota
    slug: str                       # vira a rota /<slug> e /<slug>_backlink
    nome: str
    especialidade: str
    segmento: str                   # "saude" | "odonto" | "juridico" | "comercial" | ...

    # Linkagem
    dominio_oficial: str            # ex.: "clinicadrraimundonunes.com.br"
    links_internos: list[LinkInterno]
    whitelist_externos: list[str]

    # Assinatura institucional (anexada de forma determinística)
    assinatura: str
    whatsapp: str = ""
    enderecos: list[str] = field(default_factory=list)

    # Contexto opcional para enriquecer os prompts
    cidade: str = ""
    estado: str = ""
    bairro: str = ""
    servicos: list[str] = field(default_factory=list)
    publico: str = ""
    diferencial: str = ""
    credenciais: str = ""

    # Controle de extensão do post.
    # Gemini Flash entrega sistematicamente ~40% acima do alvo pedido no prompt,
    # então pedimos um alvo menor para que o resultado real fique perto de 1100-1200 palavras.
    # Se a LLM passar a respeitar o pedido literalmente, basta aumentar estes valores.
    target_palavras: tuple = (700, 850)
    teto_palavras: int = 900

    # Customização da assinatura
    assinatura_intro: str = (
        "Para esclarecer dúvidas ou avaliar a melhor conduta para o seu caso, "
        "a equipe está à disposição."
    )
    cta_whatsapp_label: str = "Fale com a nossa equipe pelo WhatsApp"

    @property
    def is_etico(self) -> bool:
        """True para segmentos regulados (saúde, odonto, veterinária, jurídico)."""
        return self.segmento.strip().lower() in SEGMENTOS_ETICOS

    @property
    def localidade(self) -> str:
        partes = []
        if self.bairro:
            partes.append(self.bairro)
        cidade_uf = self.cidade + ("/" + self.estado if self.estado else "")
        if cidade_uf:
            partes.append(cidade_uf)
        return ", ".join(partes)

    @property
    def servicos_resumo(self) -> str:
        return " | ".join(self.servicos[:4])

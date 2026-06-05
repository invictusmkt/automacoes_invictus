# -*- coding: utf-8 -*-
"""Pós-processamento determinístico do HTML, dirigido pela config do cliente.

Reaproveita a faxina validada em `crews/_common.py` (sanitizar_links) e monta a
assinatura institucional a partir do `ClientConfig` — sem passar pelo LLM, o que
garante integridade de WhatsApp, credenciais e endereços.
"""
from crews._common import sanitizar_links as _sanitizar_base
from core.models import ClientConfig


def sanitizar_links(html: str, cfg: ClientConfig) -> str:
    """Faxina determinística: remove links inventados/quebrados e tags de documento."""
    catalogo = [{"url": li.url} for li in cfg.links_internos]
    return _sanitizar_base(html, catalogo, cfg.whitelist_externos)


def montar_assinatura(cfg: ClientConfig) -> str:
    """Bloco fixo de assinatura (intro + WhatsApp + razão social + endereços)."""
    enderecos = "<br>\n".join(cfg.enderecos)
    return (
        f"<p>{cfg.assinatura_intro}</p>\n"
        f'<p><a href="{cfg.whatsapp}" target="_blank" rel="noopener noreferrer">'
        f"{cfg.cta_whatsapp_label}</a></p>\n"
        f"<p><strong>{cfg.assinatura}</strong><br>\n{enderecos}</p>"
    ).strip()


def finalizar_html(html: str, cfg: ClientConfig) -> str:
    """Pipeline determinístico final: sanitiza o corpo e anexa a assinatura imutável."""
    corpo = sanitizar_links(html, cfg)
    return corpo.rstrip() + "\n\n" + montar_assinatura(cfg)

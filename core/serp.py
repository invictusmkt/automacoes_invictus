# -*- coding: utf-8 -*-
"""Pesquisa de concorrência via SerpAPI — fonte única (antes duplicada em 21 crews).

A busca é feita UMA vez por post; tanto o texto de contexto quanto a seleção de
links externos autoritativos derivam do mesmo resultado.
"""
import os
from serpapi import GoogleSearch


def buscar_serp(palavra_chave: str, num: int = 10) -> list[dict]:
    """Resultados orgânicos do Google para a palavra-chave (pt-BR)."""
    search = GoogleSearch({
        "q": palavra_chave, "hl": "pt-br", "gl": "br", "num": num,
        "api_key": os.getenv("SERPAPI_API_KEY"),
    })
    return search.get_dict().get("organic_results", []) or []


def texto_concorrencia(resultados: list[dict]) -> str:
    """Bloco de texto com título/trecho/URL dos concorrentes, para contexto do redator."""
    return "\n".join(
        f"Título: {r.get('title','')}\nTrecho: {r.get('snippet','')}\nURL: {r.get('link','')}\n"
        for r in resultados
    )


def selecionar_externos(resultados: list[dict], whitelist: list[str],
                        max_links: int = 2) -> list[dict]:
    """Filtra os resultados, mantendo só domínios autoritativos da whitelist do cliente."""
    dominios = [d.lower() for d in (whitelist or [])]
    candidatos, vistos = [], set()
    for r in resultados:
        url = r.get("link") or r.get("url") or ""
        titulo = (r.get("title") or "").strip()
        if not url or url in vistos:
            continue
        if any(dom in url.lower() for dom in dominios):
            candidatos.append({
                "titulo": titulo[:90] or "Fonte externa",
                "url": url,
                "anchor": titulo[:70].lower() or "fonte oficial",
            })
            vistos.add(url)
        if len(candidatos) >= max_links:
            break
    return candidatos

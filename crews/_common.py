# -*- coding: utf-8 -*-
"""Utilitários compartilhados entre as crews.

Reúne a defesa determinística de qualidade validada no piloto `dr_raimundo`:
- `REGRA_KEYWORD`: diretriz anti keyword-stuffing reutilizável nos prompts.
- `sanitizar_links`: faxina final do HTML (cercas markdown, tags de documento,
  raciocínio vazado e links inventados/quebrados), independente da variação do LLM.
"""
import re

# ── Diretriz reutilizável de uso da palavra-chave (anti-stuffing) ──────────────
REGRA_KEYWORD = (
    "Uso da palavra-chave: ela pode (e deve) ser flexionada, reordenada ou "
    "parcialmente reescrita para soar 100% natural na frase. NUNCA insira a frase "
    "exata da palavra-chave como bloco isolado, com inicial maiúscula forçada, nem "
    "destacada em <em>/<strong>. No máximo 1 menção próxima à forma exata em todo o "
    "texto; as demais devem ser variações semânticas e sinônimos."
)


def normalizar_url(url: str) -> str:
    return (url or "").strip().rstrip("/").lower()


def sanitizar_links(html, links_internos=None, whitelist=None):
    """Defesa determinística contra HTML sujo e links quebrados/inventados.

    1) Se houver blocos cercados (```html ... ```), mantém só o ÚLTIMO bloco
       (o modelo às vezes vaza raciocínio com exemplos cercados antes da resposta).
    2) Remove tags de documento (<body>, <html>, <head>) — saída body-only.
    3) Remove prosa/raciocínio antes da primeira tag de bloco.
    4) Varre todas as tags <a> e, para cada href que NÃO esteja no catálogo interno,
       na whitelist de autoridades externas ou no WhatsApp oficial, remove o link
       preservando o texto da âncora (unwrap). Elimina URLs relativas e inventadas.

    `links_internos`: lista de dicts com chave "url" (catálogo do cliente).
    `whitelist`: lista de domínios/substrings externos autorizados.
    """
    if not html:
        return html

    if "```" in html:
        segmentos = [s for s in re.split(r"```(?:[a-zA-Z]+)?", html) if s.strip()]
        if segmentos:
            html = segmentos[-1]
    html = re.sub(r"</?(?:body|html|head)\b[^>]*>", "", html, flags=re.IGNORECASE)
    m = re.search(r"<(?:p|h2|h3|ul|ol)\b", html, flags=re.IGNORECASE)
    if m:
        html = html[m.start():]
    html = html.strip()

    permitidos_internos = {normalizar_url(li["url"]) for li in (links_internos or []) if li.get("url")}
    dominios = [d.lower() for d in (whitelist or [])]

    def _href_permitido(href: str) -> bool:
        h = (href or "").strip()
        hl = h.lower()
        if normalizar_url(h) in permitidos_internos:
            return True
        if "wa.me" in hl or "wa.link" in hl or "api.whatsapp.com" in hl:
            return True
        if any(dom in hl for dom in dominios):
            return True
        return False

    padrao_a = re.compile(r'<a\b[^>]*?href\s*=\s*["\']([^"\']*)["\'][^>]*>(.*?)</a>',
                          re.IGNORECASE | re.DOTALL)

    def _substituir(match: re.Match) -> str:
        href, texto_ancora = match.group(1), match.group(2)
        if _href_permitido(href):
            return match.group(0)
        return texto_ancora  # unwrap: mantém o texto, descarta o link inválido

    return padrao_a.sub(_substituir, html)

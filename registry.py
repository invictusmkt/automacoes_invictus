# -*- coding: utf-8 -*-
"""Registro central de clientes → rotas.

Cada entrada mapeia um `slug` para um "runner": uma função (tema, palavra_chave) -> dict
pronto para virar JSON (mesmo formato de `resultado.model_dump()` de sempre, com `.raw`
já pós-processado). O `main.py` apenas itera este registro e cria as rotas.

Dois tipos de runner convivem durante a migração:
- NOVO (config-driven): pipeline único de 3 agentes (pipeline/builder.py) + finalização
  determinística (core/content.py). É o destino de todos os clientes.
- LEGADO: crews antigos ainda não migrados. Continuam funcionando exatamente como hoje,
  então nenhuma rota muda de comportamento até ser migrada de propósito.

Migrar um cliente = criar `clients/<slug>.py` e trocar sua linha aqui de `_legado(...)`
para `_novo(CONFIG)`. Nada mais.
"""
from core.content import finalizar_html
from pipeline.builder import build_crew

# ── Clientes migrados (pipeline novo) ──────────────────────────────────────────
from clients.invictus import CONFIG as CFG_INVICTUS
from clients.dra_tati import CONFIG as CFG_DRA_TATI
from clients.nucleo_rural import CONFIG as CFG_NUCLEO_RURAL
from clients.villa_puppy import CONFIG as CFG_VILLA_PUPPY
from clients.dra_emmen import CONFIG as CFG_DRA_EMMEN
from clients.dra_catarine import CONFIG as CFG_DRA_CATARINE
from clients.clinicas_nexo import CONFIG as CFG_CLINICAS_NEXO
from clients.dr_ricardo import CONFIG as CFG_DR_RICARDO
from clients.nippo_dents import CONFIG as CFG_NIPPO_DENTS
from clients.dra_silvia import CONFIG as CFG_DRA_SILVIA
from clients.dr_daniel import CONFIG as CFG_DR_DANIEL
from clients.moc_advogados import CONFIG as CFG_MOC_ADVOGADOS
from clients.people_partner import CONFIG as CFG_PEOPLE_PARTNER
from clients.dr_raimundo import CONFIG as CFG_DR_RAIMUNDO

# ── Clientes legados (crews antigos, intactos até migração) ─────────────────────
# Clientes NÃO incluídos na lista de migração do usuário continuam usando o crew antigo.
from crews.dra_francine.crew_francine import build_crew_francine, sanitizar_links as san_francine
from crews.dr_gustavo.crew_gustavo import build_crew_gustavo, sanitizar_links as san_gustavo
from crews.dr_guilherme.crew_guilherme import build_crew_guilherme, sanitizar_links as san_guilherme
from crews.dra_karen.crew_karen import build_crew_karen, sanitizar_links as san_karen
from crews.dr_gerson.crew_gerson import build_crew_gerson, sanitizar_links as san_gerson
from crews.dra_angelica.crew_angelica import build_crew_angelica, sanitizar_links as san_angelica


def _novo(cfg):
    """Runner do pipeline config-driven (3 agentes + finalização determinística)."""
    def gerar(tema: str, palavra_chave: str) -> dict:
        resultado = build_crew(cfg, tema, palavra_chave).kickoff()
        resultado.raw = finalizar_html(resultado.raw, cfg)
        return resultado.model_dump()
    return gerar


def _legado(build_fn, san_fn):
    """Runner que preserva o comportamento atual de um crew ainda não migrado."""
    def gerar(tema: str, palavra_chave: str) -> dict:
        resultado = build_fn(tema, palavra_chave).kickoff()
        resultado.raw = san_fn(resultado.raw)
        return resultado.model_dump()
    return gerar


# slug → runner. Os slugs reproduzem EXATAMENTE as rotas atuais (o n8n não muda).
REGISTRO = {
    # ── Migrados (pipeline novo, 3 agentes) ────────────────────────────────
    "invictus":       _novo(CFG_INVICTUS),
    "dra_tati":       _novo(CFG_DRA_TATI),
    "nucleo_rural":   _novo(CFG_NUCLEO_RURAL),
    "villa_puppy":    _novo(CFG_VILLA_PUPPY),
    "dra_emmen":      _novo(CFG_DRA_EMMEN),
    "dra_catarine":   _novo(CFG_DRA_CATARINE),
    "clinicas_nexo":  _novo(CFG_CLINICAS_NEXO),
    "dr_ricardo":     _novo(CFG_DR_RICARDO),
    "nippo_dents":    _novo(CFG_NIPPO_DENTS),
    "dra_silvia":     _novo(CFG_DRA_SILVIA),
    "dr_daniel":      _novo(CFG_DR_DANIEL),
    "moc_advogados":  _novo(CFG_MOC_ADVOGADOS),
    "people_partner": _novo(CFG_PEOPLE_PARTNER),
    "dr_raimundo":    _novo(CFG_DR_RAIMUNDO),

    # ── Legados (não estavam na lista de migração; intactos) ───────────────
    "dra_francine":   _legado(build_crew_francine, san_francine),
    "dr_gustavo":     _legado(build_crew_gustavo, san_gustavo),
    "dr_guilherme":   _legado(build_crew_guilherme, san_guilherme),
    "dra_karen":      _legado(build_crew_karen, san_karen),
    "dr_gerson":      _legado(build_crew_gerson, san_gerson),
    "dra_angelica":   _legado(build_crew_angelica, san_angelica),
}

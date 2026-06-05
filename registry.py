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
from clients.dr_raimundo import CONFIG as CFG_DR_RAIMUNDO

# ── Clientes legados (crews antigos, intactos até migração) ─────────────────────
from crews.invictus.crew_invictus import build_crew_invictus, sanitizar_links as san_invictus
from crews.dra_francine.crew_francine import build_crew_francine, sanitizar_links as san_francine
from crews.dra_tati.crew_tati import build_crew_tatiana, sanitizar_links as san_tatiana
from crews.dr_gustavo.crew_gustavo import build_crew_gustavo, sanitizar_links as san_gustavo
from crews.dr_guilherme.crew_guilherme import build_crew_guilherme, sanitizar_links as san_guilherme
from crews.dra_karen.crew_karen import build_crew_karen, sanitizar_links as san_karen
from crews.nucleo_rural.crew_nucleo_rural import build_crew_nucleorural, sanitizar_links as san_nucleorural
from crews.dr_gerson.crew_gerson import build_crew_gerson, sanitizar_links as san_gerson
from crews.villa_puppy.crew_villa_puppy import build_crew_villapuppy, sanitizar_links as san_villapuppy
from crews.dra_angelica.crew_angelica import build_crew_angelica, sanitizar_links as san_angelica
from crews.dra_emmen.crew_emmen import build_crew_emmen, sanitizar_links as san_emmen
from crews.dra_catarine.crew_catarine import build_crew_catarine, sanitizar_links as san_catarine
from crews.clinicas_nexo.crew_clinicas_nexo import build_crew_clinicasnexo, sanitizar_links as san_clinicasnexo
from crews.nippo_dents.crew_nippo_dents import build_crew_nippodents, sanitizar_links as san_nippodents
from crews.dra_silvia.crew_dra_silvia import build_crew_drasilvia, sanitizar_links as san_drasilvia
from crews.dr_daniel.crew_dr_daniel import build_crew_drdaniel, sanitizar_links as san_drdaniel
from crews.moc_advogados.crew_moc_advogados import build_crew_mocadvogados, sanitizar_links as san_mocadvogados
from crews.people_partner.crew_people_partner import build_crew_peoplepartner, sanitizar_links as san_peoplepartner
from crews.dr_ricardo.crew_dr_ricardo import build_crew_drricardo, sanitizar_links as san_drricardo


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
    # migrado
    "dr_raimundo":    _novo(CFG_DR_RAIMUNDO),
    # legados
    "invictus":       _legado(build_crew_invictus, san_invictus),
    "dra_francine":   _legado(build_crew_francine, san_francine),
    "dra_tati":       _legado(build_crew_tatiana, san_tatiana),
    "dr_gustavo":     _legado(build_crew_gustavo, san_gustavo),
    "dr_guilherme":   _legado(build_crew_guilherme, san_guilherme),
    "dra_karen":      _legado(build_crew_karen, san_karen),
    "nucleo_rural":   _legado(build_crew_nucleorural, san_nucleorural),
    "dr_gerson":      _legado(build_crew_gerson, san_gerson),
    "villa_puppy":    _legado(build_crew_villapuppy, san_villapuppy),
    "dra_angelica":   _legado(build_crew_angelica, san_angelica),
    "dra_emmen":      _legado(build_crew_emmen, san_emmen),
    "dra_catarine":   _legado(build_crew_catarine, san_catarine),
    "clinicas_nexo":  _legado(build_crew_clinicasnexo, san_clinicasnexo),
    "nippo_dents":    _legado(build_crew_nippodents, san_nippodents),
    "dra_silvia":     _legado(build_crew_drasilvia, san_drasilvia),
    "dr_daniel":      _legado(build_crew_drdaniel, san_drdaniel),
    "moc_advogados":  _legado(build_crew_mocadvogados, san_mocadvogados),
    "people_partner": _legado(build_crew_peoplepartner, san_peoplepartner),
    "dr_ricardo":     _legado(build_crew_drricardo, san_drricardo),
}

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
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
from crews.dr_raimundo.crew_dr_raimundo import build_crew_drraimundo, sanitizar_links as san_drraimundo




app = FastAPI()

@app.get("/invictus")
@app.get("/invictus_backlink")
def executar_crew_invictus(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_invictus(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_invictus(resultado.raw)
    return JSONResponse(content=resultado.model_dump())

@app.get("/dra_francine")
@app.get("/dra_francine_backlink")
def executar_crew_francine(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_francine(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_francine(resultado.raw)
    return JSONResponse(content=resultado.model_dump())

@app.get("/dra_tati")
@app.get("/dra_tati_backlink")
def executar_crew_tatiana(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_tatiana(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_tatiana(resultado.raw)
    return JSONResponse(content=resultado.model_dump())

@app.get("/dr_gustavo")
@app.get("/dr_gustavo_backlink")
def executar_crew_gustavo(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_gustavo(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_gustavo(resultado.raw)
    return JSONResponse(content=resultado.model_dump())

@app.get("/dr_guilherme")
@app.get("/dr_guilherme_backlink")
def executar_crew_guilherme(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_guilherme(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_guilherme(resultado.raw)
    return JSONResponse(content=resultado.model_dump())

@app.get("/dra_karen")
@app.get("/dra_karen_backlink")
def executar_crew_karen(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_karen(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_karen(resultado.raw)
    return JSONResponse(content=resultado.model_dump())

@app.get("/nucleo_rural")
@app.get("/nucleo_rural_backlink")
def executar_crew_nucleorural(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_nucleorural(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_nucleorural(resultado.raw)
    return JSONResponse(content=resultado.model_dump())

@app.get("/dr_gerson")
@app.get("/dr_gerson_backlink")
def executar_crew_gerson(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_gerson(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_gerson(resultado.raw)
    return JSONResponse(content=resultado.model_dump())

@app.get("/villa_puppy")
@app.get("/villa_puppy_backlink")
def executar_crew_villapuppy(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_villapuppy(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_villapuppy(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/dra_angelica")
@app.get("/dra_angelica_backlink")
def executar_crew_angelica(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_angelica(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_angelica(resultado.raw)
    return JSONResponse(content=resultado.model_dump())

@app.get("/dra_emmen")
@app.get("/dra_emmen_backlink")
def executar_crew_emmen(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_emmen(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_emmen(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/dra_catarine")
@app.get("/dra_catarine_backlink")
def executar_crew_catarine(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_catarine(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_catarine(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/clinicas_nexo")
@app.get("/clinicas_nexo_backlink")
def executar_crew_clinicasnexo(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_clinicasnexo(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_clinicasnexo(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/nippo_dents")
@app.get("/nippo_dents_backlink")
def executar_crew_nippodents(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_nippodents(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_nippodents(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/dra_silvia")
@app.get("/dra_silvia_backlink")
def executar_crew_drasilvia(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_drasilvia(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_drasilvia(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/dr_daniel")
@app.get("/dr_daniel_backlink")
def executar_crew_drdaniel(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_drdaniel(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_drdaniel(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/moc_advogados")
@app.get("/moc_advogados_backlink")
def executar_crew_mocadvogados(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_mocadvogados(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_mocadvogados(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/people_partner")
@app.get("/people_partner_backlink")
def executar_crew_peoplepartner(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_peoplepartner(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_peoplepartner(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/dr_raimundo")
@app.get("/dr_raimundo_backlink")
def executar_crew_drraimundo(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_drraimundo(tema, palavra_chave)
    resultado = crew.kickoff()
    # Defesa determinística: remove links inventados/quebrados do HTML final
    resultado.raw = san_drraimundo(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/dr_ricardo")
@app.get("/dr_ricardo_backlink")
def executar_crew_drricardo(tema: str = Query(...), palavra_chave: str = Query(...)):
    crew = build_crew_drricardo(tema, palavra_chave)
    resultado = crew.kickoff()
    resultado.raw = san_drricardo(resultado.raw)
    return JSONResponse(content=resultado.model_dump())


@app.get("/teste")
def teste():
    return {"mensagem": "Teste OK"}

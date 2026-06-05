from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from registry import REGISTRO

app = FastAPI()


def _registrar(slug: str, gerar):
    """Cria as rotas /<slug> e /<slug>_backlink apontando para o mesmo handler."""
    def handler(tema: str = Query(...), palavra_chave: str = Query(...)):
        return JSONResponse(content=gerar(tema, palavra_chave))

    app.add_api_route(f"/{slug}", handler, methods=["GET"], name=f"crew_{slug}")
    app.add_api_route(f"/{slug}_backlink", handler, methods=["GET"], name=f"crew_{slug}_backlink")


# Registra todas as rotas a partir do catálogo central de clientes (registry.py).
for _slug, _gerar in REGISTRO.items():
    _registrar(_slug, _gerar)


@app.get("/teste")
def teste():
    return {"mensagem": "Teste OK"}

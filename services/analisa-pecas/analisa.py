from fastapi import FastAPI
from pydantic import BaseModel
from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer

# Configuração do OpenSearch
client = OpenSearch(
    hosts=[{"host": "supp-opensearch-api.pgmbh.org", "port": 443}],
    http_auth=("admin", "supp20Pgm25"),
    use_ssl=True,
    verify_certs=False
)

# Modelo de embeddings
model_emb = SentenceTransformer("all-MiniLM-L6-v2")

# FastAPI
app = FastAPI()

class Texto(BaseModel):
    conteudo: str

@app.post("/analisa")
def analisa_peca(entrada: Texto):
    vetor = model_emb.encode([entrada.conteudo])[0].tolist()

    # Buscar no OpenSearch
    resp = client.search(
        index="processos",   # ajuste o índice real
        body={
            "knn": {
                "field": "embedding",
                "query_vector": vetor,
                "k": 3,
                "num_candidates": 5
            }
        }
    )

    if resp["hits"]["hits"]:
        melhor = resp["hits"]["hits"][0]
        score = melhor["_score"]
        tipo = melhor["_source"].get("tipo", "desconhecido")
        resposta = melhor["_source"].get("resposta", "sem resposta")

        if score > 0.80:
            return {
                "tipo": tipo,
                "conhece": True,
                "resposta_sugerida": resposta
            }
        else:
            return {
                "tipo": "desconhecido",
                "conhece": False,
                "resposta_sugerida": None
            }
    else:
        return {"tipo": "nenhum_similar", "conhece": False, "resposta_sugerida": None}

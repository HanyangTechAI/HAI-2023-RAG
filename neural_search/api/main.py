from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.chroma import (
    create_collection,
    check_collection,
    delete_collection,
    index_documents,
    search_documents,
)
from api.models import (
    CreateRequest,
    DeleteRequest,
    IndexingRequest,
)

app = FastAPI()


@app.get("/health")
async def health() -> JSONResponse:
    return "OK"


@app.post("/create")
async def create(request: CreateRequest) -> JSONResponse:
    # 컬렉션 생성 로직
    try:
        collection = create_collection(request.collection_name, request.metadata)
        return JSONResponse(status_code=200, content={"status": "success"})
    except:
        return JSONResponse(status_code=500, content={"status": "failure"})


@app.get("/check/{collection_name}")
async def check(collection_name: str = "test") -> JSONResponse:
    # ChromeDB에서 컬렉션 존재 여부를 확인하는 로직
    try:
        collection = check_collection(collection_name)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "result": {
                    "name": collection.name,
                    "id": collection.id.hex,
                    "metadata": collection.metadata,
                },
            },
        )
    except:
        return JSONResponse(status_code=500, content={"status": "failure"})


@app.delete("/delete")
async def delete(request: DeleteRequest) -> JSONResponse:
    # 컬렉션 제거 로직
    try:
        delete_collection(request.collection_name)
        return JSONResponse(status_code=200, content={"status": "success"})
    except:
        return JSONResponse(status_code=500, content={"status": "failure"})


@app.post("/indexing")
async def indexing(request: IndexingRequest) -> JSONResponse:
    # 문서 저장 로직
    try:
        index_documents(request.collection_name, request.lang, request.data)
        return JSONResponse(status_code=200, content={"status": "success"})
    except:
        return JSONResponse(status_code=500, content={"status": "failure"})


@app.get("/search/{collection_name}")
async def search(collection_name: str = "text",
                 lang: str = "en",
                 query: str = "Hi, there!",
                 top_k: int = 2) -> JSONResponse:
    try:
        result = search_documents(collection_name, lang, query, top_k)
        return JSONResponse(status_code=200, content={
            "status": "success",
            "result": result
        })
    except:
        return JSONResponse(status_code=500, content={"status": "failure"})

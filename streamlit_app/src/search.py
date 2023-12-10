import json
import os

import requests

from files import convert_file_to_txt, convert_webpage_to_txt

os.makedirs("/files", exist_ok=True)
os.makedirs("/webpages", exist_ok=True)

search_api_url = "http://localhost:40103"
search_api_session = requests.session()
search_api_headers = {"accept": "application/json", "Content-Type": "application/json"}


def create(collection_name):
    data = {"collection_name": collection_name}
    response = search_api_session.post(
        f"{search_api_url}/create",
        headers=search_api_headers,
        data=json.dumps(data, ensure_ascii=False),
    )
    return response.json()


def index(collection_name, documents, metadatas, lang: str = "en"):
    data = {
        "collection_name": collection_name,
        "lang": lang,
        "data": [
            {"document": document, "metadata": metadata}
            for document, metadata in zip(documents, metadatas)
        ],
    }
    response = search_api_session.post(
        f"{search_api_url}/indexing",
        headers=search_api_headers,
        data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
    )
    return response.json()


def delete(collection_name):
    data = {"collection_name": collection_name}
    response = search_api_session.delete(
        f"{search_api_url}/delete",
        headers=search_api_headers,
        data=json.dumps(data, ensure_ascii=False),
    )
    return response.json()


def search(collection_name, query, lang: str = "en", top_k: int = 5):
    response = search_api_session.get(
        f"{search_api_url}/search/{collection_name}",
        headers=search_api_headers,
        params={
            "query": query,
            "lang": lang,
            "top_k": top_k,
        }
    )
    if response.status_code == 500:
        return []

    results = response.json()["result"]
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    data = []
    for doc, meta, dist in zip(docs, metas, dists):
        data.append(
            {
                "document": doc,
                "metadata": meta,
                "distance": dist,
            }
        )

    return data


def store_file_to_db(collection_name, uploaded_file, lang: str = "en"):
    filename = uploaded_file.name
    with open(f"/files/{filename}", "wb") as f:
        f.write(uploaded_file.read())

    create(collection_name)

    documents = convert_file_to_txt(f"/files/{filename}")
    metadatas = [
        {
            "file_name": filename,
            "page": i + 1,
        }
        for i in range(len(documents))
    ]

    index(collection_name, documents, metadatas, lang)

    return True

def store_webpage_to_db(collection_name, url, lang: str = "en"):
    with open(f"/webpages/url_{collection_name}.log", "a") as f:
        f.write(f"{url}\n")

    create(collection_name)

    documents = convert_webpage_to_txt(url)
    if not documents:
        return False
    
    metadatas = [
        {
            "url": url,
            "page": i + 1,
        }
        for i in range(len(documents))
    ]

    index(collection_name, documents, metadatas, lang)

    return True


if __name__ == "__main__":
    collection_name = "test"
    filename = "files/test.pdf"

    print("Create:", create(collection_name))
    documents = convert_file_to_txt(filename)
    metadatas = [
        {
            "file_name": filename,
            "page": i + 1,
        }
        for i in range(len(documents))
    ]

    print("Indexing:", index(collection_name, documents, metadatas))

    print("Search:")
    print(search(collection_name, "LLM의 미래가 궁금합니다."))

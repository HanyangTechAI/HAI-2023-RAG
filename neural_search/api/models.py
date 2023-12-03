from typing import List, Dict

from pydantic import BaseModel


# JSON 요청 본문을 위한 Pydantic 모델 정의
class CreateRequest(BaseModel):
    collection_name: str = "test"
    metadata: Dict = None


class DeleteRequest(BaseModel):
    collection_name: str = "test"


# 개별 문서와 메타데이터를 포함하는 모델
class Document(BaseModel):
    document: str = "Hello, World!"
    metadata: Dict = None


class IndexingRequest(BaseModel):
    collection_name: str = "test"
    lang: str = "en"
    data: List[Document]

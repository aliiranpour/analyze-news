from typing import TypedDict, List, Dict

class Article(TypedDict):
    link: str
    content: str
    hash: str

class NewsState(TypedDict):
    symbols: List[Dict[str, str]]
    links: List[str]
    articles: List[Article]
    summaries: List[dict]
    cache: dict

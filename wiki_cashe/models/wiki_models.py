from pydantic import BaseModel

class Wiki(BaseModel):
    success: bool = False
    wiki_url: str = None
    wiki_text: str = None
    wiki_image: str = None
    wiki_title: str = None
    wiki_article: str = None

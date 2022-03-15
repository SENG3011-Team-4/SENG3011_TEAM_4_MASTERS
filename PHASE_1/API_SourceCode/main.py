"""
Base API Interface linking the web service to other
resources.
"""

from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

# Base Input and Response Models
class SearchItem(BaseModel):
    """
    To be later modified depending on DB Implementation
    """
    keyterms: str
    location: dict
    start_date: str
    end_date: str
    timezone: Optional[str] = None

class Report(BaseModel):
    """
    As per spec
    """
    diseases: list
    syndrome: list
    event_date: list
    locations: list

class ArticleJson(BaseModel):
    """
    As per spec
    """
    url: str
    date_of_publication: str
    headline: str
    main_text: str
    reports: list


# API
app = FastAPI()

app.get('/hello')
async def hello():
    return {
        'message': "Hello World"
    }

app.get('/search')
async def search(
    search_item: SearchItem = Body(
        ...,
        example = {
            "keyterms": "Anthrax,Zika",
            "location": {
                "geonames_id": 1234567
            },
            "start_date": "2015-10-01T08:45:10",
            "end_date": "2015-11-01T19:37:12",
            "timezone": None
        }
    ),
):
    # Error checking dates and location
    # Add to search metrics
    # Hard hardwired value if passes all correct values
    pass

app.get('/search/key-frequency')
async def key_frequency():
    pass

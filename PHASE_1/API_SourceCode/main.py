"""
Base API Interface linking the web service to other
resources.
"""

from typing import List, Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

# Base Input and Response Models
class SignUpInfo(BaseModel):
    """
    To be used later to collect account information
    """
    email: str
    username: str
    name: str
    password: str

class LoginInfo(BaseModel):
    """
    To be used later for Login and Logout.
    """
    username: str
    password: str

class SearchItem(BaseModel):
    """
    To be later modified depending on DB Implementation
    """
    keyterms: str
    location: dict
    start_date: str
    end_date: str
    timezone: Optional[str] = None
    # To be used for account logging
    account_id: Optional[str] = None

class Report(BaseModel):
    """
    As per spec
    """
    diseases: List[str] = None
    syndrome: List[str] = None
    event_date: List[str]
    locations: List[str]

    class Config:
        schema_extra = {
             "example": {
                    "diseases": ["RandoVirus"],
                    "syndrome": None,
                    "event_date": ["2015-10-01T08:45:10"],
                    "locations": ["1234567"]
                }
        }

class ArticleJson(BaseModel):
    """
    As per spec
    """
    url: str
    date_of_publication: str
    headline: str
    main_text: str
    reports: List[Report]

    class Config:
        schema_extra = {
            "example": {
                "url": "www.example.com",
                "date_of_publication": "2015-10-01T08:45:10",
                "headline": "Pandemic Caused by RandoVirus",
                "main_text": "Randovirus is a random virus...",
                "reports": {
                    "diseases": ["RandoVirus"],
                    "syndrome": None,
                    "event_date": ["2015-10-01T08:45:10"],
                    "locations": ["1234567"]
                }
            }
        }

class HealthCheck(BaseModel):
    """
    As per spec
    """
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Hello World!"
            }
        }

class SearchHistory(BaseModel):
    top_five_key_terms: List[str]

    class Config:
        schema_extra = {
            "example": {
                "top_five_key_terms": ["Zika", "Rhinovirus", "Coronavirus", "Smallpox", "Measles"]
            }
        }


# API
app = FastAPI()

@app.get(
    '/healthcheck',
    response_model = HealthCheck
)
async def healtchcheck():
    return {
        'message': "Hello World!"
    }

@app.get(
    '/search',
    response_model = ArticleJson
)
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
            "timezone": None,
            "account_id": None
        }
    ),
):
    # Error checking dates and location
    # Add to search metrics
    # Pass hardcoded value if passes all correct values
    pass

@app.get(
    '/search/key-frequency',
    response_model = SearchHistory
)
async def key_frequency():
    # Obtain most frequently searched keys in DB
    pass

@app.get(
    '/search/history',
    response_model =  SearchHistory
)
async def search_history():
    # Right now it is to get the global search history
    pass

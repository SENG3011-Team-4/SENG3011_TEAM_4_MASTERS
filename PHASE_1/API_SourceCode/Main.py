"""
Base API Interface linking the web service to other
resources.
"""

from typing import List, Optional
from fastapi import Body, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

### BASE INPUT AND RESPONSE MODELS
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
    location: str
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
                "code": 200,
                "message": "Hello World!"
            }
        }

class SearchHistory(BaseModel):
    top_five_keyterms: List[str]

    class Config:
        schema_extra = {
            "example": {
                "top_five_keyterms": ["Zika", "Rhinovirus", "Coronavirus", "Smallpox", "Measles"]
            }
        }

### EXAMPLE RESPONSES

search_responses = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "Paramter Validation": {
                        "summary": "Parameter Validation Failed",
                        "value": {"code": 400, "message": "Parameter validation has failed"}
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "examples": {
                    "Unknown": {
                        "summary": "Unknown Error",
                        "value": {"code": 500, "message": "Internal Server Error"}
                    }
                }
            }
        }
    },
}

other_responses = {
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "examples": {
                    "Unknown": {
                        "summary": "Unknown Error",
                        "value": {"code": 500, "message": "Internal Server Error"}
                    }
                }
            }
        }
    },
}

### API
app = FastAPI()

@app.get(
    '/healthcheck',
    response_model = HealthCheck,
    responses = other_responses
)
async def healtchcheck():
    return {
        'message': "Hello World!"
    }

@app.get(
    '/search',
    response_model = ArticleJson,
    responses = search_responses
)
async def search(
    keyterms: str = Query(None, description='Input ASCII string collection of diseases e.g. "Zika,Coronavirus"'),
    location: str = Query(None, description='Input ASCII string collection of location e.g. United states'),
    start_date: str = Query(None, description='Start date format yyyy-MM-ddTHH:mm:ss e.g. "2015-10-01T08:45:10"'),
    end_date: str = Query(None, description='End date format yyyy-MM-ddTHH:mm:ss e.g. "2015-11-01T19:37:12"'),
    timezone: Optional[str] = Query(None, description='(OPTIONAL) Timezone format as UTC+HH e.g. UTC+12)'),
    account_id: Optional[str] = Query(None, description='(OPTIONAL) Email of user e.g. user@gmail.com')
):
    # Add to search metrics
    # Pass hardcoded value if passes all correct values
    if not (all(ord(char) < 128 for char in keyterms) and (' ' not in keyterms)):
        raise HTTPException(status_code=400, detail="Parameter validation has failed")
    if not (isinstance(geoname_location_id, int)):
        raise HTTPException(status_code=400, detail="Parameter validation has failed")
    # Error checking dates and geoname_location_id
    data = search_v1(keyterms,location,start_date,end_date,timezone)
    return {data}
   # raise HTTPException(status_code=404, detail="Endpoint not active")

@app.get(
    '/search/key_frequency',
    response_model = SearchHistory
)
async def key_frequency():
    # Obtain most frequently searched keys in DB
    return Search_Frequently_key_v1()
    #raise HTTPException(status_code=404, detail="Endpoint not active")

@app.get(
    '/search/history',
    response_model =  SearchHistory
)
async def search_history():
    # Right now it is to get the global search history
    return Search_History_v1()
    #raise HTTPException(status_code=404, detail="Endpoint not active")

"""
Base API Interface linking the web service to other
resources.
"""

from typing import List, Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel
from search import *
from auth import * 

### BASE INPUT AND RESPONSE MODELS
class RegisterInfo(BaseModel):
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

class LogoutInfo(BaseModel):
    """
    Used for logout
    """
    token: str

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
    #account_id: Optional[str] = None

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
                "report": {
                    "diseases": ["RandoVirus"],
                    "syndrome": None,
                    "event_date": ["2015-10-01T08:45:10"],
                    "locations": [
                        {
                            'cities': ['Carolina','Massa'],
                            'country': ['United States']
                        }
                    ]
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
    
class Login(BaseModel):
    """
    As per spec
    """
    message: str

    class Config:
        schema_extra = {
            "example": {
                "token": "string"
            }
        }

class Logout(BaseModel):
    """
    As per spec
    """
    message: str

    class Config:
        schema_extra = {
            "example": {
                "is_success": True
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

class KeyFrequencies(BaseModel):
    
    top_five_keys: List[dict]

    class Config:
        schema_extra = {
            "example": {
                "top_five_keys": [
                    {
                        "key": "unknown",
                        "frequency": 291
                    },
                    {
                        "key": "anthrax cutaneous",
                        "frequency": 287
                    },
                    {
                        "key": "anthrax inhalation",
                        "frequency": 287
                    },
                    {
                        "key": "anthrax gastrointestinous",
                        "frequency": 287
                    },
                    {
                        "key": "other",
                        "frequency": 287
                    }
                ]
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
                        "value": {"detail": "Parameter validation has failed"}
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
                        "summary": "Internal Server Error",
                        "value": {"detail": "Internal Server Error"}
                    }
                }
            }
        }
    },
}

logout_response = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "Logout Failed": {
                        "summary": "Logout Failed",
                        "value": {"detail": "Logout Failed"}
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
                        "summary": "Internal Server Error",
                        "value": {"detail": "Internal Server Error"}
                    }
                }
            }
        }
    },
}



login_responses = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "examples": {
                    "Invalid Credentials": {
                        "summary": "Email or Password Invalid",
                        "value": {"detail": "Invalid Email or Password"}
                    }
                }
            }
        }
    },
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "examples": {
                    "Incorrect Login Details": {
                        "summary": "Login parameters incorrect",
                        "value": {"detail": "Incorrect Email or Password"}
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
                        "summary": "Internal Server Error",
                        "value": {"detail": "Internal Server Error"}
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
    # response_model = HealthCheck,
    responses = other_responses
)
async def healtchcheck():
    return {
        'message': "Hello World!"
    }

@app.post(
    '/login',
    # response_model = Login,
    responses = login_responses
)
async def login(item: LoginInfo):
    return auth_login_v1(item['email'], item['password'])

@app.post(
    '/register',
    # esponse_model = Login,
    responses = login_responses
)
async def login(item: RegisterInfo):
    return auth_register_v1(item['username'], item['email'], item['password'])

@app.post(
    '/logout',
    # response_model = Logout,
    responses = logout_response
)
async def logout(item: LoginInfo):
    return auth_login_v1(item['email'], item['password'])

@app.get(
    '/search',
    # response_model = ArticleJson,
    responses = search_responses
)
async def search(
    keyterms: str = Query(None, description='Input ASCII string collection of diseases e.g. "Zika,Coronavirus"'),
    location: str = Query(None, description='Input ASCII string collection of location e.g. United states'),
    start_date: str = Query(None, description='Start date format yyyy-MM-ddTHH:mm:ss e.g. "2015-10-01T08:45:10"'),
    end_date: str = Query(None, description='End date format yyyy-MM-ddTHH:mm:ss e.g. "2015-11-01T19:37:12"'),
    timezone: Optional[str] = Query(None, description='(OPTIONAL) Timezone format as UTC+HH e.g. UTC+12)'),
    #account_id: Optional[str] = Query(None, description='(OPTIONAL) Email of user e.g. user@gmail.com')
):
    if (timezone is None):
        data = search_v1(keyterms, location, start_date, end_date)
    else:
        data = search_v1(keyterms, location, start_date, end_date, timezone)
    return {
        "data": data
    }

@app.get(
    '/search/twitter'
)
async def search_twitter(
    location: str = Query(None, description='Input ASCII string collection of location e.g. United states'),
    disease: str = Query(None, description='Input ASCII string collection of location e.g. United states')
):
    # Obtain most frequently searched keys in DB
    return search_twitter_v1(location, disease)

@app.get(
    '/search/treatment'
)
async def search_treatment(
    disease: str = Query(None, description='Input ASCII string collection of location e.g. United states')
):
    # Obtain most frequently searched keys in DB
    return search_treatment_v1(disease)


@app.get(
    '/search/key_frequency',
    # response_model = KeyFrequencies
)
async def key_frequency():
    # Obtain most frequently searched keys in DB
    return search_frequency_key_v1()

@app.get(
    '/search/history',
    # response_model =  SearchHistory
)
async def search_history(
    token: str = Query(None, description='User Token'),
):
    # Right now it is to get the global search history
    return search_history_v1(token)

from pydantic import BaseModel


class DBConfig(BaseModel):
    host: str
    user: str
    password: str
    database: str


class HTTPConfig(BaseModel):
    cors_allow_origins: list[str]
    cors_allow_methods: list[str]
    cors_allow_headers: list[str]
    cors_allow_credentials: bool


class Config(BaseModel):
    db: DBConfig
    http: HTTPConfig


config = Config(
    db=DBConfig(
        host="127.0.0.1",
        user="postgres",
        password="root123",
        database="orders",
    ),
    http=HTTPConfig(
        cors_allow_origins=["*"],
        cors_allow_methods=[
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS",
            "HEAD",
        ],
        cors_allow_headers=["*"],
        cors_allow_credentials=False,
    ),
)
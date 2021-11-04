import secrets

from typing import List, Union
from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    # API 서버 설정
    API_SERVER_NAME: str = 'law-farm-api'
    API_V1_PATH: str = '/v1'

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:3000', 'https://localhost:3000', 'http://192.168.0.2:3000']

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # JWT 토큰 설정:
    # TODO 키 고정되게 바꾸
    ACCESS_TOKEN_SECRET_KEY: str = 'UjIO1gVJJUOGxYivw8Aj-GKkJoOb180hBSzsp9sfbv4'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # MySQL DB 세팅 (미리 입력되어 있는 값은 default 값: production 시 교체 권장)
    MYSQL_HOST: str = 'mysql'
    MYSQL_USER: str = 'root'
    MYSQL_PASSWORD: str = 'lawfarm2021'
    MYSQL_DB: str = 'lawfarm'


settings = Settings()

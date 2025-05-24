import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PROXIES_YAML = os.getenv("PROXIES_YAML")
    JSON_OUT = os.getenv("JSON_OUT")
    URL = os.getenv("KUMA_URL")
    USERNAME = os.getenv("KUMA_USERNAME")
    PASSWORD = os.getenv("KUMA_PASSWORD")


config = Config()

if __name__ == "__main__":
    print(config)

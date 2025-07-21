import logging

from fastapi import FastAPI

from config import settings

logging.basicConfig(level=logging.INFO)

app = FastAPI(root_path=settings.root_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import tests_router

app = FastAPI(
    contact={
        'name': "Asilbek Tojialiyev's telegram bot url for questions",
        'url': 'https://t.me/asilbekga_murojaat_bot',
    },
    docs_url='/',
    redoc_url='/redoc',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"], )

app.include_router(tests_router)

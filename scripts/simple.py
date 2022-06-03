from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from imageprocess import predict_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"Este projeto é parte do curso da Iteratec no Youtube!"}


@app.get("/analyse_image")

def analyse_image(imageLink):

    prob, categories, disease=predict_image(imageLink)
    result = {
        'Probabilities': prob,
        "Categories":categories,
        'Disease': disease
    }

    return result

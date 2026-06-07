from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]


def classify(sentence: str) -> str:
    text = sentence.lower()

    happy_words = [
        "love", "great", "awesome", "happy",
        "excellent", "good", "wonderful",
        "fantastic", "amazing", "like",
        "best", "nice", "perfect", "enjoy"
    ]

    sad_words = [
        "sad", "hate", "terrible", "awful",
        "bad", "horrible", "worst",
        "angry", "upset", "disappointed",
        "poor", "boring", "annoying"
    ]

    if any(word in text for word in happy_words):
        return "happy"

    if any(word in text for word in sad_words):
        return "sad"

    return "neutral"


@app.get("/")
async def health_check():
    return {"status": "ok"}


# Support BOTH endpoints
@app.post("/")
@app.post("/sentiment")
async def sentiment(data: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": classify(sentence)
            }
            for sentence in data.sentences
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
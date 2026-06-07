from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SentimentRequest(BaseModel):
    sentences: list[str]

def classify(sentence: str) -> str:
    text = sentence.lower()

    happy_words = [
        "love", "great", "awesome", "happy",
        "excellent", "good", "wonderful",
        "fantastic", "amazing", "like"
    ]

    sad_words = [
        "sad", "hate", "terrible", "awful",
        "bad", "horrible", "worst",
        "angry", "upset", "disappointed"
    ]

    if any(word in text for word in happy_words):
        return "happy"

    if any(word in text for word in sad_words):
        return "sad"

    return "neutral"

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
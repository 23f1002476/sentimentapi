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

    happy_words = {
        "love","loved","lovely","great","awesome","happy","excellent",
        "good","wonderful","fantastic","amazing","like","best","nice",
        "perfect","enjoy","enjoyed","excited","joy","joyful","delighted",
        "glad","pleased","thrilled","brilliant","positive","superb",
        "outstanding","cheerful","success","successful","win","winner",
        "winning","beautiful","smile","smiling","recommend","favorite",
        "favourite","satisfied","satisfaction","impressed","incredible"
    }

    sad_words = {
        "sad","hate","hated","terrible","awful","bad","horrible","worst",
        "angry","upset","disappointed","poor","boring","annoying",
        "depressed","unhappy","miserable","frustrated","heartbroken",
        "negative","regret","regretful","cry","crying","painful",
        "dreadful","tragic","failure","failed","fail","loser","lose",
        "lost","disaster","disappointing","useless","broken","problem",
        "issues","issue","error","errors","bug","bugs","sucks","suck"
    }

    words = text.split()

    happy_score = sum(1 for w in words if w.strip(".,!?;:'\"()[]{}") in happy_words)
    sad_score = sum(1 for w in words if w.strip(".,!?;:'\"()[]{}") in sad_words)

    if happy_score > sad_score:
        return "happy"
    elif sad_score > happy_score:
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
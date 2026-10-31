from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from groq import Groq
from pydantic import BaseModel, ValidationError

load_dotenv()
client = Groq()
app = FastAPI()

SYSTEM_PROMPT = """You are a fitness coach.
Return ONLY JSON in this exact shape:
{"plan": [
  {"day": "Monday", "exercise": "Squats", "reps": 10},
  {"day": "Monday", "exercise": "Push-ups", "reps": 12}
]}
Use one entry per exercise, repeating the day for each exercise.
Create exactly the number of training days requested.
Respect the user's equipment and any limitations."""


class PlanRequest(BaseModel):
    goal: str
    level: str
    days: int
    equipment: str
    limitations: str | None = None


class Exercise(BaseModel):
    exercise: str
    reps: int


class PlanItem(BaseModel):
    day: str
    exercise: str
    reps: int


class GroqPlan(BaseModel):
    plan: list[PlanItem]


@app.get("/")
def home():
    return {"message": "Workout planner API is running"}


@app.post("/plan")
def create_plan(req: PlanRequest) -> list[PlanItem]:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.model_dump_json()},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    raw = response.choices[0].message.content
    try:
        return GroqPlan.model_validate_json(raw).plan
    except ValidationError as e:
        raise HTTPException(status_code=502, detail=f"Model returned bad JSON: {e}")
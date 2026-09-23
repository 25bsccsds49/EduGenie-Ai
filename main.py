from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import settings
from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description=(
        "AI-powered educational assistant for Q&A, "
        "explanations, quizzes, summaries and learning paths."
    ),
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


# =========================================================
# TEMPLATES
# =========================================================

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# =========================================================
# REQUEST MODELS
# =========================================================

class TaskRequest(BaseModel):

    task: Literal[
        "explain",
        "qa",
        "quiz",
        "summarize",
        "recommend",
    ]

    text: str = Field(
        min_length=1,
        max_length=20000,
    )


class TaskResponse(BaseModel):

    task: str
    result: object


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name,
        },
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": settings.gemini_configured,
        "local_explainer_enabled": (
            settings.local_explainer_enabled
        ),
    }


# =========================================================
# Q&A
# =========================================================

@app.post("/qa", response_model=TaskResponse)
async def qa(payload: TaskRequest):

    validate_task(payload, "qa")

    try:

        result = answer_question(payload.text)

        return TaskResponse(
            task="qa",
            result=result,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=safe_error(exc),
        )


# =========================================================
# EXPLANATION
# =========================================================

@app.post("/explain", response_model=TaskResponse)
async def explain(payload: TaskRequest):

    validate_task(payload, "explain")

    try:

        result = explain_concept(payload.text)

        return TaskResponse(
            task="explain",
            result=result,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=safe_error(exc),
        )


# =========================================================
# QUIZ
# =========================================================

@app.post("/quiz", response_model=TaskResponse)
async def quiz(payload: TaskRequest):

    validate_task(payload, "quiz")

    try:

        result = generate_quiz(payload.text)

        return TaskResponse(
            task="quiz",
            result=result,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=safe_error(exc),
        )


# =========================================================
# SUMMARIZE
# =========================================================

@app.post("/summarize", response_model=TaskResponse)
async def summarize(payload: TaskRequest):

    validate_task(payload, "summarize")

    try:

        result = summarize_text(payload.text)

        return TaskResponse(
            task="summarize",
            result=result,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=safe_error(exc),
        )


# =========================================================
# LEARNING RECOMMENDATIONS
# =========================================================

@app.post(
    "/learn/recommendations",
    response_model=TaskResponse,
)
async def recommendations(payload: TaskRequest):

    validate_task(payload, "recommend")

    try:

        result = get_learning_recommendations(
            payload.text
        )

        return TaskResponse(
            task="recommend",
            result=result,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=safe_error(exc),
        )


# =========================================================
# UNIFIED API ENDPOINT
# =========================================================

@app.post(
    "/api/task",
    response_model=TaskResponse,
)
async def task_router(payload: TaskRequest):

    if payload.task == "qa":
        return await qa(payload)

    if payload.task == "explain":
        return await explain(payload)

    if payload.task == "quiz":
        return await quiz(payload)

    if payload.task == "summarize":
        return await summarize(payload)

    if payload.task == "recommend":
        return await recommendations(payload)

    raise HTTPException(
        status_code=400,
        detail="Unknown task.",
    )


# =========================================================
# VALIDATION
# =========================================================

def validate_task(
    payload: TaskRequest,
    expected: str,
) -> None:

    if payload.task != expected:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Expected task '{expected}', "
                f"received '{payload.task}'."
            ),
        )

    if not payload.text.strip():

        raise HTTPException(
            status_code=400,
            detail="Input cannot be empty.",
        )


# =========================================================
# ERROR HANDLING
# =========================================================

def safe_error(exc: Exception) -> str:

    message = str(exc).strip()

    if not message:

        return (
            "The AI service returned "
            "an unknown error."
        )

    return message[:1000]

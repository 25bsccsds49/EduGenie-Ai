# EduGenie

## Google Gemini Powered Learning Assistant

EduGenie is an AI-powered educational assistant built with:

- Python
- FastAPI
- Google Gemini
- LaMini-Flan-T5
- HTML
- CSS
- JavaScript

The system supports:

- Question answering
- Concept explanation
- Quiz generation
- Text summarization
- Personalized learning paths


# Features

## 1. Question Answering

Students can ask academic questions.

Example:

What is photosynthesis?

EduGenie generates a concise educational answer.


## 2. Concept Explanation

Students can enter a difficult concept.

Example:

Explain recursion.

The application attempts to use:

LaMini-Flan-T5

and falls back to Gemini when necessary.


## 3. Quiz Generator

EduGenie creates:

- 3 questions
- 4 options per question
- One correct answer
- Explanation for the answer


## 4. Summarization

Students can paste educational material.

EduGenie creates a concise revision summary.


## 5. Learning Path

Students can enter a topic such as:

Python

SQL

Machine Learning

Biology

Physics

EduGenie creates a beginner-to-advanced learning path.


# Project Structure

EduGenie/

    main.py

    config.py

    gemini_client.py

    explanation_module.py

    qna.py

    quiz_module.py

    summary_module.py

    learning_path.py

    requirements.txt

    .env

    .env.example

    .gitignore

    pytest.ini

    README.md

    templates/
        index.html

    static/
        style.css
        app.js

    tests/
        test_api.py


# Requirements

Python 3.10 or newer.

A Gemini API key is required for:

- Q&A
- Quiz
- Summary
- Learning Path
- Gemini explanation fallback


# Installation

## Step 1

Open the EduGenie folder in VS Code.


## Step 2

Open the VS Code terminal.


## Step 3

Create virtual environment.

Windows PowerShell:

    py -3.10 -m venv .venv

Activate:

    .\.venv\Scripts\Activate.ps1


Windows CMD:

    py -3.10 -m venv .venv

Activate:

    .venv\Scripts\activate


macOS/Linux:

    python3 -m venv .venv

Activate:

    source .venv/bin/activate


# Step 4

Upgrade pip:

    python -m pip install --upgrade pip


# Step 5

Install dependencies:

    pip install -r requirements.txt


# Step 6

Create `.env`

Copy:

    .env.example

to:

    .env


Then add your Gemini API key:

    GEMINI_API_KEY=your_real_api_key


# Step 7

Run the application

    uvicorn main:app --reload


# Step 8

Open browser

    http://127.0.0.1:8000


# API Documentation

FastAPI automatically provides Swagger documentation.

Open:

    http://127.0.0.1:8000/docs


# Health Check

Open:

    http://127.0.0.1:8000/health


# API Endpoints

POST:

    /qa

POST:

    /explain

POST:

    /quiz

POST:

    /summarize

POST:

    /learn/recommendations

POST:

    /api/task


GET:

    /health


# Testing

Run:

    pytest


The tests check:

- Home page
- Health endpoint
- Request validation


# If LaMini-Flan-T5 is too heavy

Open `.env`.

Change:

    LOCAL_EXPLAINER_ENABLED=true

to:

    LOCAL_EXPLAINER_ENABLED=false


Then:

    uvicorn main:app --reload

Explanations will use Gemini instead.


# Port Problem

If port 8000 is already being used:

    uvicorn main:app --reload --port 8001

Then open:

    http://127.0.0.1:8001


# PowerShell Activation Problem

If PowerShell does not allow virtual environment activation, use:

    .venv\Scripts\python.exe -m pip install -r requirements.txt

Then:

    .venv\Scripts\python.exe -m uvicorn main:app --reload


# Architecture

Browser

    ↓

FastAPI

    ↓

Task Router

    ↓

--------------------------------

| Q&A

| Explanation

| Quiz

| Summary

| Learning Path

--------------------------------

    ↓

Gemini API

and

LaMini-Flan-T5

    ↓

Educational Response


# Educational Workflow

Student enters learning material.

        ↓

Student selects task.

        ↓

Frontend sends request.

        ↓

FastAPI receives request.

        ↓

Appropriate AI module is selected.

        ↓

Gemini / local model processes request.

        ↓

Response is validated.

        ↓

FastAPI returns result.

        ↓

Frontend displays result.


# Future Improvements

Possible future versions can add:

- Voice input
- Multilingual learning
- Student accounts
- Progress tracking
- Gamification
- Adaptive learning
- Image input
- PDF upload
- Learning history
- Notifications
- LMS integration
- Mobile application
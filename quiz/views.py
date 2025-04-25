# views.py
from django.shortcuts import render
import openai  # For OpenAI API, you'll need to install the package: pip install openai
from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

import json

def index(request):
    """Render the index page with the quiz generation form."""
    return render(request, 'index.html')

def generate_quiz(request):
    """Generate quiz questions using OpenAI's API and render the quiz page."""
    if request.method == "POST":
        topic = request.POST.get('topic', '')
        difficulty = request.POST.get('difficulty', 'medium')
        num_questions = int(request.POST.get('num_questions', 10))
        
        # Limit number of questions to a reasonable range
        num_questions = max(5, min(num_questions, 20))
        
        # Generate the quiz questions
        quiz_questions = generate_questions_with_openai(topic, difficulty, num_questions)
        
        context = {
            'topic': topic,
            'difficulty': difficulty,
            'quiz_questions': quiz_questions
        }
        
        return render(request, 'quiz_results.html', context)
    
    # If not POST, redirect to index
    return render(request, 'index.html')

def generate_questions_with_openai(topic: str,
                                   difficulty: str,
                                   num_questions: int) -> list[dict]:
    """
    Generate multiple-choice quiz questions with Sutra-Light.
    Returns: [{question:str, options:{option_1:str,…}, answer:str}, …]
    """
    try:
        print("INSIDE OPENAI")

        client = OpenAI(
            base_url="https://api.two.ai/v2",
            api_key=os.getenv("SUTRA_API_KEY"),
        )

        # ---------- PROMPT --------------------------------------------------
        prompt = f"""
You are a Google-certified instructional designer.

Create **{num_questions}** {difficulty.lower()}-level MCQs on **{topic}**.
Each object in the JSON array MUST look exactly like this template
and MUST be valid JSON (no comments, no trailing commas):

{{
  "question": "The text of the question?",
  "options": {{
    "option_1": "first answer choice",
    "option_2": "second answer choice",
    "option_3": "third answer choice",
    "option_4": "fourth answer choice"
  }},
  "answer": "option_2"   // key of the correct option above
}}

Return **only** the JSON array – nothing else.
"""
        # --------------------------------------------------------------------

        stream = client.chat.completions.create(
            model="sutra-light",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that generates quiz questions."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=2048,
            temperature=0.7,
            stream=True,
        )

        chunks = []
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                chunks.append(delta)

        content = "".join(chunks)
        print("GENERATED:", content[:200] + ("…" if len(content) > 200 else ""))

        # ---------- JSON PARSING -------------------------------------------
        try:
            questions = json.loads(content)
        except json.JSONDecodeError:
            # fallback 1 – extract first […] block
            match = re.search(r"\[[\s\S]*?]", content)
            if match:
                questions = json.loads(match.group(0))
            else:
                # fallback 2 – give up gracefully
                raise ValueError("Model did not return valid JSON.")

        # ---------- VALIDATION / NORMALISATION -----------------------------
        formatted = []
        for q in questions:
            # the model might nest options under "question" – fix that:
            if isinstance(q.get("question"), dict) and not q.get("options"):
                q["options"], q["question"] = q["question"], "QUESTION_TEXT_MISSING"

            # ensure required keys
            if not all(k in q for k in ("question", "options", "answer")):
                continue

            formatted.append({
                "question": q["question"],
                "options": q["options"],
                "answer": q["answer"],
            })

        # Ensure we return the exact amount requested
        if len(formatted) < num_questions:
            print("Warning: fewer items than requested; filling with placeholders.")
            while len(formatted) < num_questions:
                formatted.append({
                    "question": f"Placeholder question on {topic}",
                    "options": {f"option_{i}": f"Answer {i}" for i in range(1, 5)},
                    "answer": "option_1",
                })

        return formatted[:num_questions]

    # -------------------- ERROR HANDLING -----------------------------------
    except Exception as exc:
        print(f"Error generating questions: {exc}")
        return [{
            "question": f"Unable to generate quiz on {topic}.",
            "options": {f"option_{i}": "—" for i in range(1, 5)},
            "answer": "option_1",
        }]
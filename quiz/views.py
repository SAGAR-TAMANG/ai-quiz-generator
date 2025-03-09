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

def generate_questions_with_openai(topic, difficulty, num_questions):
    """
    Generate quiz questions using OpenAI's API.
    
    Args:
        topic (str): The topic for the quiz.
        difficulty (str): The difficulty level (easy, medium, hard).
        num_questions (int): The number of questions to generate.
        
    Returns:
        list: A list of dictionaries with questions and answers.
    """
    try:
        print("INSIDE OPENAI")
        sutra_url = 'https://api.two.ai/v2'
        client = OpenAI(base_url=sutra_url, api_key=os.getenv("SUTRA_API_KEY"))
        
        # Create the prompt for OpenAI
        prompt = f"""
        Generate {num_questions} quiz questions about {topic} at a {difficulty} difficulty level.
        Each question should have a clear answer.
        Format the response as a JSON array of objects, each with 'question' and 'answer' fields.
        """
        

        # Call OpenAI API
        stream = client.chat.completions.create(
            model='sutra-light',
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates quiz questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
            stream=True
        )

        chunks = []

        for chunk in stream:
            message_chunk = chunk.choices[0].delta.content

            if len(chunk.choices) > 0:
                content = chunk.choices[0].delta.content
                if content:
                    chunks.append(message_chunk)

        content = ''.join(chunks)
        print(f"GENERATED: {content}")


        # Extract and parse the response
        # content = response.choices[0].message.content
        
        # Try to find JSON in the response
        try:
            # First attempt: try to parse the entire response as JSON
            questions = json.loads(content)
            
            print(f"QUESTIONS: {questions}")
        except json.JSONDecodeError:
            # Second attempt: try to extract JSON from the text
            # This is a fallback in case the AI includes explanatory text
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                questions = json.loads(json_match.group(0))
            else:
                # If JSON parsing fails, create a simple format manually
                questions = []
                lines = content.split('\n')
                question = None
                for line in lines:
                    if line.strip().startswith(('Q', 'Question')):
                        if question:
                            questions.append(question)
                        question = {'question': line.split(':', 1)[1].strip() if ':' in line else line.strip(), 'answer': ''}
                    elif line.strip().startswith(('A', 'Answer')) and question:
                        question['answer'] = line.split(':', 1)[1].strip() if ':' in line else line.strip()
                if question and question['answer']:
                    questions.append(question)
        
        # Ensure we have the expected format
        formatted_questions = []
        for item in questions:
            if isinstance(item, dict) and 'question' in item and 'answer' in item:
                formatted_questions.append({
                    'question': item['question'],
                    'answer': item['answer']
                })
        
        return formatted_questions[:num_questions]
    
    except Exception as e:
        # In case of any error, return some default questions
        print(f"Error generating questions: {e}")
        return [
            {'question': f'Question about {topic} (Error occurred while generating quiz)', 
             'answer': 'Please try again later.'}
        ]
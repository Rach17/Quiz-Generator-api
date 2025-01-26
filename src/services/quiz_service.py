from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from models.schemas import QuizSchema, QuestionSchema
from config import settings
from typing import List
import json
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert quiz generator. Generate {num_questions} questions based on the following context.
Each question should have 4 options and one correct answer. Format the response as valid JSON.

Context:
{context}

JSON Format:
{{
  "quiz": [
    {{
      "question": "question text",
      "options": ["option1", "option2", "option3", "option4"],
      "correct_answer": "optionX"
    }}
  ]
}}
"""

async def generate_quiz(
    context: str,
    num_questions: int = 5,
    difficulty: str = "medium"
) -> QuizSchema:
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "Additional requirements: Difficulty level - {difficulty}")
        ])

        # Create processing chain
        chain = prompt | llm

        # Generate quiz
        response = await chain.ainvoke({
            "context": context,
            "num_questions": num_questions,
            "difficulty": difficulty
        })

        # Parse and validate response
        try:
            quiz_data = json.loads(response.content)
            questions = [
                QuestionSchema(**q) for q in quiz_data["quiz"]
            ]
            return QuizSchema(
                topic="Generated Quiz",
                difficulty=difficulty,
                questions=questions
            )
            
        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response")
            raise ValueError("Invalid response format from AI model")
            
    except Exception as e:
        logger.error(f"Quiz generation failed: {str(e)}")
        raise
from models.schemas import  QuestionSchema, QuizSchema
from config import settings
from langchain_core.prompts import PromptTemplate
import json
import logging
from utils.llm_utils import init_llm_model
from services.vector_store_service import get_random_doc

logger = logging.getLogger(__name__)


QUIZ_PROMPT_TEMPLATE = PromptTemplate(
        input_variables=["context", "difficulty"],
        template=
            """
            You are an expert quiz generator. Create 1 multiple-choice question.
            Context:{context}
            
            Requirements:
            - Generate 4 options for the question
            - Difficulty: {difficulty}
            - Avoid mentioning "according to the text" in the question
        """
    ) 


async def create_question(collection_name : str, difficulty: str) -> QuestionSchema:
    try:
        print("Generating question...")
        print("Initiating LLM model...")
        llm_model = init_llm_model()
        print("Getting random document...")
        doc_context = await get_random_doc(collection_name)
        context = doc_context.page_content
        print("Initiating chain...")
        model = llm_model.with_structured_output(QuestionSchema)
        chain = QUIZ_PROMPT_TEMPLATE | model
        print("Invoking chain...")
        response = await chain.ainvoke({"context": context, "difficulty": difficulty})
        print("Question generated successfully")
        return response

    except json.JSONDecodeError:
        logger.error("Failed to parse LLM response")
        raise ValueError("Invalid response format from AI model")
    except Exception as e:
        logger.error("Quiz generation failed: %s", str(e))
        raise
    
    
async def create_quiz(collection_name: str, difficulty: str, questions_number: int) -> QuizSchema:
    questions = []
    for i in range(questions_number):
        try:
            print(f"Generating question {i+1}...")
            question = await create_question(collection_name, difficulty)
            print(f"Question {i+1} generated successfully")
            questions.append(question)
        except Exception as e:
            logger.error("Quiz generation failed: %s", str(e))
            raise
        
    quizz = QuizSchema(name=collection_name, difficulty=difficulty, questions=questions)
    return quizz
from models.schemas import  QuestionSchema, QuizSchema
from config import settings
from langchain_core.prompts import PromptTemplate
import json
import logging
from utils.llm_utils import init_llm_model
from services.collection_service import get_random_doc

logger = logging.getLogger(__name__)


QUIZ_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["context", "difficulty", "language"],
    template="""
                You are a knowledgeable quiz expert. Based on the context provided below, generate one multiple-choice question in {language}.

                Context:
                {context}

                Instructions:
                - Create one clear, well-structured question at a {difficulty} difficulty level.
                - Provide 4 distinct answer options for the question, ensuring one option is correct and the others are plausible distractors.
                - Avoid phrases such as "according to the text" or any similar references.
            """
        )

async def create_question(collection_name : str, difficulty: str) -> QuestionSchema:
    try:
        logger.info("Getting random document from collection...")
        doc = await get_random_doc(collection_name)
        doc_content, language = doc.get("doc") , doc.get("lang")
        context = doc_content.page_content
        logger.info("Initiating LLM model...")
        llm_model = init_llm_model()
        model = llm_model.with_structured_output(QuestionSchema)
        chain = QUIZ_PROMPT_TEMPLATE | model
        logger.info("Generating question...")
        response = await chain.ainvoke({"context": context, "difficulty": difficulty, "language": language})
        return response

    except json.JSONDecodeError:
        logger.error("Failed to parse LLM response")
        raise ValueError("Invalid response format from AI model")
    except Exception as e:
        logger.error("Quiz generation failed: %s", str(e))
        raise
    
    
async def create_quiz(collection_name: str, difficulty: str , questions_number: int ) -> QuizSchema:
    questions = []
    for i in range(questions_number):
        try:
            question = await create_question(collection_name, difficulty)
            questions.append(question)
        except Exception as e:
            logger.error("Quiz generation failed: %s", str(e))
            raise
    
    logging.info("Quiz generated successfully")
    quizz = QuizSchema(name=collection_name, difficulty=difficulty, questions=questions)
    return quizz

async def event_quiz_generation(collection_name: str, difficulty: str, questions_number: int):
        for i in range(questions_number):
                try:
                    # Generate one question at a time.
                    question = await create_question(collection_name, difficulty)
                    # Convert the question (which is a Pydantic model) to JSON.
                    yield {"event": "new_question", "data": question.json()}
                except Exception as e:
                    logger.error("Quiz generation failed: %s", str(e))
                    yield {"event": "error", "data": "Failed to generate quiz. Please try again."}
            # Signal that the quiz generation is complete.
        yield {"event": "done", "data": "Quiz generation completed"}
    
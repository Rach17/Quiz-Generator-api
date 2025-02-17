from langchain_core.prompts import PromptTemplate


QUIZ_PROMPT_TEMPLATE = PromptTemplate(
        input_variables=["context", "difficulty", "language"],
        template="""
                    Generate 1 {difficulty}-level multiple-choice question in {language} about:
                    {context}

                    Format strictly as:
                    Question: [Your question here]
                    A) [Option1]
                    B) [Option2]
                    C) [Option3]
                    D) [Option4]
                    Answer: [Letter]

                    Rules:
                    - No "according to text" references
                    - Plausible distractors only
                """
) 

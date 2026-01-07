from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# --- LLM-as-a-judge grading schema ---

def llm_grade_question(question: str, context: str, model_name: str = "gpt-4") -> Dict:
    """Grade a question using the EvalResult schema (LLM-as-a-judge)."""
    llm = ChatOpenAI(model=model_name, temperature=0)
    prompt = ChatPromptTemplate.from_template(
        """
        You are a product expert. Evaluate the following question about the product context.

        Product Context: {context}
        Question: {question}

        Respond in JSON using this schema:
        {{
            "relevance_score": float,  # 0-1, how relevant is the question to the product?
            "safety_pass": bool,       # Is the question safe and appropriate?
            "specificity_score": float, # 0-1, how specific is the question?
            "reasoning": str           # Brief explanation for the grade
        }}
        """
    )
    chain = prompt | llm
    response = chain.invoke({"context": context, "question": question})
    # Parse and return JSON (assume response.content is JSON)
    import json
    return json.loads(response.content)

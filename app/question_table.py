import streamlit as st
import pandas as pd
import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from question_generator import generate_base_questions, evaluate_question_simple
from llm_grader import llm_grade_question
from rag_graph import create_enhanced_rag_graph, run_rag_query

def show_question_table():
    import streamlit as st
    import pandas as pd
    import random
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    from question_generator import generate_base_questions, evaluate_question_simple
    from llm_grader import llm_grade_question
    from rag_graph import create_enhanced_rag_graph, run_rag_query
    # Generate 20 random questions each time
    base_questions = generate_base_questions()
    if len(base_questions) < 20:
        questions = [q + f" ({i})" for i in range(20) for q in base_questions]
        questions = random.sample(questions, 20)
    else:
        questions = random.sample(base_questions, 20)
    from question_generator import load_product_context
    context = load_product_context()
    rows = []
    graph = create_enhanced_rag_graph()
    for q in questions:
        ragas_eval = evaluate_question_simple(q, context)
        llm_eval = llm_grade_question(q, context)
        answer = run_rag_query(graph, q)["answer"]
        rows.append({
            "Question": q,
            "Coverage": ragas_eval.coverage,
            "Specificity": ragas_eval.specific,
            "Insight": ragas_eval.insight,
            "Grounded": ragas_eval.grounded,
            "RAGAS Overall": ragas_eval.overall_score,
            "LLM Relevance": llm_eval.get("relevance_score", 0),
            "LLM Specificity": llm_eval.get("specificity_score", 0),
            "LLM Safety": llm_eval.get("safety_pass", False),
            "LLM Reasoning": llm_eval.get("reasoning", ""),
            "Answer": answer[:300]
        })
    df = pd.DataFrame(rows)
    st.set_page_config(page_title="Question Table", layout="wide")
    st.title("🧠 Question Table (Randomized)")
    st.write("Each time you load this page, 20 random questions are generated and evaluated with metrics, LLM grader, and answers.")
    st.dataframe(df, use_container_width=True)

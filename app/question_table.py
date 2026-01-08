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
    """Enhanced question table with real metrics from datasets."""
    import streamlit as st
    import pandas as pd
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    # Use enhanced question generator with real datasets
    try:
        from enhanced_question_generator import generate_enhanced_questions
        st.write("🔍 Using enhanced question generator with real datasets...")
        questions_with_metrics = generate_enhanced_questions(100)
    except ImportError as e:
        st.error(f"Enhanced generator not available: {e}")
        return
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return
    
    # Debug: Print number of questions generated
    st.write(f"🔍 Debug: Generated {len(questions_with_metrics)} questions")
    
    # Prepare data for table
    rows = []
    for q_data in questions_with_metrics:
        metrics = q_data['metrics']
        llm_eval = q_data['llm_eval']
        
        rows.append({
            "Question": q_data['question'],
            "Coverage": round(metrics['coverage'], 3),
            "Specificity": round(metrics['specificity'], 3),
            "Insight": round(metrics['insight'], 3),
            "Grounded": round(metrics['grounded'], 3),
            "LLM_Relevance": round(llm_eval.get('relevance_score', 0), 3),
            "LLM_Specificity": round(llm_eval.get('specificity_score', 0), 3),
            "Source": q_data.get('context_source', 'Unknown'),
            "All_Metrics_Above_0.7": "✅ Yes" if q_data['passes_threshold'] else "❌ No"
        })
    
    df = pd.DataFrame(rows)
    
    # Debug: Print final dataframe size
    st.write(f"🔍 Debug: Final dataframe has {len(df)} rows")
    
    st.markdown("### 📊 Enhanced Question Quality Analysis")
    st.markdown("Showing 100 questions generated from **real datasets** using **BM25 + Semantic retrieval** with **RAGAS/LLM-based metrics**. Only questions with **ALL metrics > 0.7** will appear in the main chat interface.")
    
    # Display the table
    st.dataframe(df, use_container_width=True)
    
    # Show statistics
    high_quality_count = sum(1 for row in rows if row["All_Metrics_Above_0.7"] == "✅ Yes")
    st.markdown(f"### 📈 Quality Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("High Quality Questions", f"{high_quality_count}/100", f"{high_quality_count}%")
    
    with col2:
        avg_coverage = sum(row["Coverage"] for row in rows) / len(rows)
        st.metric("Average Coverage", f"{avg_coverage:.3f}")
    
    with col3:
        avg_insight = sum(row["Insight"] for row in rows) / len(rows)
        st.metric("Average Insight", f"{avg_insight:.3f}")
    
    with col4:
        avg_llm_relevance = sum(row["LLM_Relevance"] for row in rows) / len(rows)
        st.metric("Avg LLM Relevance", f"{avg_llm_relevance:.3f}")
    
    # Show source distribution
    source_counts = {}
    for row in rows:
        source = row["Source"]
        source_counts[source] = source_counts.get(source, 0) + 1
    
    st.markdown("### 📚 Source Distribution")
    for source, count in sorted(source_counts.items()):
        st.write(f"**{source}**: {count} questions")
    
    # Show only high quality questions
    if high_quality_count > 0:
        st.markdown("### 🎯 High Quality Questions (All Metrics > 0.7)")
        high_quality_df = df[df["All_Metrics_Above_0.7"] == "✅ Yes"]
        st.dataframe(high_quality_df, use_container_width=True)
    else:
        st.info("🔍 No questions currently meet the >0.7 threshold for all metrics. The question generation system may need tuning.")
    
    # Show methodology
    with st.expander("🔬 Methodology", expanded=False):
        st.markdown("""
        **Question Generation Process:**
        1. **Dataset Retrieval**: Uses BM25 + Semantic search on real datasets (dataset_1 & dataset_2)
        2. **Question Generation**: Creates hypothetical questions from retrieved chunks
        3. **RAGAS Metrics**: Evaluates coverage, specificity, insight, groundedness
        4. **LLM Grading**: Additional evaluation using LLM-based grader
        5. **Quality Filter**: Only questions with ALL metrics > 0.7 are high quality
        
        **Metrics Explanation:**
        - **Coverage**: How well the question relates to the retrieved context
        - **Specificity**: How specific vs generic the question is
        - **Insight**: Whether the question asks for deeper understanding
        - **Grounded**: How grounded the question is in the actual data
        - **LLM Relevance**: LLM-based relevance scoring
        - **LLM Specificity**: LLM-based specificity scoring
        """)

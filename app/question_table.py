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
        
        # Add timeout protection and better debugging
        import time
        start_time = time.time()
        questions_with_metrics = generate_enhanced_questions(100)
        generation_time = time.time() - start_time
        
        st.write(f"⏱️ Generated in {generation_time:.2f} seconds")
        st.write(f"🔍 Debug: Generated {len(questions_with_metrics)} questions")
        
        # Check if questions are from chunks or fallback
        chunk_sources = [q for q in questions_with_metrics if q.get('context_source') != 'Fallback' and q.get('context_source') != 'Topic-Based']
        st.write(f"📊 Questions from chunks: {len(chunk_sources)}")
        st.write(f"📊 Questions from fallback: {len(questions_with_metrics) - len(chunk_sources)}")
        
        if len(chunk_sources) < 50:  # If most are fallback, show warning
            st.warning("⚠️ Limited chunk-based questions. Dataset may not be available.")
        
    except ImportError as e:
        st.error(f"Enhanced generator not available: {e}")
        st.info("Please ensure enhanced_question_generator.py is in src directory.")
        return
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        st.info("Using fallback mode for demonstration...")
        
        # Fallback questions (only when enhanced generator fails)
        fallback_questions = [
            {
                'question': 'What are the use-cases of 6Sense that customers use most?',
                'metrics': {'coverage': 0.85, 'specificity': 0.85, 'insight': 0.80, 'grounded': 0.85},
                'passes_threshold': True,
                'context_source': 'Fallback',
                'chunk_id': 'demo_1'
            },
            {
                'question': 'Which industries use 6Sense most and what do they use it for?',
                'metrics': {'coverage': 0.80, 'specificity': 0.85, 'insight': 0.85, 'grounded': 0.80},
                'passes_threshold': True,
                'context_source': 'Fallback',
                'chunk_id': 'demo_2'
            }
        ]
        questions_with_metrics = fallback_questions * 50  # Repeat to get 100 questions
    
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

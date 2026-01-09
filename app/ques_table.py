import streamlit as st
import pandas as pd
import requests
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def show_question_table():
    """Enhanced question table using data-driven generation from API."""
    import streamlit as st
    import pandas as pd
    import requests
    import time
    
    st.title("📋 Question Table")
    st.write("Questions generated using RAG graph from actual data")
    
    # API Configuration
    API_URL = os.getenv("API_URL", "https://cuspera-rag-platform-production.railway.app")
    
    # Generation controls
    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("Topic (optional)", placeholder="e.g., predictive analytics, features, implementation")
    with col2:
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, value=10)
    
    # Generate button
    if st.button("🚀 Generate Questions from RAG Data"):
        with st.spinner("Generating questions using RAG graph..."):
            try:
                start_time = time.time()
                
                # Call API to generate questions
                response = requests.post(
                    f"{API_URL}/generate-questions",
                    json={"topic": topic if topic else None, "num_questions": num_questions},
                    timeout=30
                )
                
                generation_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status") == "success":
                        questions = data.get("questions", [])
                        method = data.get("generation_method", "Unknown")
                        source = data.get("data_source", "Unknown")
                        
                        st.success(f"✅ Generated {len(questions)} questions in {generation_time:.2f}s using {method}")
                        st.info(f"📊 Data Source: {source}")
                        
                        # Display questions in table
                        if questions:
                            df = pd.DataFrame(questions)
                            
                            # Prepare display columns
                            display_cols = ['question']
                            
                            # Add metrics columns if available
                            if 'metrics' in questions[0]:
                                metric_cols = ['coverage', 'specificity', 'insight', 'grounded', 'overall_score']
                                display_cols.extend(metric_cols)
                            
                            # Add LLM evaluation if available
                            if 'llm_eval' in questions[0]:
                                llm_cols = ['relevance_score', 'answerability_score', 'clarity_score', 'insight_score']
                                display_cols.extend(llm_cols)
                            
                            # Add metadata columns
                            if 'context_source' in questions[0]:
                                display_cols.extend(['context_source', 'reasoning'])
                            
                            # Filter to only available columns
                            available_cols = [col for col in display_cols if col in df.columns]
                            
                            # Display the table
                            st.dataframe(
                                df[available_cols],
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "question": st.column_config.TextColumn("Question", width="large"),
                                    "coverage": st.column_config.ProgressColumn("Coverage", format="%.2f"),
                                    "specificity": st.column_config.ProgressColumn("Specificity", format="%.2f"),
                                    "insight": st.column_config.ProgressColumn("Insight", format="%.2f"),
                                    "grounded": st.column_config.ProgressColumn("Grounded", format="%.2f"),
                                    "overall_score": st.column_config.ProgressColumn("Overall", format="%.2f"),
                                    "relevance_score": st.column_config.ProgressColumn("Relevance", format="%.2f"),
                                    "answerability_score": st.column_config.ProgressColumn("Answerability", format="%.2f"),
                                    "clarity_score": st.column_config.ProgressColumn("Clarity", format="%.2f"),
                                    "insight_score": st.column_config.ProgressColumn("LLM Insight", format="%.2f"),
                                    "context_source": st.column_config.TextColumn("Source", width="medium"),
                                    "reasoning": st.column_config.TextColumn("Reasoning", width="large")
                                }
                            )
                            
                            # Statistics
                            st.subheader("📊 Generation Statistics")
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Total Questions", len(questions))
                            with col2:
                                st.metric("Generation Method", method)
                            with col3:
                                st.metric("Data Source", source)
                            with col4:
                                st.metric("Generation Time", f"{generation_time:.2f}s")
                            
                            # Metrics summary
                            if 'metrics' in questions[0]:
                                st.subheader("📈 Quality Metrics Summary")
                                metric_cols = ['coverage', 'specificity', 'insight', 'grounded', 'overall_score']
                                
                                for metric in metric_cols:
                                    if metric in df.columns:
                                        values = df[metric].tolist()
                                        st.metric(
                                            f"Avg {metric.title()}",
                                            f"{sum(values)/len(values):.3f}",
                                            delta=f"{min(values):.3f} - {max(values):.3f}"
                                        )
                        
                        else:
                            st.warning("⚠️ No questions generated")
                    else:
                        st.error(f"❌ Generation failed: {data.get('error', 'Unknown error')}")
                        
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to API. Please check API URL.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()

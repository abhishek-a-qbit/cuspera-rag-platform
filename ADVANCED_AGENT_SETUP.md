# Advanced AI Agent Installation Guide

## 🚀 **New Features Added**

### ✅ **Completed:**
1. **LangGraph Integration** - State management and chat memory
2. **Amazon Rufus-style Interface** - Interactive question cards
3. **Rich Context Display** - Sources and metrics in chat responses
4. **Intent Detection** - Basic navigation routing

### 🔄 **In Progress:**
- Dynamic code execution engine
- Advanced visualization generation

## 📦 **Installation Steps**

### 1. Install New Dependencies
```bash
# Activate your virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install LangGraph and updated dependencies
pip install langgraph>=0.0.26

# Install all requirements (including updated ones)
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
# Check if LangGraph is available
python -c "from langgraph.graph import StateGraph; print('✅ LangGraph installed')"

# Check if spaCy model is available
python -c "import spacy; spacy.load('en_core_web_sm'); print('✅ spaCy model ready')"
```

### 3. Start the Backend
```bash
# Start the API backend
python api_backend_simple.py
```

### 4. Start the Frontend
```bash
# In a new terminal, start Streamlit
streamlit run app/cuspera_working.py
```

## 🎯 **How to Use the New Features**

### **Amazon Rufus-style Chat Interface**
1. Generate questions in the **Question Generator** page
2. Navigate to the **Chat Assistant** page
3. Click on any question card to chat about it
4. View rich responses with sources and metrics

### **Enhanced Chat Features**
- **Question Cards**: Interactive cards with quality scores
- **Source Attribution**: Retrieved documents with match percentages
- **Quality Metrics**: Coverage, specificity, insightfulness, groundedness
- **Follow-up Questions**: AI-suggested next questions
- **Chat Memory**: Persistent conversation history

### **Intent Detection**
The agent now detects when you want to:
- Navigate to analytics, reports, or other pages
- Generate visualizations or dashboards
- Ask for code generation
- General chat about the data

## 🔧 **Architecture Overview**

```
🤖 Advanced AI Agent
├── LangGraph (State Management)
│   ├── Chat Memory
│   ├── Tool Routing
│   └── Context Persistence
├── Amazon Rufus Interface
│   ├── Question Cards
│   ├── Rich Responses
│   └── Interactive Elements
├── Intent Detection
│   ├── Page Navigation
│   ├── Code Generation
│   └── Dynamic Routing
└── Enhanced Metrics
    ├── Source Attribution
    ├── Quality Scores
    └── Visual Analytics
```

## 📊 **What's Next**

### **Phase 2: Dynamic Code Execution**
- Python sandbox for data analysis
- HTML/CSS/JS generation
- Interactive dashboard creation
- PowerPoint-like visualizations

### **Phase 3: Advanced Features**
- Multi-modal responses
- Advanced analytics
- Custom templates
- Export capabilities

## 🐛 **Troubleshooting**

### **Common Issues:**

1. **LangGraph Import Error**
   ```bash
   pip install langgraph>=0.0.26
   ```

2. **spaCy Model Missing**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Memory Issues**
   - Restart the backend
   - Clear browser cache
   - Check available RAM

4. **Chat Interface Not Loading**
   - Check if `rufus_chat_interface.py` is in the `app/` folder
   - Verify all dependencies are installed
   - Check browser console for errors

## 🎨 **Customization**

### **Add Custom Intents**
Edit `src/advanced_ai_agent.py` in the `_detect_intent` method:
```python
# Add your custom intents here
if "dashboard" in query_lower:
    state["code_execution"] = {"type": "dashboard", "query": user_query}
```

### **Custom Question Cards**
Edit `app/rufus_chat_interface.py` in the `display_question_card` function:
```python
# Customize card styling and content
```

### **Add New Metrics**
Extend the metrics calculation in `src/data_driven_question_generator.py`:
```python
# Add your custom metrics here
```

## 📞 **Support**

If you encounter issues:
1. Check the installation steps above
2. Verify all dependencies are installed
3. Check the backend logs for errors
4. Restart both backend and frontend

---

**🎉 Your Advanced AI Agent is ready!** 

The system now has state management, Amazon Rufus-style interface, and enhanced chat capabilities. Enjoy the improved user experience!

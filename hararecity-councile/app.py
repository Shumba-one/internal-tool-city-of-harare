import streamlit as st
import os
from dotenv import load_dotenv
from utils.rag_engine import ChatEngine

# Set Groq API key
os.environ["GROQ_API_KEY"] = "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"

# Load environment variables
load_dotenv()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Page configuration
st.set_page_config(
    page_title="Harare City Council IT Support",
    page_icon="🏛️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
    }
    .response-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .error-box {
        background-color: #ffebee;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ffcdd2;
        margin: 20px 0;
    }
    .coming-soon {
        background-color: #fff3e0;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ffe0b2;
        margin: 20px 0;
        text-align: center;
    }
    .model-training {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #c8e6c9;
        margin: 20px 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🏛️ Harare City Council IT Support")

# Initialize chat engine
@st.cache_resource
def get_chat_engine():
    try:
        return ChatEngine()
    except ValueError as e:
        st.error(f"""
            Configuration Error: {str(e)}
            Please ensure you have created a .env file in the project root with the following variable:
            GROQ_API_KEY=your_groq_api_key
        """)
        st.stop()

try:
    chat_engine = get_chat_engine()
    st.markdown("Welcome to the IT Support Assistant. How can I help you today?")

    # Chat interface
    user_query = st.text_area("Enter your IT-related question:", height=100)

    if st.button("Submit Question"):
        if user_query:
            with st.spinner("Processing your question..."):
                try:
                    # Get response from chat engine
                    response, _ = chat_engine.get_response(user_query)
                    
                    # Display response
                    st.markdown("### Response")
                    st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
                    
                    # Display sources (Coming Soon)
                    st.markdown("### Sources")
                    st.markdown("""
                        <div class="coming-soon">
                            <h4>🔜 Coming Soon</h4>
                            <p>Document source tracking and reference system is under development.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "query": user_query,
                        "response": response
                    })
                    
                    # Feedback mechanism
                    st.markdown("### Was this response helpful?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("👍 Yes"):
                            st.success("Thank you for your feedback!")
                    with col2:
                        if st.button("👎 No"):
                            st.info("We're sorry the response wasn't helpful. Please try rephrasing your question or contact the IT support team directly.")
                except Exception as e:
                    error_message = str(e)
                    if "model_not_found" in error_message:
                        st.markdown("""
                            <div class="model-training">
                                <h3>🔄 System Update in Progress</h3>
                                <p>We are currently collecting and processing data to train our IT support model.</p>
                                <p>Please check back later when we have completed the training process.</p>
                                <p><em>Note: The current API key has expired. We will update it once the model is ready.</em></p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"An error occurred: {error_message}")

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### Previous Questions")
        for chat in reversed(st.session_state.chat_history):
            with st.expander(f"Q: {chat['query']}"):
                st.markdown(f"**Response:** {chat['response']}")
                st.markdown("""
                    <div class="coming-soon">
                        <h4>🔜 Coming Soon</h4>
                        <p>Source references and document links will be available here soon.</p>
                    </div>
                """, unsafe_allow_html=True)

    # Additional Features Section
    st.markdown("---")
    st.markdown("### Additional Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Document Upload")
        st.markdown("""
            <div class="coming-soon">
                <h4>🔜 Coming Soon</h4>
                <p>Upload IT documentation and manuals for better support.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Knowledge Base")
        st.markdown("""
            <div class="coming-soon">
                <h4>🔜 Coming Soon</h4>
                <p>Access the IT knowledge base and documentation.</p>
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    error_message = str(e)
    if "model_not_found" in error_message:
        st.markdown("""
            <div class="model-training">
                <h3>🔄 System Update in Progress</h3>
                <p>We are currently collecting and processing data to train our IT support model.</p>
                <p>Please check back later when we have completed the training process.</p>
                <p><em>Note: The current API key has expired. We will update it once the model is ready.</em></p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"An error occurred: {error_message}")

# Footer
st.markdown("---")
st.markdown("© 2024 Harare City Council - Internal Use Only") 
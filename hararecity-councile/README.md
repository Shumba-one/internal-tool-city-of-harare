# Harare City Council IT Support Assistant

An intelligent IT support system for Harare City Council employees that provides context-aware answers to IT-related queries using RAG (Retrieval-Augmented Generation) technology.

## Features

- Interactive web interface for submitting IT queries
- Real-time response generation using LangChain and OpenAI
- Document retrieval from Pinecone vector database
- Source document highlighting
- User feedback mechanism
- Branded interface matching Harare City Council guidelines

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

- `app.py`: Main Streamlit application
- `utils/`: Utility functions and helpers
  - `document_processor.py`: Document processing and embedding
  - `rag_engine.py`: RAG implementation
- `data/`: Directory for storing documents and embeddings
- `static/`: Static assets (images, CSS)

## Contributing

Please follow the Harare City Council's internal guidelines for contributing to this project.

## License

Internal use only - Harare City Council 
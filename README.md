# WhatsApp Chat Analyzer with RAG

A comprehensive Streamlit-based application that analyzes WhatsApp chat exports and provides AI-powered question answering using Retrieval-Augmented Generation (RAG). The application combines statistical analysis with semantic search capabilities to help users understand their chat history.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Key Components](#key-components)
- [RAG Pipeline Deep Dive](#rag-pipeline-deep-dive)
- [Analysis Pipeline](#analysis-pipeline)
- [Technical Decisions](#technical-decisions)
- [Future Improvements](#future-improvements)

## ✨ Features

### Analysis Features
- **Statistical Analysis**: Message counts, word counts, media shared, links shared
- **Timeline Visualization**: Monthly and daily message timelines
- **Activity Maps**: Busiest days of the week and months
- **User Analytics**: Most active users, user participation percentages
- **Word Analysis**: Word clouds and most common words
- **Emoji Analysis**: Most frequently used emojis with visualizations

### RAG Features
- **Semantic Search**: Ask questions about your chat history using natural language
- **Context-Aware Answers**: AI generates answers based on retrieved chat context
- **Time-Based Chunking**: Intelligent conversation grouping by time gaps
- **Multi-Format Support**: Handles both 24-hour and 12-hour (AM/PM) time formats

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  ┌──────────────────┐        ┌──────────────────┐        │
│  │  Analysis View    │        │   Chat View       │        │
│  │  - Statistics    │        │   - RAG Query     │        │
│  │  - Visualizations│        │   - Chat History  │        │
│  └──────────────────┘        └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Preprocessing Layer                       │
│  - WhatsApp Export Parser                                   │
│  - Time Format Detection (24h/12h)                          │
│  - DataFrame Creation                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌──────────────────────┐    ┌──────────────────────┐
│   Analysis Pipeline  │    │    RAG Pipeline      │
│                      │    │                      │
│  - Helper Functions  │    │  - Time Slicing      │
│  - Statistics       │    │  - Embedding         │
│  - Visualizations   │    │  - Vector Store      │
│  - Charts           │    │  - LLM Generation    │
└──────────────────────┘    └──────────────────────┘
```

### Component Architecture

```
app.py (Main Entry Point)
├── utils/
│   ├── rag_utils.py          # RAG initialization & caching
│   └── sidebar_utils.py      # UI view toggling
├── views/
│   ├── analysis_view.py      # Analysis dashboard
│   └── chat_view.py          # RAG chat interface
├── preprocessor.py           # WhatsApp export parsing
├── helper.py                 # Analysis helper functions
└── rag_src/
    ├── main.py               # RAG orchestrator
    ├── chunking/
    │   └── time_slicer.py    # Time-based chunking
    ├── slice_text.py         # Text formatting
    ├── embeding.py           # Embedding generation
    ├── store.py              # ChromaDB operations
    └── llm.py                # Gemini LLM integration
```

## 🛠️ Tech Stack

### Frontend
- **Streamlit** (v1.49.1): Web framework for building the UI
- **Matplotlib**: Chart generation
- **Seaborn**: Statistical visualizations
- **WordCloud**: Word cloud generation

### Backend & Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations
- **Python 3.x**: Core language

### RAG & ML Components
- **SentenceTransformers**: Text embedding generation (`all-MiniLM-L6-v2`)
- **ChromaDB**: Vector database for similarity search
- **Google Gemini API**: LLM for answer generation (`gemma-3-12b-it`)

### Utilities
- **URLExtract**: URL extraction from messages
- **Emoji**: Emoji detection and analysis
- **Regex**: Pattern matching for parsing

## 📁 Project Structure

```
whatsapp-analyser/
├── steam-bro/                    # Main application directory
│   ├── app.py                    # Main Streamlit app entry point
│   ├── preprocessor.py          # WhatsApp export parser
│   ├── helper.py                 # Analysis helper functions
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── rag_utils.py         # RAG initialization utilities
│   │   └── sidebar_utils.py     # Sidebar UI components
│   ├── views/
│   │   ├── __init__.py
│   │   ├── analysis_view.py     # Analysis dashboard view
│   │   └── chat_view.py         # RAG chat interface view
│   └── rag_src/                 # RAG pipeline modules
│       ├── __init__.py
│       ├── main.py               # RAG class orchestrator
│       ├── embeding.py          # Embedding generation
│       ├── slice_text.py        # Text formatting
│       ├── store.py             # ChromaDB vector store
│       ├── llm.py               # Gemini LLM wrapper
│       └── chunking/
│           ├── __init__.py
│           └── time_slicer.py   # Time-based chunking logic
├── requirements.txt              # Python dependencies
├── README.md                    # This file
└── WhatsApp Chat *.txt          # Sample chat exports
```

## 🔄 How It Works

### 1. File Upload & Preprocessing

When a user uploads a WhatsApp chat export:

1. **File Reading**: Raw text file is read and decoded
2. **Format Detection**: Auto-detects 24-hour vs 12-hour (AM/PM) format
3. **Parsing**: Regex patterns extract dates, users, and messages
4. **DataFrame Creation**: Structured data with columns:
   - `date`: Parsed datetime
   - `user`: Message sender
   - `message`: Message content
   - `year`, `month`, `day`, `hour`, `minute`: Time features
   - `day_name`, `period`: Derived features

### 2. Analysis Pipeline

**User selects "Analysis" view:**

1. User selects a user (or "Overall") from dropdown
2. Clicks "Show analysis" button
3. Helper functions compute:
   - Basic stats (messages, words, media, links)
   - Timelines (monthly, daily)
   - Activity maps (busy days/months)
   - User rankings
   - Word clouds and common words
   - Emoji frequency
4. Results displayed as charts and dataframes

### 3. RAG Pipeline

**User selects "Chat" view:**

#### Initialization (One-time, when file uploaded):

1. **Data Preparation**: Convert DataFrame to list of tuples `(user, message, date)`
2. **Time Slicing**: `TimeSlicer` groups messages by 30-minute gaps
   - Messages within 30 minutes → same conversation slice
   - Gap > 30 minutes → new slice
3. **Text Formatting**: Convert slices to readable text format
   - Format: `"User: message\nUser2: message2"`
4. **Embedding**: Generate 384-dimensional vectors using SentenceTransformer
5. **Storage**: Store embeddings + metadata in ChromaDB

#### Query Processing (Every user question):

1. **Query Embedding**: Convert user question to embedding vector
2. **Similarity Search**: Find top 5 most similar chunks from ChromaDB
3. **Context Extraction**: Extract text from retrieved chunks
4. **Prompt Building**: Combine query + context + instructions
5. **LLM Generation**: Send prompt to Gemini, get answer
6. **Response Display**: Show answer in chat interface

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd whatsapp-analyser
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up Gemini API Key**
   - Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Add to `steam-bro/rag_src/llm.py`:
   ```python
   genai.configure(api_key="YOUR_API_KEY_HERE")
   ```
   Or set environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```

5. **Run the application**
```bash
cd steam-bro
streamlit run app.py
```

6. **Access the app**
   - Open browser to `http://localhost:8501`
   - Upload a WhatsApp chat export file

## 💻 Usage

### Exporting WhatsApp Chat

1. Open WhatsApp chat (individual or group)
2. Tap three dots → More → Export chat
3. Choose "Without Media"
4. Save the `.txt` file

### Using the Application

1. **Upload File**: Use sidebar file uploader
2. **Wait for Processing**: RAG system initializes (may take 30-60 seconds)
3. **Choose View**:
   - **Analysis**: Click "📊 Analysis" button
     - Select user from dropdown
     - Click "Show analysis"
     - View statistics and visualizations
   - **Chat**: Click "💬 Chat" button
     - Type questions in chat input
     - Get AI-powered answers about your chat

### Example Questions for RAG

- "Who are the users in this chat?"
- "What topics were discussed recently?"
- "What did [user name] say about [topic]?"
- "When was [event] mentioned?"
- "Summarize the main discussions"

## 🔧 Key Components

### Preprocessor (`preprocessor.py`)

**Purpose**: Parse WhatsApp chat exports into structured DataFrame

**Key Features**:
- Auto-detects time format (24-hour vs 12-hour)
- Handles both formats with appropriate regex patterns
- Extracts dates, users, messages
- Creates time-based features (year, month, day, hour, etc.)

**Regex Patterns**:
- 24-hour: `r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"`
- 12-hour: `r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(am|pm|AM|PM)\s-\s"`

**Datetime Formats**:
- 24-hour: `"%d/%m/%Y, %H:%M - "`
- 12-hour: `"%d/%m/%Y, %I:%M %p - "`

### Helper Functions (`helper.py`)

**Purpose**: Statistical analysis and visualization helpers

**Functions**:
- `fetch_stats()`: Basic statistics (messages, words, media, links)
- `most_busy_users()`: User activity ranking
- `monthly_timeline()`: Monthly message counts
- `daily_timeline()`: Daily message counts
- `week_activity_map()`: Day-of-week activity
- `month_activity_map()`: Month activity
- `create_word_cloud()`: Word cloud generation
- `most_common_words()`: Top words analysis
- `emoji_helper()`: Emoji frequency analysis

### Time Slicer (`rag_src/chunking/time_slicer.py`)

**Purpose**: Group messages into conversation chunks based on time gaps

**Algorithm**:
1. Start with first message as current slice
2. For each subsequent message:
   - Calculate time difference from previous message
   - If difference ≤ 30 minutes → add to current slice
   - If difference > 30 minutes → start new slice
3. Return list of slices

**Why Time-Based?**
- Preserves conversation context
- Groups related messages together
- Better semantic coherence than fixed-size chunks

### Embedding (`rag_src/embeding.py`)

**Purpose**: Convert text to numerical vectors for similarity search

**Model**: `all-MiniLM-L6-v2` from SentenceTransformers
- 384-dimensional vectors
- Multilingual support
- Fast inference
- Good semantic understanding

**Process**:
```python
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts)  # Returns numpy array
```

### Vector Store (`rag_src/store.py`)

**Purpose**: Store and query embeddings using ChromaDB

**Operations**:
- `add_embeddings()`: Store embeddings with metadata
- `query()`: Find similar embeddings using cosine similarity

**Storage Structure**:
- `ids`: Unique identifiers
- `embeddings`: Vector representations
- `metadatas`: `{source, start_time, text}`
- `documents`: Text content for easy retrieval

**Query Process**:
1. Convert query to embedding
2. Compute cosine similarity with all stored embeddings
3. Return top-K most similar chunks

### LLM Integration (`rag_src/llm.py`)

**Purpose**: Generate natural language answers using Gemini

**Model**: `gemma-3-12b-it` (Gemini)
- 12B parameter model
- Good instruction following
- Handles context well

**Process**:
1. Receive prompt with query + context
2. Generate response
3. Return text answer

### RAG Orchestrator (`rag_src/main.py`)

**Purpose**: Coordinate the entire RAG pipeline

**Class: RAG**

**Initialization** (`__init__`):
1. Time slicing
2. Text formatting
3. Metadata creation
4. Embedding generation
5. ChromaDB storage

**Query Processing** (`ask_query`):
1. Query embedding
2. Similarity search
3. Prompt building
4. LLM generation
5. Answer return

**Prompt Building** (`_build_prompt`):
- Extracts text from retrieved chunks
- Formats context clearly
- Provides clear instructions to LLM
- Prevents hallucination

## 🔍 RAG Pipeline Deep Dive

### Why RAG?

**Problem**: LLMs have limited context windows and training data cutoff dates. They can't access your specific chat history.

**Solution**: RAG combines:
- **Retrieval**: Find relevant parts of your chat
- **Augmentation**: Add that context to the prompt
- **Generation**: LLM generates answer using your data

### Step-by-Step RAG Flow

```
1. User Question: "Who are the users in this chat?"
   │
   ▼
2. Query Embedding
   Input: "Who are the users in this chat?"
   Model: SentenceTransformer
   Output: [0.23, -0.45, 0.67, ..., 0.12] (384-dim vector)
   │
   ▼
3. Vector Similarity Search
   Database: ChromaDB (all chat chunks)
   Method: Cosine similarity
   Top-K: 5 most similar chunks
   │
   ▼
4. Retrieved Context
   Chunk 1: "Charan Rkv: Hey everyone\nBalaji: Hi there..."
   Chunk 2: "Nishit: Welcome to the group..."
   Chunk 3: "Akshit: Here's the API key..."
   ...
   │
   ▼
5. Prompt Construction
   """
   User Question: Who are the users in this chat?
   
   Relevant Chat Context:
   Chunk 1: Charan Rkv: Hey everyone...
   Chunk 2: Nishit: Welcome...
   ...
   
   Instructions: Answer based on context...
   """
   │
   ▼
6. LLM Generation
   Model: Gemini
   Input: Complete prompt
   Output: "Based on the chat history, the users are: 
            Charan Rkv, Balaji, Nishit, Akshit..."
   │
   ▼
7. Display Answer
   User sees natural language response
```

### Embedding Similarity Explained

**Cosine Similarity**:
- Measures angle between vectors, not distance
- Range: -1 (opposite) to 1 (identical)
- Formula: `cos(θ) = (A · B) / (||A|| × ||B||)`

**Why It Works**:
- Semantically similar text → similar vectors → high similarity
- Example:
  - Query: "users in chat"
  - Chunk: "Charan Rkv, Balaji, Nishit are members"
  - High similarity → retrieved

### Chunking Strategy

**Time-Based Chunking**:
- Groups messages by conversation continuity
- 30-minute gap threshold
- Preserves context better than fixed-size chunks

**Alternative Approaches Considered**:
- Fixed-size chunks (e.g., 100 tokens): Loses conversation flow
- Sentence-based: Too granular, loses context
- Semantic chunking: More complex, time-based works well for chats

## 📊 Analysis Pipeline

### Statistical Computations

**Basic Stats** (`fetch_stats`):
- Message count: `df.shape[0]`
- Word count: Split messages, count words
- Media count: Count `"<Media omitted>\n"` messages
- Link count: Use URLExtract to find URLs

**Timeline Analysis**:
- Monthly: Group by `(year, month)`, count messages
- Daily: Group by `only_date`, count messages

**Activity Maps**:
- Week activity: `df['day_name'].value_counts()`
- Month activity: `df['month'].value_counts()`

**User Analysis**:
- Busiest users: `df['user'].value_counts()`
- Percentage: `(user_count / total_messages) * 100`

**Word Analysis**:
- Filter out notifications and media messages
- Remove stop words (optional)
- Count word frequency
- Generate word cloud

**Emoji Analysis**:
- Extract emojis using `emoji` library
- Count frequency
- Display top emojis

## 🎯 Technical Decisions

### Why Streamlit?

**Pros**:
- Rapid prototyping
- Built-in widgets (file upload, charts, chat)
- Python-only (no frontend knowledge needed)
- Good for data apps

**Cons**:
- Less customizable than React
- Performance limitations for large apps
- State management can be tricky

**Alternative Considered**: React + FastAPI, but Streamlit faster for MVP

### Why Time-Based Chunking?

**Advantages**:
- Preserves conversation context
- Natural grouping (people reply within time windows)
- Better semantic coherence

**Trade-offs**:
- Variable chunk sizes (some very small, some large)
- May split long conversations
- Fixed-size chunks would be more predictable

### Why SentenceTransformer over OpenAI Embeddings?

**Reasons**:
- **Free**: No API costs
- **Local**: Works offline
- **Fast**: No network latency
- **Good Quality**: `all-MiniLM-L6-v2` performs well
- **Multilingual**: Handles mixed languages

**Trade-offs**:
- OpenAI embeddings might be slightly better
- But cost and latency not worth it for this use case

### Why ChromaDB?

**Advantages**:
- Simple API
- In-memory option (fast)
- Good Python integration
- Handles metadata well

**Alternatives**:
- Pinecone: Cloud-based, paid
- Weaviate: More complex
- FAISS: Lower-level, more setup needed

### Why Gemini over GPT?

**Reasons**:
- Free tier available
- Good performance
- Easy API
- Handles context well

**Model Choice**: `gemma-3-12b-it`
- Instruction-tuned
- Good for RAG tasks
- Reasonable response time

## 🚧 Future Improvements

### Short-term
1. **Better Filtering**: Remove notifications and media before RAG
2. **Multilingual Embeddings**: Use `paraphrase-multilingual-MiniLM-L12-v2` for better Telugu/Hindi support
3. **Chunk Size Optimization**: Experiment with different time gaps (10min, 1hr)
4. **Error Handling**: Better error messages and fallbacks
5. **Caching**: Cache analysis results to avoid recomputation

### Medium-term
1. **Hybrid Search**: Combine semantic search with keyword search
2. **Re-ranking**: Use cross-encoder to re-rank retrieved chunks
3. **Conversation Memory**: Remember previous questions in chat
4. **Export Results**: Download analysis as PDF/CSV
5. **User Filtering in RAG**: Filter chunks by specific users

### Long-term
1. **Multi-file Support**: Analyze multiple chat files together
2. **Real-time Updates**: Support live chat analysis
3. **Advanced Analytics**: Sentiment analysis, topic modeling
4. **Custom Models**: Fine-tune embedding model on chat data
5. **Deployment**: Deploy to cloud (Streamlit Cloud, AWS, etc.)

## 📝 Code Quality & Best Practices

### Modular Design
- Separated concerns: preprocessing, analysis, RAG
- Reusable components
- Easy to test individual modules

### Error Handling
- Try-except blocks in critical paths
- Graceful degradation
- User-friendly error messages

### Performance Optimizations
- Streamlit caching (`@st.cache_resource`)
- Session state management
- Efficient DataFrame operations

### Code Organization
- Clear file structure
- Descriptive function names
- Comments where needed
- Type hints (can be added)

## 🐛 Known Issues & Limitations

1. **Large Files**: Very large chat files (>100MB) may be slow
2. **Memory**: ChromaDB stores in memory, large chats use more RAM
3. **API Limits**: Gemini API has rate limits
4. **Language Support**: Better for English, mixed languages may need improvements
5. **Chunking**: 30-minute gap may not work for all conversation patterns

## 📚 Dependencies

Key dependencies (see `requirements.txt` for full list):
- `streamlit==1.49.1`: Web framework
- `pandas==2.3.2`: Data manipulation
- `sentence-transformers`: Embedding generation
- `chromadb`: Vector database
- `google-generativeai`: Gemini API
- `matplotlib==3.10.6`: Charting
- `wordcloud==1.9.4`: Word clouds
- `emoji==2.14.1`: Emoji handling

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

## 📄 License

[Add your license here]

## 👤 Author

[Your Name]

---

## 🎓 Interview Preparation Notes

### Architecture Questions
- **Monolithic vs Microservices**: Currently monolithic (single Streamlit app), could be split into API + frontend
- **Scalability**: Current design works for single user, would need changes for multi-user
- **Database**: Using ChromaDB (in-memory), could use persistent storage for production

### Technical Deep Dives
- **Embedding Dimensions**: 384-dim chosen for balance between quality and speed
- **Top-K Retrieval**: 5 chunks chosen empirically, could be tuned
- **Time Gap**: 30 minutes chosen based on typical conversation patterns

### Design Patterns Used
- **Factory Pattern**: RAG initialization
- **Strategy Pattern**: Different views (Analysis vs Chat)
- **Singleton Pattern**: ChromaDB client (implicit)

### Performance Considerations
- **Embedding Generation**: Most time-consuming step (~10-30s for large chats)
- **ChromaDB Query**: Fast (<100ms)
- **LLM Generation**: Depends on API (~2-5s)

### Security Considerations
- **API Keys**: Currently hardcoded (should use env vars)
- **File Upload**: No validation (should add file size/type checks)
- **Data Privacy**: All processing local, no data sent externally except to Gemini API

---

**Last Updated**: February 2025

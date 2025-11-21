# GROQ API Setup with LlamaIndex

## Why GROQ?

GROQ provides fast inference for open-source LLMs, making it ideal for RAG applications:
- **Fast**: Up to 10x faster than traditional APIs
- **Cost-effective**: Lower costs than OpenAI
- **Open-source models**: Llama 3.1, Mixtral, Gemma
- **High throughput**: Handles many concurrent requests

## Setup

1. **Get GROQ API Key**:
   - Sign up at https://console.groq.com/
   - Navigate to API Keys section
   - Create a new API key

2. **Configure `.env` file**:
   ```bash
   GROQ_API_KEY=your-groq-api-key-here
   GROQ_MODEL=llama-3.1-70b-versatile
   LLM_PROVIDER=groq
   ```

3. **Available Models**:
   - `llama-3.1-70b-versatile` - Best for complex tasks (recommended)
   - `llama-3.1-8b-instant` - Fast, good for simple tasks
   - `mixtral-8x7b-32768` - Large context window (32k tokens)
   - `gemma2-9b-it` - Google's Gemma model

## Usage in Code

The LLM is automatically configured based on `LLM_PROVIDER` setting:

```python
from app.services.llm_setup import get_llm

# Get LLM instance (GROQ or OpenAI based on config)
llm = get_llm()

# Use with LlamaIndex
from llama_index.core import VectorStoreIndex, ServiceContext
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(llm=llm)
```

## Switching Between Providers

To switch back to OpenAI:
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-key
```

## Benefits for SummarIQ

- **Faster paper processing**: Quick entity extraction and summarization
- **Lower costs**: More affordable for research workloads
- **Better for RAG**: Fast inference improves query response times
- **Open-source**: No vendor lock-in

## Rate Limits

GROQ has generous rate limits:
- Free tier: 30 requests/minute
- Paid tier: Higher limits available

Check current limits at: https://console.groq.com/docs/rate-limits


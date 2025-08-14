# MOSDAC Chatbot Documentation

### Overview: 
The MOSDAC Chatbot simplifies access to meteorological and oceanographic data using a local RAG pipeline, knowledge graph, and planned Flask UI, ensuring security and interpretability.

### Usage:
- Run: python MVP_V_1_1.py to crawl MOSDAC, build graphs, and start terminal Q&A.
- Q&A: Enter queries (e.g., “INSAT-3D revisit time?”) or type exit to quit.
- Outputs:
  - Text: mvp_data_v2/raw_text/*.txt
  - Metadata: mvp_data_v2/metadata/*.json
  - Graph: mvp_data_v2/graph/knowledge_graph.png
- Planned UI: Flask-based login/chat (templates/ not in repo).
- Demo: Google Drive Video

### Technical Notes

- Crawling: Playwright scrapes MOSDAC URLs (update targets in code).
- Knowledge Graph: spaCy extracts entities; NetworkX/Neo4j (planned) stores graphs.
- RAG Pipeline: LangChain with Mistral 7B and FAISS for secure, efficient Q&A.
- Storage: MongoDB (planned) for users.json, chats.json.
- Portability: Modular design for ISRO, DRDO websites.
- Voice: Future Bhashini LLM integration.

### Setup

1. Clone: git clone https://github.com/your-username/mosdac-hackathon
2. Env: conda create -n py310 python=3.10; conda activate py310
3. Install: pip install flask requests beautifulsoup4 playwright pdfplumber spacy networkx matplotlib langchain langchain-community langchain-text-splitters faiss-cpu sentence-transformers
4. Playwright: playwright install
5. spaCy: python -m spacy download en_core_web_sm
6. Ollama: ollama run mistral

### Notes

- Ensure valid MOSDAC URLs in targets.
- Neo4j/MongoDB integration in progress for enhanced storage.

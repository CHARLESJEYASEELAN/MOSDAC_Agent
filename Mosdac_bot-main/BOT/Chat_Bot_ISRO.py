from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import json
import os
import asyncio
import logging
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import pdfplumber
import spacy
import networkx as nx
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.documents import Document
import matplotlib.pyplot as plt
import re
from typing import List, Dict

# Configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)

# Flask app setup
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# File-based storage
USERS_FILE = 'users.json'
CHATS_FILE = 'chats.json'

def load_json_file(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_json_file(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)

class MOSDACMVP:
    def __init__(self, start_url: str, output_dir: str = "mvp_data_v2"):
        self.start_url = start_url
        self.output_dir = output_dir
        self.text_data = []
        self.metadata = []
        self.nlp = spacy.load("en_core_web_sm")
        self.graph = nx.DiGraph()
        self.llm = Ollama(model="mistral", base_url="http://localhost:11434")
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Create output directories
        os.makedirs(os.path.join(output_dir, "raw_text"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "metadata"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "graph"), exist_ok=True)

    async def scrape_page(self, url: str, playwright) -> tuple:
        """Scrape a single page using Playwright."""
        logging.info(f"Scraping: {url}")
        try:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"
            )
            page = await context.new_page()
            await page.goto(url, timeout=120000, wait_until="networkidle")
            html_content = await page.content()
            await browser.close()
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text(separator=" ", strip=True)
            logging.info(f"Scraped {url}, text length: {len(text)}")
            return soup, text
        except Exception as e:
            logging.error(f"Failed to scrape {url}: {str(e)}")
            return None, ""

    def extract_pdf_text(self, url: str) -> str:
        """Extract text from a PDF file."""
        logging.info(f"Extracting PDF: {url}")
        try:
            response = requests.get(url, stream=True, timeout=30)
            if response.status_code == 200:
                with open("temp.pdf", "wb") as f:
                    f.write(response.content)
                with pdfplumber.open("temp.pdf") as pdf:
                    text = "".join(page.extract_text() or "" for page in pdf.pages)
                os.remove("temp.pdf")
                logging.info(f"Extracted PDF text, length: {len(text)}")
                return text
            else:
                logging.error(f"Failed to download PDF {url}: Status {response.status_code}")
                return ""
        except Exception as e:
            logging.error(f"Error extracting PDF {url}: {str(e)}")
            return ""

    def get_metadata(self, url: str, soup, content_type: str) -> Dict:
        """Extract metadata for a given URL."""
        last_updated = "Unknown"
        if soup:
            meta_tag = soup.find("meta", {"name": re.compile("last-modified|date", re.I)})
            if meta_tag and meta_tag.get("content"):
                last_updated = meta_tag["content"]
        return {
            "url": url,
            "type": content_type,
            "last_updated": last_updated,
            "format": content_type.lower()
        }

    async def crawl(self):
        """Crawl specific MOSDAC content if not already present."""
        targets = [
            ("https://www.mosdac.gov.in/about-us", "HTML"),
            ("https://www.mosdac.gov.in/documents/INSAT-3D.pdf", "PDF"),
            ("https://www.mosdac.gov.in/missions", "HTML")
        ]
        existing_files = os.listdir(os.path.join(self.output_dir, "raw_text"))
        async with async_playwright() as playwright:
            for url, content_type in targets:
                url_safe = url.replace("https://", "").replace("/", "_") + ".txt"
                if url_safe in existing_files:
                    logging.info(f"Reusing existing data for {url}")
                    with open(os.path.join(self.output_dir, "raw_text", url_safe), "r", encoding="utf-8") as f:
                        text = f.read()
                    self.text_data.append({"url": url, "content": text, "type": content_type})
                    metadata_file = max(
                        [f for f in os.listdir(os.path.join(self.output_dir, "metadata")) if f.startswith("metadata_")],
                        default=None
                    )
                    if metadata_file:
                        with open(os.path.join(self.output_dir, "metadata", metadata_file), "r", encoding="utf-8") as f:
                            metadata_list = json.load(f)
                            for meta in metadata_list:
                                if meta["url"] == url:
                                    self.metadata.append(meta)
                    continue
                if content_type == "HTML":
                    soup, text = await self.scrape_page(url, playwright)
                    if not text:
                        continue
                else:
                    text = self.extract_pdf_text(url)
                    soup = None
                if text:
                    self.text_data.append({"url": url, "content": text, "type": content_type})
                    self.metadata.append(self.get_metadata(url, soup, content_type))
                await asyncio.sleep(1)  # Rate limiting
        if self.text_data:
            self.save_data()

    def save_data(self):
        """Save raw text and metadata."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for item in self.text_data:
            url_safe = item["url"].replace("https://", "").replace("/", "_")
            with open(os.path.join(self.output_dir, "raw_text", f"{url_safe}.txt"), "w", encoding="utf-8") as f:
                f.write(item["content"])
        with open(os.path.join(self.output_dir, "metadata", f"metadata_{timestamp}.json"), "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)
        logging.info(f"Saved {len(self.text_data)} text files and metadata")

    def build_knowledge_graph(self):
        """Build a unimodal knowledge graph using spaCy and networkx."""
        if not os.path.exists(os.path.join(self.output_dir, "graph")):
            os.makedirs(os.path.join(self.output_dir, "graph"), exist_ok=True)
        for item in self.text_data:
            doc = self.nlp(item["content"])
            entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ("ORG", "GPE", "DATE", "PRODUCT")]
            for i, (ent1, label1) in enumerate(entities):
                self.graph.add_node(ent1, type=label1, source=item["url"])
                for ent2, label2 in entities[i+1:]:
                    self.graph.add_edge(ent1, ent2, relation="co-occurs", source=item["url"])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nx.write_graphml(self.graph, os.path.join(self.output_dir, "graph", f"knowledge_graph_{timestamp}.graphml"))
        logging.info(f"Built knowledge graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")

    def visualize_knowledge_graph(self):
        """Visualize the knowledge graph using Matplotlib."""
        try:
            graph_dir = os.path.join(self.output_dir, "graph")
            graph_files = [f for f in os.listdir(graph_dir) if f.startswith("knowledge_graph") and f.endswith(".graphml")]
            if not graph_files:
                logging.warning("No knowledge graph file found for visualization")
                return
            latest_graph = max(graph_files, key=lambda x: os.path.getmtime(os.path.join(graph_dir, x)))
            self.graph = nx.read_graphml(os.path.join(graph_dir, latest_graph))
            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(self.graph, k=0.5, iterations=50)
            entity_types = set(nx.get_node_attributes(self.graph, "type").values())
            colors = plt.cm.get_cmap("tab10", len(entity_types))
            type_to_color = {t: colors(i) for i, t in enumerate(entity_types)}
            node_colors = [type_to_color.get(self.graph.nodes[n]["type"], "grey") for n in self.graph.nodes]
            nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, node_size=800, alpha=0.8)
            nx.draw_networkx_edges(self.graph, pos, edge_color="grey", alpha=0.5)
            nx.draw_networkx_labels(self.graph, pos, font_size=10, font_weight="bold")
            edge_labels = nx.get_edge_attributes(self.graph, "relation")
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8)
            from matplotlib.lines import Line2D
            legend_elements = [
                Line2D([0], [0], marker='o', color='w', label=t, markerfacecolor=type_to_color[t], markersize=10)
                for t in entity_types
            ]
            plt.legend(handles=legend_elements, title="Entity Types", loc="upper right")
            output_path = os.path.join(self.output_dir, "graph", "knowledge_graph.png")
            plt.savefig(output_path, format="png", dpi=300, bbox_inches="tight")
            plt.close()
            logging.info(f"Saved knowledge graph visualization to {output_path}")
        except Exception as e:
            logging.error(f"Failed to visualize knowledge graph: {str(e)}")

    def setup_rag_pipeline(self):
        """Setup LangChain RAG pipeline with FAISS vector store."""
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
            documents = []
            for item in self.text_data:
                chunks = text_splitter.split_text(item["content"])
                for i, chunk in enumerate(chunks):
                    graph_context = self.get_graph_context_for_url(item["url"])
                    documents.append(Document(
                        page_content=chunk,
                        metadata={"url": item["url"], "chunk_id": f"{item['url']}_{i}", "graph_context": graph_context}
                    ))
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            self.vector_store = FAISS.from_documents(documents, embeddings)
            prompt_template = """You are a helpful assistant answering questions about MOSDAC data. Use the following context, which includes retrieved documents and related knowledge graph information, along with conversation history, to provide a concise, accurate answer.

Conversation History:
{chat_history}

Context:
{context}

Question: {question}
Answer: """
            prompt = PromptTemplate(
                input_variables=["chat_history", "context", "question"],
                template=prompt_template
            )
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
                memory=self.memory,
                combine_docs_chain_kwargs={
                    "prompt": prompt,
                    "document_prompt": PromptTemplate(
                        input_variables=["page_content", "graph_context"],
                        template="{page_content}\nGraph Context: {graph_context}"
                    )
                }
            )
            logging.info("RAG pipeline setup complete")
        except Exception as e:
            logging.error(f"Failed to setup RAG pipeline: {str(e)}")
            raise

    def get_graph_context_for_url(self, url: str) -> str:
        """Extract graph context for a specific URL."""
        graph_context = []
        for node in self.graph.nodes:
            if url in self.graph.nodes[node].get("source", ""):
                neighbors = list(self.graph.neighbors(node))
                if neighbors:
                    graph_context.append(f"{node} is related to: {', '.join(neighbors)}")
        return "; ".join(graph_context) if graph_context else "No graph context available"

    def answer_question(self, question: str) -> str:
        """Answer a question using the RAG pipeline."""
        try:
            result = self.qa_chain.invoke({"question": question})
            return result["answer"]
        except Exception as e:
            logging.error(f"Error answering question '{question}': {str(e)}")
            return "Sorry, I couldn't process your question due to an error. Please try again later."

# Initialize MOSDACMVP
mvp = MOSDACMVP(start_url="https://www.mosdac.gov.in/")
try:
    if os.path.exists(os.path.join(mvp.output_dir, "raw_text")) and len(os.listdir(os.path.join(mvp.output_dir, "raw_text"))) >= 3:
        logging.info("Found existing crawled data, loading...")
        asyncio.run(mvp.crawl())
    else:
        logging.info("No existing data found, crawling...")
        asyncio.run(mvp.crawl())
    mvp.build_knowledge_graph()
    mvp.visualize_knowledge_graph()
    mvp.setup_rag_pipeline()
except Exception as e:
    logging.error(f"Failed to initialize MOSDACMVP: {str(e)}")
    mvp = None

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('chatbot'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        users = load_json_file(USERS_FILE)
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = username
            session['username'] = user['username']
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials!'})
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    users = load_json_file(USERS_FILE)
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists!'})
    for user_data in users.values():
        if user_data.get('email') == email:
            return jsonify({'success': False, 'message': 'Email already registered!'})
    hashed_password = generate_password_hash(password)
    users[username] = {
        'username': username,
        'email': email,
        'password': hashed_password,
        'created_at': datetime.now().isoformat()
    }
    save_json_file(USERS_FILE, users)
    session['user_id'] = username
    session['username'] = username
    return jsonify({'success': True, 'message': 'Registration successful!'})

@app.route('/chatbot')
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('chatbot.html', username=session['username'])

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    data = request.get_json()
    message = data.get('message')
    if not mvp:
        return jsonify({'response': 'Error: MOSDACMVP not initialized. Please check server logs.'})
    bot_response = mvp.answer_question(message)
    chats = load_json_file(CHATS_FILE)
    user_id = session['user_id']
    if user_id not in chats:
        chats[user_id] = []
    chat_entry = {
        'user_message': message,
        'bot_response': bot_response,
        'timestamp': datetime.now().isoformat()
    }
    chats[user_id].append(chat_entry)
    save_json_file(CHATS_FILE, chats)
    return jsonify({'response': bot_response})

@app.route('/chat_history')
def chat_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    chats = load_json_file(CHATS_FILE)
    user_chats = chats.get(session['user_id'], [])
    return jsonify({'chats': user_chats})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("🚀 Starting MOSDAC ChatBot")
    print("📱 Application will be available at: http://localhost:5000")
    print("✨ Features: Login, Register, Chat with MOSDAC data, History")
    print("💾 Using file-based storage (users.json, chats.json, mvp_data_v2)")
    print("-" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
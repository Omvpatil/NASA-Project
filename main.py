import os
import warnings
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import requests
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import time
import json
from datetime import datetime
from database_manager import PaperDatabaseManager

# Suppress warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize FastAPI app
app = FastAPI(
    title="NASA Space Biology Knowledge Engine API",
    description="RAG-based API for searching NASA space biology research papers",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for vector store
vector_store = None
secondary_vector_store = None  # For abstract-based search
embeddings = None
db_manager = None  # Database manager for tracking papers

# Configuration
PERSIST_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "space_biology_papers"
CSV_URL = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publication_PMC.csv"
DB_PATH = "./papers.db"


# Pydantic Models
class SearchQuery(BaseModel):
    query: str = Field(..., description="Search query or question")
    num_results: int = Field(
        10, ge=1, le=50, description="Number of results to return")
    use_llm: bool = Field(
        True, description="Whether to use LLM for answer generation")
    google_api_key: Optional[str] = Field(
        None, description="Google API key for Gemini")
    model_name: str = Field("gemini-2.5-flash", description="LLM model to use")
    search_method: str = Field(
        "similarity", description="Search method: similarity, mmr, or similarity_score"
    )
    use_keyword_filter: bool = Field(
        False, description="Enable keyword filtering")
    keyword_filter: Optional[str] = Field(
        None, description="Comma-separated keywords for filtering"
    )


class SearchResponse(BaseModel):
    answer: Optional[str] = None
    source_documents: List[Dict[str, Any]]
    query: str
    num_results: int
    timestamp: str


class DocumentMetadata(BaseModel):
    title: str
    source: str
    pmcid: str


class DocumentResponse(BaseModel):
    page_content: str
    metadata: DocumentMetadata
    score: Optional[float] = None


class LoadPapersRequest(BaseModel):
    num_papers: int = Field(
        10, ge=1, le=607, description="Number of papers to load")


class LoadPapersResponse(BaseModel):
    status: str
    papers_loaded: int
    chunks_created: int
    message: str


class OnDemandSearchQuery(BaseModel):
    query: str = Field(..., description="Search query")
    num_results: int = Field(
        5, ge=1, le=20, description="Number of papers to retrieve")
    use_llm: bool = Field(True, description="Generate LLM answer")
    google_api_key: Optional[str] = Field(None, description="Google API key")
    model_name: str = Field("gemini-2.5-flash", description="LLM model")


class DatabaseStatus(BaseModel):
    status: str
    collection_name: str
    persist_directory: str
    total_chunks: int
    total_papers: int


# Helper Functions
def init_database():
    """Initialize SQLite database for tracking papers"""
    global db_manager
    if db_manager is None:
        db_manager = PaperDatabaseManager(DB_PATH)
    return db_manager


def load_csv():
    """Load papers CSV from GitHub"""
    return pd.read_csv(CSV_URL)


def scrape_article_text_with_images(article_url: str) -> Optional[tuple]:
    """Scrape article text and image URLs from PMC URL"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    try:
        page = requests.get(article_url, headers=headers, timeout=30)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "html.parser")

        # Get text
        main_content = soup.find(id="maincontent") or soup.find("article")
        if not main_content:
            main_content = soup

        paragraphs = main_content.find_all("p")
        text = "\n\n".join(p.get_text() for p in paragraphs)

        # Get images
        image_urls = scrape_article_images(article_url)

        return (text.strip(), image_urls)
    except Exception as e:
        print(f"Error scraping {article_url}: {e}")
        return None


def scrape_article_images(article_url: str) -> List[str]:
    """
    Scrape image URLs from PMC article

    Returns:
        List of image URLs found in the article
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        page = requests.get(article_url, headers=headers, timeout=30)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "html.parser")

        image_urls = []

        # Find all figure images
        figures = soup.find_all("figure") or soup.find_all(
            "div", class_="figure")
        for fig in figures:
            img = fig.find("img")
            if img and img.get("src"):
                img_url = img["src"]
                # Make absolute URL if relative
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
                elif img_url.startswith("/"):
                    from urllib.parse import urljoin

                    img_url = urljoin(article_url, img_url)
                image_urls.append(img_url)

        # Also check for images in main content
        main_content = soup.find(id="maincontent") or soup.find("article")
        if main_content:
            imgs = main_content.find_all("img")
            for img in imgs:
                if img.get("src"):
                    img_url = img["src"]
                    if img_url.startswith("//"):
                        img_url = "https:" + img_url
                    elif img_url.startswith("/"):
                        from urllib.parse import urljoin

                        img_url = urljoin(article_url, img_url)
                    if img_url not in image_urls:
                        image_urls.append(img_url)

        return image_urls
    except Exception as e:
        print(f"Error scraping images from {article_url}: {e}")
        return []


def scrape_article_abstract(article_url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    try:
        page = requests.get(article_url, headers=headers, timeout=30)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "html.parser")

        heading = soup.find(
            lambda tag: tag.name
            and tag.name.startswith("h")
            and tag.string
            and "abstract" in tag.string.lower()
        )

        if heading:
            abstract_paragraph = heading.find_next("p")
            if abstract_paragraph:
                return abstract_paragraph.get_text(strip=True)

        meta_abstract = soup.find("meta", {"name": "description"})
        if meta_abstract and meta_abstract.get("content"):
            return meta_abstract.get("content").strip()

        return None
    except Exception as e:
        print(f"Error scraping {article_url}: {e}")
        return None


def init_embeddings():
    """Initialize HuggingFace embeddings"""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def create_vectorstore(docs, embeddings_func, persist_dir, collection):
    """Create ChromaDB vector store"""
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings_func,
        persist_directory=persist_dir,
        collection_name=collection,
    )
    return vector_store


def load_existing_vectorstore(embeddings_func, persist_dir, collection):
    """Load existing ChromaDB vector store"""
    try:
        vs = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings_func,
            collection_name=collection,
        )
        collection_obj = vs._collection
        count = collection_obj.count()
        if count > 0:
            return vs, count
        return None, 0
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None, 0


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize embeddings and try to load existing database on startup"""
    global vector_store, embeddings, db_manager

    print("🚀 Starting NASA Space Biology Knowledge Engine API...")

    # Initialize SQLite database
    db_manager = init_database()
    print(f"✅ SQLite database initialized at {DB_PATH}")

    # Initialize embeddings
    embeddings = init_embeddings()
    print("✅ Embeddings initialized")

    # Try to load secondary (abstract) vector store
    global secondary_vector_store
    sec_vs, sec_count = load_existing_vectorstore(
        embeddings, "./small_persistent_db", "search_semantics"
    )
    if sec_vs:
        secondary_vector_store = sec_vs
        print(f"✅ Loaded secondary (abstract) database with {
              sec_count} chunks")
    else:
        print("⚠️ No secondary database found. Abstracts not indexed yet.")

    # Try to load existing vector store
    vs, count = load_existing_vectorstore(
        embeddings, PERSIST_DIRECTORY, COLLECTION_NAME
    )
    if vs:
        vector_store = vs
        print(f"✅ Loaded existing database with {count} chunks")
    else:
        print("⚠️ No existing database found. Use /load-papers endpoint to create one.")


# API Endpoints


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "NASA Space Biology Knowledge Engine API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "search": "/search (POST) - Smart search with automatic paper scraping and images",
            "load_papers": "/load-papers (POST)",
            "database_status": "/database-status",
            "papers_list": "/papers",
            "reset_database": "/reset-database (POST)",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database_loaded": vector_store is not None,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/database-status", response_model=DatabaseStatus)
async def get_database_status():
    """Get current database status"""
    if not vector_store:
        raise HTTPException(status_code=404, detail="Database not loaded")

    collection = vector_store._collection
    total_chunks = collection.count()

    # Get unique papers
    all_results = collection.get(include=["metadatas"])
    unique_papers = set()
    for metadata in all_results["metadatas"]:
        pmcid = metadata.get("pmcid", "N/A")
        if pmcid != "N/A":
            unique_papers.add(pmcid)

    return DatabaseStatus(
        status="loaded",
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
        total_chunks=total_chunks,
        total_papers=len(unique_papers),
    )


@app.get("/papers")
async def list_papers():
    """List all papers in the database"""
    if not vector_store:
        raise HTTPException(status_code=404, detail="Database not loaded")

    collection = vector_store._collection
    all_results = collection.get(include=["metadatas"])

    unique_papers = {}
    for metadata in all_results["metadatas"]:
        title = metadata.get("title", "Unknown")
        pmcid = metadata.get("pmcid", "N/A")
        source = metadata.get("source", "Unknown")
        if pmcid not in unique_papers:
            unique_papers[pmcid] = {"title": title,
                                    "pmcid": pmcid, "source": source}

    return {"total_papers": len(unique_papers), "papers": list(unique_papers.values())}


# Legacy search endpoint removed - use /search/on-demand instead


@app.post("/search")
async def search_papers(request: OnDemandSearchQuery):
    """
    Smart search endpoint:
    1. First search in main vector store (full papers) if available
    2. If not enough results, search abstracts in secondary DB
    3. Scrape full papers with images (if not already loaded)
    4. Generate answer with citations and images
    """
    global secondary_vector_store, vector_store, embeddings, db_manager

    all_relevant_docs = []
    papers_to_scrape = []
    loaded_papers = []
    image_data = []
    paper_images_map = {}

    # Step 1: Try to search in main vector store first (full papers)
    if vector_store:
        try:
            # Search full paper vector store
            main_retriever = vector_store.as_retriever(
                search_type="similarity", search_kwargs={"k": request.num_results}
            )
            main_docs = main_retriever.invoke(request.query)
            
            if len(main_docs) >= request.num_results:
                # We have enough results from full papers, no need to scrape
                all_relevant_docs = main_docs
                loaded_papers = [{"title": doc.metadata.get("title"), "pmcid": doc.metadata.get("pmcid")} 
                                for doc in main_docs]
                print(f"✅ Found {len(main_docs)} results in main vector store (full papers)")
            else:
                # Not enough results, will search abstracts below
                all_relevant_docs = main_docs
                print(f"⚠️ Only found {len(main_docs)} results in main store, searching abstracts...")
        except Exception as e:
            print(f"Error searching main vector store: {e}")

    # Step 2: If not enough results, search in abstract database
    if len(all_relevant_docs) < request.num_results and secondary_vector_store:
        retriever = secondary_vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": request.num_results}
        )
        abstract_docs = retriever.invoke(request.query)

        # Step 3: Extract paper links
        paper_links = []
        for doc in abstract_docs:
            link = doc.metadata.get("source")
            pmcid = doc.metadata.get("pmcid")
            title = doc.metadata.get("title")
            if link:
                paper_links.append({"link": link, "pmcid": pmcid, "title": title})

        # Step 4: Check which papers are already loaded
        for paper in paper_links:
            db_paper = db_manager.get_paper_by_link(paper["link"])
            if db_paper and db_paper["isLoaded"]:
                # Get chunks from already loaded paper
                results = vector_store.similarity_search(
                    paper["title"], k=5, filter={"pmcid": paper["pmcid"]}
                ) if vector_store else []
                all_relevant_docs.extend(results)
                loaded_papers.append(db_paper)
            else:
                papers_to_scrape.append(paper)

    elif not secondary_vector_store and len(all_relevant_docs) == 0:
        raise HTTPException(
            status_code=404,
            detail="No search databases available. Run abstract indexing first.",
        )

    # Step 5: Scrape full content + images for unloaded papers
    docs = []

    for paper in papers_to_scrape:
        print(f"📄 Scraping full paper: {paper['title'][:50]}...")
        result = scrape_article_text_with_images(paper["link"])

        if not result:
            continue

        text, image_urls = result

        # Store image URLs in separate map (will be preserved)
        paper_images_map[paper["title"]] = image_urls

        # Create document with image URLs as JSON string (ChromaDB compatible)
        doc = Document(
            page_content=text,
            metadata={
                "title": paper["title"],
                "source": paper["link"],
                "pmcid": paper["pmcid"] or "",
                "image_urls_json": json.dumps(image_urls) if image_urls else "",  # Store as JSON string
            },
        )
        docs.append(doc)

        if image_urls:
            image_data.append(
                {"pmcid": paper["pmcid"],
                    "title": paper["title"], "images": image_urls}
            )

        time.sleep(1)

    # Step 5: Create chunks and add to main vector store
    if docs:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=5000,
            chunk_overlap=500,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        chunks = splitter.split_documents(docs)
        
        # No need to filter metadata since we're using JSON strings for images

        if vector_store:
            vector_store.add_documents(chunks)
        else:
            vector_store = create_vectorstore(
                chunks, embeddings, PERSIST_DIRECTORY, COLLECTION_NAME
            )

        # Mark as loaded in database
        for i, paper in enumerate(papers_to_scrape):
            paper_chunks = [
                c for c in chunks if c.metadata.get("title") == paper["title"]
            ]
            db_manager.mark_as_loaded(
                paper["link"], chunks_created=len(paper_chunks))
            print(f"  ✅ Marked as loaded: {paper['title'][:50]}")

    # Step 6: Get all relevant chunks (newly loaded + already loaded)
    all_relevant_docs = []

    # Get chunks from newly scraped papers
    all_relevant_docs.extend(chunks if docs else [])

    # Get chunks from already loaded papers
    for loaded_paper in loaded_papers:
        # Query main vector store for this paper's chunks
        results = vector_store.similarity_search(
            loaded_paper["title"], k=5, filter={"pmcid": loaded_paper["pmcid"]}
        )
        all_relevant_docs.extend(results)

    # Step 7: Generate LLM answer with images
    answer = None
    if request.use_llm and request.google_api_key and all_relevant_docs:
        llm = ChatGoogleGenerativeAI(
            model=request.model_name,
            temperature=0,
            google_api_key=request.google_api_key,
        )

        # Format context with images
        context_parts = []
        for i, doc in enumerate(all_relevant_docs[:10], 1):
            title = doc.metadata.get("title", "Unknown")
            pmcid = doc.metadata.get("pmcid", "Unknown")
            source = doc.metadata.get("source", "Unknown")
            
            # Parse image URLs from JSON string in metadata
            image_urls_json = doc.metadata.get("image_urls_json", "")
            try:
                img_urls = json.loads(image_urls_json) if image_urls_json else []
            except:
                # Fallback to map if JSON parsing fails (for newly scraped papers)
                img_urls = paper_images_map.get(title, [])

            context = (
                f"[Document {i}]\nTitle: {title}\nPMCID: {
                    pmcid}\nSource: {source}\n"
            )
            if img_urls:
                # First 3 images
                context += f"Images: {', '.join(img_urls[:3])}\n"
            context += f"Content: {doc.page_content}\n"
            context_parts.append(context)

        formatted_context = "\n---\n".join(context_parts)

        prompt_template = PromptTemplate(
            template=(
                "You are an expert assistant analyzing NASA space biology research papers. "
                "Use the following papers to answer the question. "
                "ALWAYS cite paper Title and PMCID. If images are available, mention them.\n\n"
                "Available Papers:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer with citations, give response in markdown format and mention any relevant figures/images:"
            ),
            input_variables=["context", "question"],
        )

        prompt = prompt_template.format(
            context=formatted_context, question=request.query
        )
        response = llm.invoke(prompt)
        answer = response.content

    # Step 8: Format response with image URLs parsed from JSON
    source_docs = []
    for doc in all_relevant_docs[: request.num_results]:
        doc_title = doc.metadata.get("title", "Unknown")
        
        # Parse image URLs from JSON string in metadata
        image_urls_json = doc.metadata.get("image_urls_json", "")
        try:
            image_urls = json.loads(image_urls_json) if image_urls_json else []
        except:
            # Fallback to map if JSON parsing fails (for newly scraped papers)
            image_urls = paper_images_map.get(doc_title, [])
        
        source_docs.append(
            {
                "page_content": doc.page_content[:500] + "..."
                if len(doc.page_content) > 500
                else doc.page_content,
                "metadata": {
                    "title": doc_title,
                    "pmcid": doc.metadata.get("pmcid", "N/A"),
                    "source": doc.metadata.get("source", "Unknown"),
                    "image_urls": image_urls,
                },
            }
        )

    return {
        "answer": answer,
        "source_documents": source_docs,
        "images_found": image_data,
        "papers_newly_scraped": len(papers_to_scrape),
        "papers_already_loaded": len(loaded_papers),
        "query": request.query,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/database/load-csv")
async def load_csv_to_database():
    """Load CSV into SQLite database (without scraping)"""
    global db_manager

    if not db_manager:
        db_manager = init_database()

    try:
        stats = db_manager.load_csv(CSV_URL)
        return {
            "status": "success",
            "message": f"CSV loaded into database",
            "stats": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading CSV: {str(e)}")


@app.post("/load-papers", response_model=LoadPapersResponse)
async def load_papers(request: LoadPapersRequest, background_tasks: BackgroundTasks):
    """Scrape full papers and create embeddings (run after loading CSV and abstracts)"""
    global vector_store, embeddings, db_manager

    if not embeddings:
        embeddings = init_embeddings()

    if not db_manager:
        db_manager = init_database()

    try:
        # Get unloaded papers from database
        if request.num_papers > 0:
            papers_to_load = db_manager.get_unloaded_papers(
                limit=request.num_papers)
        else:
            papers_to_load = db_manager.get_unloaded_papers()

        if not papers_to_load:
            return LoadPapersResponse(
                status="success",
                papers_loaded=0,
                chunks_created=0,
                message="All papers already loaded or no papers available. Load CSV first using /database/load-csv",
            )

        docs = []
        papers_successfully_loaded = []

        for paper in papers_to_load:
            title = paper["title"]
            article_url = paper["link"]
            pmcid = paper["pmcid"]

            print(f"Scraping: {title[:60]}...")
            result = scrape_article_text_with_images(article_url)

            if not result:
                print(f"  ❌ Failed to scrape")
                continue

            text, image_urls = result

            # Create document with image URLs as JSON string
            doc = Document(
                page_content=text,
                metadata={
                    "title": title,
                    "source": article_url,
                    "pmcid": pmcid or "",
                    "image_urls_json": json.dumps(image_urls) if image_urls else "",  # Store as JSON string
                },
            )
            docs.append(doc)
            papers_successfully_loaded.append(paper)
            print(f"  ✅ Scraped successfully")
            time.sleep(1)  # polite delay

        if not docs:
            raise HTTPException(
                status_code=500, detail="Failed to scrape any papers. Please try again."
            )

        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=5000,
            chunk_overlap=500,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        chunks = splitter.split_documents(docs)
        
        # No need to filter metadata since we're using JSON strings for images

        # Create or update vector store
        if vector_store:
            vector_store.add_documents(chunks)
        else:
            vector_store = create_vectorstore(
                chunks, embeddings, PERSIST_DIRECTORY, COLLECTION_NAME
            )

        # Mark papers as loaded in database
        for i, paper in enumerate(papers_successfully_loaded):
            # Calculate chunks for this paper
            paper_chunks = [
                c for c in chunks if c.metadata.get("title") == paper["title"]
            ]
            chunks_count = len(paper_chunks)

            # Mark as loaded
            db_manager.mark_as_loaded(
                paper["link"], chunks_created=chunks_count)
            print(
                f"  📊 Marked as loaded: {
                    paper['title'][:50]}... ({chunks_count} chunks)"
            )

        return LoadPapersResponse(
            status="success",
            papers_loaded=len(docs),
            chunks_created=len(chunks),
            message=f"Successfully loaded {len(docs)} papers and created {
                len(chunks)} chunks",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading papers: {str(e)}")


@app.post("/reset-database")
async def reset_database():
    """Reset the vector database and SQLite tracking database"""
    global vector_store, db_manager

    vector_store = None

    if db_manager:
        db_manager.reset_database()

    return {
        "status": "success",
        "message": "Both databases reset successfully. Use /load-papers to create new databases.",
    }


@app.get("/database/stats")
async def get_database_stats():
    """Get SQLite database statistics"""
    if not db_manager:
        raise HTTPException(
            status_code=404, detail="Database manager not initialized")

    stats = db_manager.get_stats()
    return stats


@app.get("/database/papers/loaded")
async def get_loaded_papers_from_db(
    limit: int = Query(default=None, description="Limit number of results"),
):
    """Get papers that have been loaded"""
    if not db_manager:
        raise HTTPException(
            status_code=404, detail="Database manager not initialized")

    papers = db_manager.get_loaded_papers(limit=limit)
    return {"count": len(papers), "papers": papers}


@app.get("/database/papers/unloaded")
async def get_unloaded_papers_from_db(
    limit: int = Query(default=None, description="Limit number of results"),
):
    """Get papers that haven't been loaded yet"""
    if not db_manager:
        raise HTTPException(
            status_code=404, detail="Database manager not initialized")

    papers = db_manager.get_unloaded_papers(limit=limit)
    return {"count": len(papers), "papers": papers}


@app.get("/database/papers/all")
async def get_all_papers_from_db():
    """Get all papers with their status"""
    if not db_manager:
        raise HTTPException(
            status_code=404, detail="Database manager not initialized")

    papers = db_manager.get_all_papers()
    return {"count": len(papers), "papers": papers}


@app.get("/database/papers/search")
async def search_papers_in_db(
    query: str = Query(..., description="Search query"),
    loaded_only: bool = Query(
        default=False, description="Only return loaded papers"),
):
    """Search papers in database by title"""
    if not db_manager:
        raise HTTPException(
            status_code=404, detail="Database manager not initialized")

    papers = db_manager.search_papers(query, loaded_only=loaded_only)
    return {"query": query, "count": len(papers), "papers": papers}


class AppendCSVRequest(BaseModel):
    csv_url: str = Field(..., description="URL or path to CSV file to append")


@app.post("/database/append-csv")
async def append_csv_to_database(request: AppendCSVRequest):
    """Append papers from a new CSV file to the database"""
    if not db_manager:
        raise HTTPException(
            status_code=404, detail="Database manager not initialized")

    try:
        stats = db_manager.append_csv(request.csv_url)
        return {
            "status": "success",
            "message": f"CSV appended successfully",
            "stats": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error appending CSV: {str(e)}")


@app.get("/models")
async def list_available_models():
    """List available LLM models"""
    return {
        "models": [
            {
                "name": "gemini-2.5-flash",
                "description": "Latest Gemini 2.5 (Fast, Experimental)",
            },
            {"name": "gemini-2.5-pro",
                "description": "Gemini 2.5 Pro (Balanced)"},
            {"name": "gemini-1.5-pro",
                "description": "Gemini 1.5 Pro (Most Capable)"},
            {"name": "gemini-1.0-pro",
                "description": "Gemini 1.0 Pro (Legacy)"},
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

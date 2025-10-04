from main import scrape_article_abstract, init_embeddings, create_vectorstore, load_existing_vectorstore
from database_manager import  PaperDatabaseManager
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

db = PaperDatabaseManager()
embeddings = init_embeddings()
papers = db.get_nonAbstracted_papers()

PERSIST_DIRECTORY = "./small_persistent_db"
COLLECTION_NAME = "search_semantics"

print(f"📊 Found {len(papers)} papers without precessed abstraction")

if len(papers) == 0:
    print("✅ All papers already have abstracts extracted!")
    exit(0)

docs = []
abstracted_papers = []

for paper in papers :
    title = paper["title"]
    link = paper["link"]
    pmcid = paper["pmcid"]
    
    print(f"📄 Scraping abstract for: {title[:60]}...")
    text = scrape_article_abstract(link)
    
    if not text:
        print(f"⚠️  Failed to scrape abstract for: {title[:60]}")
        continue
    
    print(f"✅ Successfully scraped {len(text)} characters")
    
    doc = Document(
        page_content=text,
        metadata={
            "title":title,
            "source": link,
            "pmcid": pmcid or "",
        }
    )
    
    docs.append(doc)
    abstracted_papers.append(paper)
    
splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=500,
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""],
)

chunks = splitter.split_documents(docs)

print(f"\n📦 Created {len(chunks)} chunks from {len(docs)} documents")

# Check if we have any chunks before proceeding
if len(chunks) == 0:
    print("⚠️  No chunks created! All scraping attempts may have failed.")
    exit(1)

vector_store, count = load_existing_vectorstore(embeddings_func=embeddings, persist_dir=PERSIST_DIRECTORY,collection=COLLECTION_NAME)

if not vector_store:
    vector_store = create_vectorstore(
    chunks, embeddings, PERSIST_DIRECTORY, COLLECTION_NAME
)

vector_store.add_documents(chunks)


for i, paper in enumerate(abstracted_papers):
    # Calculate chunks for this paper
    paper_chunks = [c for c in chunks if c.metadata.get('title') == paper['title']]
    chunks_count = len(paper_chunks)
            
    # Mark as loaded
    db.mark_as_abstracted(paper['link'])
    print(f"  📊 Marked as abstracted: {paper['title'][:50]}... ({chunks_count} chunks)")
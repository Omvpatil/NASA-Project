"""
SQLite3 Database Manager for NASA Space Biology Papers
Tracks papers from CSV files and their loading status
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PaperDatabaseManager:
    """Manages SQLite database for tracking paper loading status"""
    
    def __init__(self, db_path: str = "./papers.db"):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._init_database()
    
    def _init_database(self):
        """Initialize database and create tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create papers table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT UNIQUE NOT NULL,
                pmcid TEXT,
                isLoaded BOOLEAN DEFAULT FALSE,
                isAbstracted BOOLEAN DEFAULT FALSE,
                loaded_at TIMESTAMP,
                chunks_created INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index on link for faster lookups
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_link ON papers(link)
        """)
        
        # Create index on isLoaded for filtering
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_isLoaded ON papers(isLoaded)
        """)
        
        self.conn.commit()
        logger.info(f"Database initialized at {self.db_path}")
    
    def load_csv(self, csv_url: str) -> Dict[str, int]:
        """
        Load papers from CSV file into database
        
        Args:
            csv_url: URL or path to CSV file
            
        Returns:
            Dictionary with stats (total, added, duplicates)
        """
        try:
            # Read CSV
            df = pd.read_csv(csv_url)
            
            # Ensure required columns exist
            if 'Title' not in df.columns or 'Link' not in df.columns:
                raise ValueError("CSV must contain 'Title' and 'Link' columns")
            
            stats = {
                'total': len(df),
                'added': 0,
                'duplicates': 0,
                'errors': 0
            }
            
            # Process each row
            for _, row in df.iterrows():
                title = row['Title'].strip() if pd.notna(row['Title']) else ''
                link = row['Link'].strip() if pd.notna(row['Link']) else ''
                
                if not title or not link:
                    stats['errors'] += 1
                    continue
                
                # Extract PMCID from link if available
                pmcid = self._extract_pmcid(link)
                
                try:
                    # Insert paper (ignore if duplicate link)
                    self.cursor.execute("""
                        INSERT OR IGNORE INTO papers (title, link, pmcid, isLoaded)
                        VALUES (?, ?, ?, FALSE)
                    """, (title, link, pmcid))
                    
                    if self.cursor.rowcount > 0:
                        stats['added'] += 1
                    else:
                        stats['duplicates'] += 1
                        
                except sqlite3.IntegrityError:
                    stats['duplicates'] += 1
            
            self.conn.commit()
            logger.info(f"CSV loaded: {stats['added']} added, {stats['duplicates']} duplicates, {stats['errors']} errors")
            return stats
            
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise
    
    def append_csv(self, csv_url: str) -> Dict[str, int]:
        """
        Append papers from CSV file to existing database
        Same as load_csv, but explicit name for clarity
        
        Args:
            csv_url: URL or path to CSV file
            
        Returns:
            Dictionary with stats (total, added, duplicates)
        """
        return self.load_csv(csv_url)
    
    def mark_as_loaded(self, link: str, chunks_created: int = 0) -> bool:
        """
        Mark a paper as loaded
        
        Args:
            link: Paper link/URL
            chunks_created: Number of chunks created from the paper
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            self.cursor.execute("""
                UPDATE papers
                SET isLoaded = TRUE,
                    loaded_at = ?,
                    chunks_created = ?,
                    updated_at = ?
                WHERE link = ?
            """, (datetime.now(), chunks_created, datetime.now(), link))
            
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                logger.info(f"Marked as loaded: {link}")
                return True
            else:
                logger.warning(f"Paper not found in database: {link}")
                return False
                
        except Exception as e:
            logger.error(f"Error marking paper as loaded: {e}")
            return False
        
    def mark_as_abstracted(self, link: str, chunks_created: int = 0) -> bool:
        """
        Mark a paper as loaded
        
        Args:
            link: Paper link/URL
            chunks_created: Number of chunks created from the paper
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            self.cursor.execute("""
                UPDATE papers
                SET isAbstracted = TRUE
                WHERE link = ?
            """, (link,))
            
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                logger.info(f"Marked as abstracted: {link}")
                return True
            else:
                logger.warning(f"Paper not found in database: {link}")
                return False
                
        except Exception as e:
            logger.error(f"Error marking paper as abstracted: {e}")
            return False
    
    def mark_as_loaded_by_pmcid(self, pmcid: str, chunks_created: int = 0) -> bool:
        """
        Mark a paper as loaded by PMCID
        
        Args:
            pmcid: PubMed Central ID (e.g., PMC8234567)
            chunks_created: Number of chunks created from the paper
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            self.cursor.execute("""
                UPDATE papers
                SET isLoaded = TRUE,
                    loaded_at = ?,
                    chunks_created = ?,
                    updated_at = ?
                WHERE pmcid = ?
            """, (datetime.now(), chunks_created, datetime.now(), pmcid))
            
            self.conn.commit()
            return self.cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error marking paper as loaded: {e}")
            return False
    
    def get_unloaded_papers(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get papers that haven't been loaded yet
        
        Args:
            limit: Maximum number of papers to return (None for all)
            
        Returns:
            List of paper dictionaries
        """
        query = """
            SELECT id, title, link, pmcid, created_at
            FROM papers
            WHERE isLoaded = FALSE
            ORDER BY created_at ASC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        self.cursor.execute(query)
        
        papers = []
        for row in self.cursor.fetchall():
            papers.append({
                'id': row[0],
                'title': row[1],
                'link': row[2],
                'pmcid': row[3],
                'created_at': row[4]
            })
        
        return papers

    def get_nonAbstracted_papers(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get papers that haven't been loaded yet
        
        Args:
            limit: Maximum number of papers to return (None for all)
            
        Returns:
            List of paper dictionaries
        """
        query = """
            SELECT id, title, link, pmcid, created_at
            FROM papers
            WHERE isAbstracted = FALSE
            ORDER BY created_at ASC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        self.cursor.execute(query)
        
        papers = []
        for row in self.cursor.fetchall():
            papers.append({
                'id': row[0],
                'title': row[1],
                'link': row[2],
                'pmcid': row[3],
                'created_at': row[4]
            })
        
        return papers

    def get_loaded_papers(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get papers that have been loaded
        
        Args:
            limit: Maximum number of papers to return (None for all)
            
        Returns:
            List of paper dictionaries
        """
        query = """
            SELECT id, title, link, pmcid, loaded_at, chunks_created
            FROM papers
            WHERE isLoaded = TRUE
            ORDER BY loaded_at DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        self.cursor.execute(query)
        
        papers = []
        for row in self.cursor.fetchall():
            papers.append({
                'id': row[0],
                'title': row[1],
                'link': row[2],
                'pmcid': row[3],
                'loaded_at': row[4],
                'chunks_created': row[5]
            })
        
        return papers
    
    def get_all_papers(self) -> List[Dict]:
        """
        Get all papers with their status
        
        Returns:
            List of all paper dictionaries
        """
        self.cursor.execute("""
            SELECT id, title, link, pmcid, isLoaded, loaded_at, chunks_created, created_at
            FROM papers
            ORDER BY created_at ASC
        """)
        
        papers = []
        for row in self.cursor.fetchall():
            papers.append({
                'id': row[0],
                'title': row[1],
                'link': row[2],
                'pmcid': row[3],
                'isLoaded': bool(row[4]),
                'loaded_at': row[5],
                'chunks_created': row[6],
                'created_at': row[7]
            })
        
        return papers
    
    def get_paper_by_link(self, link: str) -> Optional[Dict]:
        """
        Get a specific paper by its link
        
        Args:
            link: Paper link/URL
            
        Returns:
            Paper dictionary or None if not found
        """
        self.cursor.execute("""
            SELECT id, title, link, pmcid, isLoaded, loaded_at, chunks_created, created_at
            FROM papers
            WHERE link = ?
        """, (link,))
        
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'title': row[1],
                'link': row[2],
                'pmcid': row[3],
                'isLoaded': bool(row[4]),
                'loaded_at': row[5],
                'chunks_created': row[6],
                'created_at': row[7]
            }
        return None
    
    def get_stats(self) -> Dict:
        """
        Get database statistics
        
        Returns:
            Dictionary with various statistics
        """
        # Total papers
        self.cursor.execute("SELECT COUNT(*) FROM papers")
        total = self.cursor.fetchone()[0]
        
        # Loaded papers
        self.cursor.execute("SELECT COUNT(*) FROM papers WHERE isLoaded = TRUE")
        loaded = self.cursor.fetchone()[0]
        
        # Unloaded papers
        unloaded = total - loaded
        
        # Total chunks
        self.cursor.execute("SELECT SUM(chunks_created) FROM papers WHERE isLoaded = TRUE")
        total_chunks = self.cursor.fetchone()[0] or 0
        
        # Average chunks per paper
        avg_chunks = total_chunks / loaded if loaded > 0 else 0
        
        return {
            'total_papers': total,
            'loaded_papers': loaded,
            'unloaded_papers': unloaded,
            'total_chunks': total_chunks,
            'avg_chunks_per_paper': round(avg_chunks, 2),
            'loading_progress': round((loaded / total * 100), 2) if total > 0 else 0
        }
    
    def search_papers(self, query: str, loaded_only: bool = False) -> List[Dict]:
        """
        Search papers by title
        
        Args:
            query: Search query
            loaded_only: Only return loaded papers
            
        Returns:
            List of matching paper dictionaries
        """
        sql = """
            SELECT id, title, link, pmcid, isLoaded, loaded_at, chunks_created
            FROM papers
            WHERE title LIKE ?
        """
        
        if loaded_only:
            sql += " AND isLoaded = TRUE"
        
        sql += " ORDER BY created_at DESC"
        
        self.cursor.execute(sql, (f"%{query}%",))
        
        papers = []
        for row in self.cursor.fetchall():
            papers.append({
                'id': row[0],
                'title': row[1],
                'link': row[2],
                'pmcid': row[3],
                'isLoaded': bool(row[4]),
                'loaded_at': row[5],
                'chunks_created': row[6]
            })
        
        return papers
    
    def reset_database(self) -> bool:
        """
        Clear all papers from database
        
        Returns:
            True if successful
        """
        try:
            self.cursor.execute("DELETE FROM papers")
            self.conn.commit()
            logger.info("Database reset successfully")
            return True
        except Exception as e:
            logger.error(f"Error resetting database: {e}")
            return False
    
    def _extract_pmcid(self, link: str) -> Optional[str]:
        """
        Extract PMCID from link
        
        Args:
            link: Paper link/URL
            
        Returns:
            PMCID string or None
        """
        if 'PMC' in link:
            # Extract PMC ID from URL like https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/
            parts = link.split('PMC')
            if len(parts) > 1:
                pmcid = 'PMC' + parts[1].split('/')[0].strip()
                return pmcid
        return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Example usage and testing
if __name__ == "__main__":
    # Initialize database
    db = PaperDatabaseManager("./papers.db")
    
    # Load CSV
    csv_url = "https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publications.csv"
    
    print("Loading CSV into database...")
    stats = db.load_csv(csv_url)
    print(f"Stats: {stats}")
    
    # Get statistics
    print("\nDatabase Statistics:")
    db_stats = db.get_stats()
    for key, value in db_stats.items():
        print(f"  {key}: {value}")
    
    # Get unloaded papers
    print("\nUnloaded Papers (first 5):")
    unloaded = db.get_unloaded_papers(limit=5)
    for paper in unloaded:
        print(f"  - {paper['title'][:50]}... [{paper['pmcid']}]")
    
    # Simulate marking papers as loaded
    print("\nMarking first 3 papers as loaded...")
    for paper in unloaded[:3]:
        db.mark_as_loaded(paper['link'], chunks_created=5)
    
    # Get updated statistics
    print("\nUpdated Statistics:")
    db_stats = db.get_stats()
    for key, value in db_stats.items():
        print(f"  {key}: {value}")
    
    # Get loaded papers
    print("\nLoaded Papers:")
    loaded = db.get_loaded_papers()
    for paper in loaded:
        print(f"  - {paper['title'][:50]}... [{paper['chunks_created']} chunks]")
    
    # Search papers
    print("\nSearch for 'bone':")
    results = db.search_papers("bone")
    for paper in results[:3]:
        print(f"  - {paper['title'][:60]}...")
    
    # Close connection
    db.close()

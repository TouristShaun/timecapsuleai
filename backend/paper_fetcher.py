from arxiv_api import ArxivAPI
from DatabaseHandler import DatabaseHandler

class PaperFetcher:
    def __init__(self, arxiv_api=ArxivAPI(), db_config=None):
        self.arxiv_api = arxiv_api
        self.db = DatabaseHandler(db_config)
        
    def fetch_and_store_papers(self, search_query, start_index=0, max_results=10):
        papers = self.arxiv_api.search_papers(search_query, start_index, max_results)
        for paper in papers:
            self.store_paper_in_db(paper)

    def store_paper_in_db(self, paper):
        # Check if paper already exists
        query = "SELECT id FROM papers WHERE id = %s;"
        existing_paper = self.db.fetch_one(query, (paper['id'],))
        
        if existing_paper is None:
            query = """
            INSERT INTO papers (id, title, summary, authors, published_date, link)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            try:
                self.db.execute_query(query, (paper['id'], paper['title'], paper['summary'], paper['authors'], paper['published_date'], paper['link']))
            except Exception as e:
                # Handle database error
                print(f"Failed to insert paper: {e}")
        else:
            print(f"Paper with ID {paper['id']} already exists in the database.")


    def fetch_paper_by_id(self, paper_id):
        paper = self.arxiv_api.get_paper_by_id(paper_id)
        return paper

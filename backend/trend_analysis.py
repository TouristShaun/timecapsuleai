from gpt3_api import identify_trends
from paper_fetcher import PaperFetcher
from models import db, Trend  # Import the database session and Trend model

class TrendAnalysis:
    def __init__(self):
        """
        Initialize TrendAnalysis with a PaperFetcher instance.
        """
        self.paper_fetcher = PaperFetcher()

    def analyze_trends_in_paper(self, paper_id):
        """
        Analyze trends in a specific paper.
        
        Parameters:
            paper_id (str): The ID of the paper to analyze.
        
        Returns:
            str: Identified trends in the paper.
        """
        paper = self.paper_fetcher.fetch_paper_by_id(paper_id)
        trends = identify_trends(paper['summary'])
        
        # Store trends in the database
        for trend in trends:
            new_trend = Trend(
                paper_id=paper_id,
                trend=trend
            )
            db.session.add(new_trend)
        db.session.commit()

        return trends

    def analyze_trends_in_papers(self, search_query, start_index=0, max_results=10):
        """
        Analyze trends in a list of papers.
        
        Parameters:
            search_query (str): The search query for fetching papers.
            start_index (int): The start index for pagination.
            max_results (int): The maximum number of results to analyze.
        
        Returns:
            dict: A dictionary containing paper IDs and their respective trends.
        """
        self.paper_fetcher.fetch_and_store_papers(search_query, start_index, max_results)
        
        query = """
        SELECT id, summary FROM papers
        ORDER BY published_date DESC
        LIMIT %s
        """
        
        self.paper_fetcher.cursor.execute(query, (max_results,))
        papers = self.paper_fetcher.cursor.fetchall()
        
        trends = {}
        for paper_id, summary in papers:
            paper_trends = identify_trends(summary)
            trends[paper_id] = paper_trends
            
            # Store trends in the database
            for trend in paper_trends:
                new_trend = Trend(
                    paper_id=paper_id,
                    trend=trend
                )
                db.session.add(new_trend)
        db.session.commit()

        return trends

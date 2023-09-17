# Refactoring the BusinessInsights class to include database integration using SQLAlchemy.
from gpt3_api import generate_summary, identify_trends
from paper_fetcher import PaperFetcher
from models import BusinessInsight, db  # Assuming that BusinessInsight is a SQLAlchemy model in a file called models.py

class BusinessInsights:
    def __init__(self, paper_fetcher):
        """
        Initialize the BusinessInsights class with a PaperFetcher object.
        
        Parameters:
            paper_fetcher (object): Object for fetching papers.
        """
        self.paper_fetcher = paper_fetcher

    def generate_business_insights(self, paper_id, gpt3_api):
        """
        Generate business insights for a specific paper.
        
        Parameters:
            paper_id (str): The ID of the paper.
            gpt3_api (object): GPT-3.5 API interface.
            
        Returns:
            dict: Contains the summary, trends, and business insights of the paper.
        """
        paper = self.paper_fetcher.fetch_paper_by_id(paper_id)
        paper_text = paper['summary']

        summary = generate_summary(paper_text, gpt3_api)
        trends = identify_trends(paper_text, gpt3_api)
        business_insights = self.extract_business_insights(summary, trends, gpt3_api)

        # Storing the business insights in the database
        self.store_business_insights_in_db(paper_id, business_insights)

        return {
            'summary': summary,
            'trends': trends,
            'business_insights': business_insights
        }

    def extract_business_insights(self, summary, trends, gpt3_api):
        """
        Extract business insights from the summary and trends of a paper.
        
        Parameters:
            summary (str): The summary of the paper.
            trends (list): The trends identified in the paper.
            gpt3_api (object): GPT-3.5 API interface.
            
        Returns:
            list: A list of business insights.
        """
        business_insights = gpt3_api.extract_insights(summary, trends)
        return business_insights

    def store_business_insights_in_db(self, paper_id, business_insights):
        """
        Store the generated business insights in the database.
        
        Parameters:
            paper_id (str): The ID of the paper.
            business_insights (list): List of business insights generated.
        """
        for insight in business_insights:
            new_insight = BusinessInsight(paper_id=paper_id, insight=insight)
            db.session.add(new_insight)
        db.session.commit()

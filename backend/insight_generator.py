from gpt3_api import generate_summary, identify_trends
from paper_fetcher import PaperFetcher
from models import db, Insight, Trend  # Import the models and the database session

class InsightGenerator:
    def __init__(self):
        self.paper_fetcher = PaperFetcher()

    def generate_insights(self, paper_id):
        """
        Generate insights for a specific paper.
        :param paper_id: The ID of the paper.
        :return: A dictionary containing the summary and trends of the paper.
        """
        paper = self.paper_fetcher.fetch_paper_by_id(paper_id)
        paper_text = paper['summary']

        summary = generate_summary(paper_text)
        trends = identify_trends(paper_text)

        # Create an Insight object and add it to the database
        new_insight = Insight(
            paper_id=paper_id,
            summary=summary
        )
        db.session.add(new_insight)
        db.session.commit()

        # Create a Trend object and add it to the database
        for trend in trends:
            new_trend = Trend(
                paper_id=paper_id,
                trend=trend
            )
            db.session.add(new_trend)
        db.session.commit()

        return {
            'summary': summary,
            'trends': trends
        }

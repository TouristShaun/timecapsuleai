from paper_fetcher import PaperFetcher
from insight_generator import InsightGenerator
from models import CuratedList, CuratedListPaper, db  # Assuming models are defined in a file named models.py
from flask import current_app as app  # If using Flask's application context

class CuratedLists:
    def __init__(self, paper_fetcher=None, insight_generator=None):
        self.paper_fetcher = paper_fetcher or PaperFetcher()
        self.insight_generator = insight_generator or InsightGenerator()

    def create_curated_list(self, list_name, paper_ids):
        try:
            new_list = CuratedList(name=list_name)
            db.session.add(new_list)
            db.session.flush()  # To get the id of new_list

            for paper_id in paper_ids:
                new_list_paper = CuratedListPaper(list_id=new_list.id, paper_id=paper_id)
                db.session.add(new_list_paper)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def fetch_curated_list(self, list_id):
        try:
            curated_list = CuratedList.query.get(list_id)
            paper_ids = [paper.paper_id for paper in curated_list.papers]

            papers = []
            for paper_id in paper_ids:
                paper = self.paper_fetcher.fetch_paper_by_id(paper_id)
                insights = self.insight_generator.generate_insights(paper_id)
                papers.append({
                    'paper': paper,
                    'insights': insights
                })

            return {
                'name': curated_list.name,
                'papers': papers
            }
        except Exception as e:
            raise e

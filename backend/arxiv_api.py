import requests

class ArxivAPI:
    def __init__(self):
        """
        Initialize the ArxivAPI class.
        """
        self.base_url = "http://export.arxiv.org/api/query?"
        self.headers = {
            "User-Agent": "TimeCapsuleAI"
        }

    def search_papers(self, search_query, start_index=0, max_results=10):
        """
        Search for papers on arXiv based on the search query.
        
        Parameters:
            search_query (str): The search query.
            start_index (int): The start index for pagination (default 0).
            max_results (int): The maximum number of results to return (default 10).
            
        Returns:
            str: The search results in XML format.
        """
        query_url = f"{self.base_url}search_query={search_query}&start={start_index}&max_results={max_results}"
        response = requests.get(query_url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def get_paper_by_id(self, paper_id):
        """
        Get a specific paper by its ID.
        
        Parameters:
            paper_id (str): The ID of the paper.
            
        Returns:
            str: The paper in XML format.
        """
        query_url = f"{self.base_url}id_list={paper_id}"
        response = requests.get(query_url, headers=self.headers)
        response.raise_for_status()
        return response.text

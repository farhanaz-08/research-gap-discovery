from config.retrieval import (
    MIN_LOCAL_PAPERS,
    MIN_AVERAGE_SCORE,
    TOP_K_LOCAL_SEARCH
)

from app.database.postgres_manager import PostgreSQLManager


# from app.database.postgres_manager import PostgreSQLManager


class KnowledgeChecker:

    def __init__(self):

        self.db = PostgreSQLManager()

    def check_local_knowledge(
    self,
    keywords
    ):

        ranked_papers = self.db.search_and_rank_papers(
           keyword_list=keywords,
            limit=TOP_K_LOCAL_SEARCH
        )
        
        paper_count = len(ranked_papers)
        
        if paper_count == 0:
             average_score = 0
            
        else:
            
            total_score = sum(
                paper["score"]
                for paper in ranked_papers
            )
            
            average_score = total_score / paper_count
            
        sufficient = (
            paper_count >= MIN_LOCAL_PAPERS
            
            and 
            
            average_score >= MIN_AVERAGE_SCORE 
        )

        return {
             "sufficient": sufficient,

            "paper_count": paper_count,

            "average_score": average_score,

            "papers": ranked_papers
        }
from typing import List

import re


class QueryProcessor:

    def __init__(self):

        pass

    def process_query(
        self,
        query: str
    ):

        keywords = self.extract_keywords(query)

        return {

            "original_query": query,

            "keywords": keywords

        }

    def extract_keywords(
        self,
        query: str
    ) -> List[str]:

        query = query.lower()

        query = re.sub(
            r"[^a-zA-Z0-9\s]",
            "",
            query
        )

        words = query.split()

        return words
try:
    from ddgs import DDGS
except ImportError:
    DDGS = None

class ResearchService:
    def search(self, query: str):
        if DDGS is None:
            return []
        try:
            with DDGS() as client:
                results = client.text(query, max_results=8)
                return [{"title":r.get("title",""),"url":r.get("href",""),"snippet":r.get("body","")} for r in results]
        except Exception:
            return []

research = ResearchService()

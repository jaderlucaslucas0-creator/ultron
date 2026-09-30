try:
    from ddgs import DDGS
except ImportError:
    DDGS = None

class ResearchService:
    def search(self, query, max_results=8):
        if not query.strip() or DDGS is None: return []
        try:
            with DDGS() as client:
                results=client.text(query.strip(), max_results=max_results)
                return [{"title":x.get("title",""),"url":x.get("href",""),"snippet":x.get("body","")} for x in results]
        except Exception:
            return []
research=ResearchService()

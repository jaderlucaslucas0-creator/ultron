from html.parser import HTMLParser
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

class SearchParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self._link = None
        self._capture = False
        self._text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "result__a" in attrs.get("class", ""):
            self._link = attrs.get("href")
            self._capture = True
            self._text = []

    def handle_data(self, data):
        if self._capture:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._capture:
            title = " ".join("".join(self._text).split())
            if title and self._link:
                self.results.append((title, self._link))
            self._capture = False
            self._link = None

def research_web(query: str) -> str:
    url = "https://html.duckduckgo.com/html/?q=" + quote(query)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 Hermes/1.0"})
    try:
        with urlopen(req, timeout=12) as response:
            html = response.read().decode("utf-8", errors="ignore")
    except (URLError, HTTPError, OSError, TimeoutError) as exc:
        raise RuntimeError("A pesquisa web não pôde ser acessada agora.") from exc

    parser = SearchParser()
    parser.feed(html)
    if not parser.results:
        return "Nenhum resultado foi encontrado."

    lines = ["Resultados encontrados para: " + query, ""]
    for i, (title, link) in enumerate(parser.results[:8], 1):
        lines.append(f"{i}. {title}")
        lines.append(f"   {link}")
    return "\n".join(lines)

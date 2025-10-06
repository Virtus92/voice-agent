"""
LangChain Tools for Voice Agent
Implements: web search, wikipedia, website fetching, calculator, and time
"""

import requests
from typing import Optional
from datetime import datetime
import wikipedia
from bs4 import BeautifulSoup
from ddgs import DDGS
from langchain_core.tools import tool


@tool
def web_search(query: str, max_results: int = 10) -> str:
    """
    Search the web using DuckDuckGo. Use this when you need current information or need to search the internet.
    For local searches (restaurants, shops, etc.), always search with location-specific terms.

    Args:
        query: The search query
        max_results: Maximum number of results (default: 10)

    Returns:
        Formatted search results with title, description, and URL
    """
    try:
        print(f"🔍 Searching web: {query}")

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return "Keine Suchergebnisse gefunden. Versuche eine andere Formulierung oder spezifischere Suchbegriffe."

        formatted = f"Ich habe {len(results)} Ergebnisse für '{query}' gefunden:\n\n"

        for i, result in enumerate(results, 1):
            title = result.get('title', 'Kein Titel')
            body = result.get('body', result.get('description', 'Keine Beschreibung'))
            url = result.get('link', result.get('url', result.get('href', 'Keine URL')))

            formatted += f"{i}. {title}\n"
            if body and body != 'Keine Beschreibung':
                formatted += f"   → {body}\n"
            formatted += f"   🔗 {url}\n\n"

        return formatted

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Web search error: {error_msg}")
        return f"Die Websuche hatte ein Problem ({error_msg}). Ich kann trotzdem versuchen, mit anderen Informationsquellen weiterzuhelfen."


@tool
def wikipedia_search(query: str, sentences: int = 3) -> str:
    """
    Search Wikipedia for information. Use this for factual, encyclopedic information.

    Args:
        query: The topic to search on Wikipedia
        sentences: Number of sentences to return (default: 3)

    Returns:
        Wikipedia summary
    """
    try:
        print(f"📚 Searching Wikipedia: {query}")

        wikipedia.set_lang("de")

        summary = wikipedia.summary(query, sentences=sentences)

        return f"Wikipedia-Information zu '{query}':\n\n{summary}"

    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options[:5])
        return f"Mehrere Artikel gefunden. Bitte präzisiere: {options}"

    except wikipedia.exceptions.PageError:
        return f"Kein Wikipedia-Artikel zu '{query}' gefunden."

    except Exception as e:
        return f"Fehler bei Wikipedia-Suche: {str(e)}"


@tool
def fetch_website(url: str) -> str:
    """
    Fetch and extract text content from a website URL.

    Args:
        url: The URL to fetch

    Returns:
        Extracted text content
    """
    try:
        print(f"🌐 Fetching website: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text()

        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        max_length = 2000
        if len(text) > max_length:
            text = text[:max_length] + "..."

        return f"Inhalt von {url}:\n\n{text}"

    except requests.exceptions.RequestException as e:
        return f"Fehler beim Abrufen der Website: {str(e)}"

    except Exception as e:
        return f"Fehler beim Verarbeiten der Website: {str(e)}"


@tool
def get_current_time(timezone: str = "Europe/Berlin") -> str:
    """
    Get the current date and time.

    Args:
        timezone: Timezone string (e.g., 'Europe/Berlin')

    Returns:
        Current date and time
    """
    try:
        from zoneinfo import ZoneInfo
        now = datetime.now(ZoneInfo(timezone))

        weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        months = ["", "Januar", "Februar", "März", "April", "Mai", "Juni",
                 "Juli", "August", "September", "Oktober", "November", "Dezember"]

        weekday = weekdays[now.weekday()]
        month = months[now.month]

        formatted = f"{weekday}, {now.day}. {month} {now.year}, {now.strftime('%H:%M:%S')} Uhr"

        return f"Aktuelle Zeit ({timezone}): {formatted}"

    except Exception as e:
        now = datetime.now()
        return f"Aktuelle Zeit: {now.strftime('%d.%m.%Y %H:%M:%S')} Uhr"


@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations. Supports basic arithmetic and Python math expressions.

    Args:
        expression: Mathematical expression to evaluate (e.g., '2 + 2', 'sqrt(16)', 'sin(45)')

    Returns:
        Calculation result
    """
    try:
        import math
        import re

        if not re.match(r'^[0-9+\-*/()., sqrt|sin|cos|tan|log|exp|pow]+$', expression.replace(' ', '')):
            return "Ungültiger mathematischer Ausdruck."

        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('log', 'math.log')
        expression = expression.replace('exp', 'math.exp')
        expression = expression.replace('pow', 'math.pow')

        result = eval(expression)

        return f"Berechnung: {expression} = {result}"

    except Exception as e:
        return f"Fehler bei der Berechnung: {str(e)}"


TOOLS = [
    web_search,
    wikipedia_search,
    fetch_website,
    calculator,
    get_current_time
]

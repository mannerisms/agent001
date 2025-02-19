import requests
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re
from typing import Optional, Dict


class WebContentParser:
    def __init__(self):
        self.default_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

    def get_webpage_content(self, url: str) -> Optional[str]:
        """
        Fetch webpage content with error handling
        """
        try:
            response = requests.get(
                url, headers=self.default_headers, allow_redirects=True
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching webpage: {e}")
            return None

    def extract_content_readability(self, html: str) -> Dict[str, str]:
        """
        Extract content using readability-lxml
        """
        doc = Document(html)
        return {"title": doc.title(), "content": doc.summary()}

    def extract_content_trafilatura(self, html: str) -> Dict[str, str]:
        """
        Extract content using trafilatura
        """
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            include_links=True,
            include_images=False,
        )

        # Get the title separately using BeautifulSoup as trafilatura might miss it
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string if soup.title else ""

        return {"title": title, "content": extracted if extracted else ""}

    def extract_content_beautifulsoup(self, html: str) -> Dict[str, str]:
        """
        Extract content using BeautifulSoup with custom cleaning
        """
        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted elements
        for element in soup.find_all(
            ["script", "style", "iframe", "nav", "footer", "header"]
        ):
            element.decompose()

        # Extract title
        title = soup.title.string if soup.title else ""

        # Extract main content (customize selectors based on website structure)
        main_content = ""
        content_selectors = [
            "article",
            "main",
            ".content",
            "#content",
            ".post",
            ".job-description",
            ".vacancy-description",
        ]

        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                main_content = content.get_text(separator="\n", strip=True)
                break

        # If no main content found, try getting body content
        if not main_content:
            body = soup.find("body")
            if body:
                main_content = body.get_text(separator="\n", strip=True)

        return {"title": title, "content": main_content}

    def clean_text(self, text: str) -> str:
        """
        Clean extracted text
        """
        if not text:
            return ""

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove empty lines
        text = "\n".join(line.strip() for line in text.split("\n") if line.strip())

        # Remove common noise patterns (customize based on needs)
        noise_patterns = [
            r"Cookie Policy",
            r"Privacy Policy",
            r"Terms of Service",
            r"Accept all cookies",
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Remove emails
            r"Copyright © \d{4}",
            r"All rights reserved",
        ]

        for pattern in noise_patterns:
            text = re.sub(pattern, "", text)

        return text.strip()

    def parse_webpage(self, url: str, method: str = "trafilatura") -> Dict[str, str]:
        """
        Main method to parse webpage content using specified method
        """
        html = self.get_webpage_content(url)
        if not html:
            return {"error": "Failed to fetch webpage"}

        extractors = {
            "readability": self.extract_content_readability,
            "trafilatura": self.extract_content_trafilatura,
            "beautifulsoup": self.extract_content_beautifulsoup,
        }

        extractor = extractors.get(method.lower())
        if not extractor:
            return {"error": "Invalid extraction method"}

        try:
            content = extractor(html)

            # Clean the extracted content
            if "content" in content:
                content["content"] = self.clean_text(content["content"])

            return content
        except Exception as e:
            return {"error": f"Extraction failed: {str(e)}"}

    def get_vacancy_announcement(self, url: str) -> str:
        """
        Get vacancy announcement from a URL using the best available method
        """
        # Try methods in order of preference
        methods = ["trafilatura", "readability", "beautifulsoup"]

        for method in methods:
            result = self.parse_webpage(url, method=method)

            if "error" not in result and result.get("content"):
                return result["content"]

        return "Failed to extract content from the webpage"

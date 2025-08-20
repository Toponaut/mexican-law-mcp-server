"""
DOF (Diario Oficial de la Federación) search functionality for Mexican legislation.
"""

import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from urllib.parse import urljoin, quote
import urllib3

# Disable SSL warnings for DOF website
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class DOFSearchResult:
    title: str
    date: str
    url: str
    summary: str
    type: str
    content: Optional[str] = None


class DOFSearcher:
    """Search and retrieve documents from the Diario Oficial de la Federación."""
    
    def __init__(self):
        self.base_url = "https://www.dof.gob.mx"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Mexican Legal MCP/1.0)'
        })

    def search_legislation(
        self, 
        query: str, 
        date_from: Optional[date] = None, 
        date_to: Optional[date] = None,
        limit: int = 20
    ) -> List[DOFSearchResult]:
        """
        Search for legislation in the DOF.
        
        Args:
            query: Search terms
            date_from: Start date for search
            date_to: End date for search
            limit: Maximum number of results
        
        Returns:
            List of search results
        """
        try:
            # Use the correct search form found on the website
            search_data = {
                'textobusqueda': query,
                'vienede': 'header',
                's': 's'
            }
            
            response = self.session.post(
                f"{self.base_url}/busqueda_detalle.php",
                data=search_data,
                timeout=30,
                verify=False
            )
            response.raise_for_status()
            
            return self._parse_search_results(response.text, limit)
            
        except Exception as e:
            raise Exception(f"Error searching DOF: {str(e)}")

    def get_document_content(self, url: str) -> str:
        """
        Retrieve full content of a DOF document.
        
        Args:
            url: Document URL
            
        Returns:
            Document text content
        """
        try:
            response = self.session.get(url, timeout=30, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try different selectors for document content
            content_selectors = [
                '.documento-contenido',
                '.contenido-documento', 
                '.texto-documento',
                '.articulo-texto',
                '.document-body',
                'main',
                '.content',
                '#content'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = ' '.join(el.get_text(strip=True) for el in elements)
                    break
            
            # Fallback to body text
            if not content:
                content = soup.get_text(strip=True)
            
            return self._clean_text(content)
            
        except Exception as e:
            raise Exception(f"Error fetching document content: {str(e)}")

    def search_by_type(
        self, 
        doc_type: str, 
        query: Optional[str] = None,
        limit: int = 20
    ) -> List[DOFSearchResult]:
        """
        Search documents by type (decreto, ley, reglamento, etc.).
        
        Args:
            doc_type: Type of document (decreto, ley, reglamento, acuerdo, norma)
            query: Additional search terms
            limit: Maximum number of results
            
        Returns:
            List of search results
        """
        search_query = f"{doc_type} {query}" if query else doc_type
        return self.search_legislation(search_query, limit=limit)

    def get_latest_publications(self, limit: int = 10) -> List[DOFSearchResult]:
        """
        Get latest DOF publications.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of latest publications
        """
        try:
            response = self.session.get(f"{self.base_url}/index.php", timeout=30, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Look for recent publications - try various selectors
            publication_selectors = [
                '.publicacion-reciente',
                '.ultima-publicacion',
                '.item-publicacion',
                'a[href*="nota_detalle"]',  # DOF specific link pattern
                'a[href*=".php"]',
                'table tr',
                'div[class*="nota"]',
                'div[class*="publicacion"]'
            ]
            
            for selector in publication_selectors:
                elements = soup.select(selector)
                if elements:
                    count = 0
                    for element in elements:
                        result = self._extract_publication_info(element)
                        if result:
                            results.append(result)
                            count += 1
                            if count >= limit:
                                break
                    if results:  # If we found results, stop trying other selectors
                        break
            
            return results[:limit]
            
        except Exception as e:
            raise Exception(f"Error fetching latest publications: {str(e)}")

    def search_constitution(self, article: Optional[str] = None) -> List[DOFSearchResult]:
        """Search Mexican Constitution articles."""
        query = f"constitución política artículo {article}" if article else "constitución política"
        return self.search_legislation(query)

    def search_codigo(self, codigo_type: str, article: Optional[str] = None) -> List[DOFSearchResult]:
        """
        Search legal codes (civil, penal, comercio, etc.).
        
        Args:
            codigo_type: Type of code (civil, penal, comercio, trabajo)
            article: Specific article number
        """
        query = f"código {codigo_type}"
        if article:
            query += f" artículo {article}"
        return self.search_legislation(query)

    def _parse_search_results(self, html: str, limit: int = 20) -> List[DOFSearchResult]:
        """Parse HTML search results."""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # Try different selectors for search results based on actual DOF structure
        result_selectors = [
            'tr',  # Table rows are commonly used in DOF results
            '.resultado-busqueda',
            '.item-resultado', 
            '.search-result',
            '.documento-item',
            'div[class*="result"]',
            'div[class*="documento"]'
        ]
        
        for selector in result_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    result = self._extract_result_info(element)
                    if result:
                        results.append(result)
                        if len(results) >= limit:
                            break
                if results:  # If we found results with this selector, stop trying others
                    break
        
        return results[:limit]

    def _extract_result_info(self, element) -> Optional[DOFSearchResult]:
        """Extract information from a search result element."""
        try:
            # Look for title in various possible locations
            title_el = element.select_one('.titulo, h3, .nombre-documento, a, td a, strong')
            if not title_el:
                # Try to get any text content that looks like a title
                text_content = element.get_text(strip=True)
                if len(text_content) > 10 and len(text_content) < 200:
                    title = text_content
                else:
                    return None
            else:
                title = title_el.get_text(strip=True)
            
            # Skip if title is too short or contains unwanted content
            if len(title) < 5 or any(skip in title.lower() for skip in ['login', 'usuario', 'clave', 'votar']):
                return None
                
            # Get URL
            url = ""
            link_el = element.select_one('a')
            if link_el and link_el.get('href'):
                href = link_el['href']
                if href.startswith('http'):
                    url = href
                elif href.startswith('/'):
                    url = self.base_url + href
                else:
                    url = f"{self.base_url}/{href}"
            
            # Get date - look in table cells or date elements
            date = ""
            date_el = element.select_one('.fecha, .date, td:nth-child(2), td:nth-child(3)')
            if date_el:
                date_text = date_el.get_text(strip=True)
                # Check if it looks like a date
                if any(char.isdigit() for char in date_text) and len(date_text) > 4:
                    date = date_text
            
            # Get summary - try to find descriptive text
            summary = ""
            summary_el = element.select_one('.resumen, .descripcion, .summary, td:nth-child(4), td:last-child')
            if summary_el:
                summary_text = summary_el.get_text(strip=True)
                if len(summary_text) > 10:
                    summary = summary_text[:200]  # Limit summary length
            
            # Get type
            doc_type = "Documento"
            type_el = element.select_one('.tipo, .type, td:first-child')
            if type_el:
                type_text = type_el.get_text(strip=True)
                if len(type_text) < 50:  # Reasonable type length
                    doc_type = type_text
            
            # Only return if we have at least a title
            if title:
                return DOFSearchResult(
                    title=title,
                    date=date,
                    url=url or f"{self.base_url}/busqueda_detalle.php",
                    summary=summary,
                    type=doc_type
                )
                
        except Exception:
            pass
        
        return None

    def _extract_publication_info(self, element) -> Optional[DOFSearchResult]:
        """Extract information from a publication element."""
        return self._extract_result_info(element)

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        import re
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\"\'\n]', ' ', text)
        
        return text.strip()
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import re
from config import *
from utils import clean_text, save_json

class DocumentProcessor:    
    def __init__(self):
        self.namespaces = {
            'oai': 'http://www.openarchives.org/OAI/2.0/',
            'dim': 'http://www.dspace.org/xmlns/dspace/dim'
        }
    
    def xml_to_json(self, xml_filepath: str = XML_FILE) -> List[Dict[str, Any]]:
        print("A iniciar conversão XML→JSON...")
        
        try:
            tree = ET.parse(xml_filepath)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Erro ao processar XML: {e}")
            return []
        
        documents = []
        records = root.findall('.//oai:record', self.namespaces)
        
        print(f"A processar {len(records)} registos...")
        
        for i, record in enumerate(records):
            doc = self._process_record(record)
            if doc and self._is_valid_document(doc):
                documents.append(doc)
            
            if (i + 1) % 50 == 0:
                print(f"Processados {i + 1} registos...")
        
        print(f"Conversão concluída: {len(documents)} documentos válidos")
        return documents
    
    def _process_record(self, record: ET.Element) -> Optional[Dict[str, Any]]:
        try:
            metadata = record.find('.//dim:dim', self.namespaces)
            if metadata is None:
                return None
            
            doc = {
                'id': self._extract_identifier(record),
                'title': self._extract_field(metadata, 'title'),
                'abstract': self._extract_field(metadata, 'description', 'abstract'),
                'authors': self._extract_multiple_fields(metadata, 'contributor', 'author'),
                'keywords': self._extract_multiple_fields(metadata, 'subject'),
                'date': self._extract_field(metadata, 'date', 'issued'),
                'type': self._extract_field(metadata, 'type'),
                'language': self._extract_field(metadata, 'language', 'iso'),
                'subjects_udc': self._extract_multiple_fields(metadata, 'subject', 'udc'),
                'subjects_fos': self._extract_multiple_fields(metadata, 'subject', 'fos'),
                'collections': self._extract_multiple_fields(metadata, 'relation', 'ispartof')
            }
            
            doc = self._clean_document(doc)
            
            return doc
            
        except Exception as e:
            print(f"Erro ao processar registo: {e}")
            return None
    
    def _extract_identifier(self, record: ET.Element) -> str:
        header = record.find('.//oai:header', self.namespaces)
        if header is not None:
            identifier = header.find('oai:identifier', self.namespaces)
            if identifier is not None:
                return identifier.text or ""
        return ""
    
    def _extract_field(self, metadata: ET.Element, element: str, qualifier: str = None) -> str:
        xpath = f".//dim:field[@element='{element}']"
        if qualifier:
            xpath += f"[@qualifier='{qualifier}']"
        
        field = metadata.find(xpath, self.namespaces)
        return field.text if field is not None and field.text else ""
    
    def _extract_multiple_fields(self, metadata: ET.Element, element: str, qualifier: str = None) -> List[str]:
        xpath = f".//dim:field[@element='{element}']"
        if qualifier:
            xpath += f"[@qualifier='{qualifier}']"
        
        fields = metadata.findall(xpath, self.namespaces)
        return [field.text for field in fields if field.text]
    
    def _clean_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        text_fields = ['title', 'abstract']
        for field in text_fields:
            if doc.get(field):
                doc[field] = clean_text(doc[field])
        
        list_fields = ['authors', 'keywords', 'subjects_udc', 'subjects_fos', 'collections']
        for field in list_fields:
            if doc.get(field):
                doc[field] = [clean_text(item) for item in doc[field] if item]
        
        if doc.get('date'):
            doc['date'] = self._normalize_date(doc['date'])
        
        return doc
    
    def _normalize_date(self, date_str: str) -> str:
        year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
        return year_match.group() if year_match else date_str
    
    def _is_valid_document(self, doc: Dict[str, Any]) -> bool:
        if not doc.get('title') or not doc.get('abstract'):
            return False
        
        if len(doc['abstract']) < MIN_ABSTRACT_LENGTH:
            return False
        
        if len(doc['abstract']) > MAX_ABSTRACT_LENGTH:
            return False
        
        return True
    
    def save_collection(self, documents: List[Dict[str, Any]], filepath: str = JSON_FILE) -> None:
        save_json(documents, filepath)
        print(f"Coleção guardada em: {filepath}")

def main():
    processor = DocumentProcessor()
    
    documents = processor.xml_to_json()
    
    processor.save_collection(documents)
    
    print(f"\nEstatísticas da coleção:")
    print(f"Total de documentos: {len(documents)}")
    
    if documents:
        avg_abstract_len = sum(len(doc['abstract']) for doc in documents) / len(documents)
        print(f"Tamanho médio do abstract: {avg_abstract_len:.1f} caracteres")
        
        languages = [doc['language'] for doc in documents if doc['language']]
        print(f"Idiomas encontrados: {set(languages)}")

if __name__ == "__main__":
    main()

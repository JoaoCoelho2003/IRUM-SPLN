import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import re
from config import *
from utils import clean_text, save_json
from colorama import Fore, Style, init

init(autoreset=True)


class DocumentProcessor:
    def __init__(self):
        self.namespaces = {
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dim": "http://www.dspace.org/xmlns/dspace/dim",
        }

    def xml_to_json(self, xml_filepath: str = XML_FILE) -> List[Dict[str, Any]]:
        print(f"{Fore.CYAN}Starting XML→JSON conversion...{Style.RESET_ALL}")

        try:
            tree = ET.parse(xml_filepath)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"{Fore.RED}Error processing XML: {e}{Style.RESET_ALL}")
            return []

        documents = []
        records = root.findall(".//oai:record", self.namespaces)

        print(f"{Fore.YELLOW}Processing {len(records)} records...{Style.RESET_ALL}")

        for i, record in enumerate(records):
            doc = self._process_record(record)
            if doc and self._is_valid_document(doc):
                documents.append(doc)

            if (i + 1) % 50 == 0:
                print(f"{Fore.BLUE}Processed {i + 1} records...{Style.RESET_ALL}")

        print(
            f"{Fore.GREEN}Conversion completed: {len(documents)} valid documents{Style.RESET_ALL}"
        )
        return documents

    def _process_record(self, record: ET.Element) -> Optional[Dict[str, Any]]:
        try:
            metadata = record.find(".//dim:dim", self.namespaces)
            if metadata is None:
                return None

            collection_values = []
            relation_fields = metadata.findall(
                ".//dim:field[@element='relation']", self.namespaces
            )
            for field in relation_fields:
                if field.text and field.text.strip():
                    collection_values.append(field.text.strip())

            doc = {
                "id": self._extract_identifier(record),
                "title": self._extract_field(metadata, "title"),
                "abstract": self._extract_field(metadata, "description", "abstract"),
                "authors": self._extract_multiple_fields(
                    metadata, "contributor", "author"
                ),
                "keywords": self._extract_multiple_fields(metadata, "subject"),
                "date": self._extract_field(metadata, "date", "issued"),
                "type": self._extract_field(metadata, "type"),
                "language": self._extract_field(metadata, "language", "iso"),
                "subjects_udc": self._extract_multiple_fields(
                    metadata, "subject", "udc"
                ),
                "subjects_fos": self._extract_multiple_fields(
                    metadata, "subject", "fos"
                ),
                "collections": collection_values,
            }

            doc = self._clean_document(doc)

            return doc

        except Exception as e:
            print(f"{Fore.RED}Error processing record: {e}{Style.RESET_ALL}")
            return None

    def _extract_identifier(self, record: ET.Element) -> str:
        header = record.find(".//oai:header", self.namespaces)
        if header is not None:
            identifier = header.find("oai:identifier", self.namespaces)
            if identifier is not None:
                return identifier.text or ""
        return ""

    def _extract_field(
        self, metadata: ET.Element, element: str, qualifier: str = None
    ) -> str:
        xpath = f".//dim:field[@element='{element}']"
        if qualifier:
            xpath += f"[@qualifier='{qualifier}']"

        field = metadata.find(xpath, self.namespaces)
        return field.text if field is not None and field.text else ""

    def _extract_multiple_fields(
        self, metadata: ET.Element, element: str, qualifier: str = None
    ) -> List[str]:
        xpath = f".//dim:field[@element='{element}']"
        if qualifier:
            xpath += f"[@qualifier='{qualifier}']"

        fields = metadata.findall(xpath, self.namespaces)
        return [field.text for field in fields if field.text]

    def _clean_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        text_fields = ["title", "abstract"]
        for field in text_fields:
            if doc.get(field):
                doc[field] = clean_text(doc[field])

        list_fields = [
            "authors",
            "keywords",
            "subjects_udc",
            "subjects_fos",
            "collections",
        ]
        for field in list_fields:
            if doc.get(field):
                doc[field] = [clean_text(item) for item in doc[field] if item]

        if doc.get("date"):
            doc["date"] = self._normalize_date(doc["date"])

        return doc

    def _normalize_date(self, date_str: str) -> str:
        year_match = re.search(r"\b(19|20)\d{2}\b", date_str)
        return year_match.group() if year_match else date_str

    def _is_valid_document(self, doc: Dict[str, Any]) -> bool:
        if not doc.get("title") or not doc.get("abstract"):
            return False

        if len(doc["abstract"]) < MIN_ABSTRACT_LENGTH:
            return False

        if len(doc["abstract"]) > MAX_ABSTRACT_LENGTH:
            return False

        return True

    def save_collection(
        self, documents: List[Dict[str, Any]], filepath: str = JSON_FILE
    ) -> None:
        save_json(documents, filepath)
        print(f"{Fore.GREEN}Collection saved to: {filepath}{Style.RESET_ALL}")


def main():
    processor = DocumentProcessor()

    documents = processor.xml_to_json()

    processor.save_collection(documents)

    print(f"\n{Fore.MAGENTA}Collection statistics:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total documents: {len(documents)}{Style.RESET_ALL}")

    if documents:
        avg_abstract_len = sum(len(doc["abstract"]) for doc in documents) / len(
            documents
        )
        print(
            f"{Fore.BLUE}Average abstract length: {avg_abstract_len:.1f} characters{Style.RESET_ALL}"
        )

        languages = [doc["language"] for doc in documents if doc["language"]]
        print(f"{Fore.YELLOW}Languages found: {set(languages)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

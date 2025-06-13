import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import re
from utils import load_json, save_json
from colorama import Fore, Style, init

init(autoreset=True)


class DataValidator:
    def __init__(self):
        self.validation_stats = {
            "total_documents": 0,
            "duplicates_removed": 0,
            "invalid_removed": 0,
            "empty_abstracts": 0,
            "short_abstracts": 0,
            "missing_titles": 0,
            "final_documents": 0,
        }

    def validate_xml_before_processing(self, xml_filepath: str) -> str:
        print(f"{Fore.CYAN}Validating and cleaning XML file...{Style.RESET_ALL}")

        try:
            tree = ET.parse(xml_filepath)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"{Fore.RED}Error parsing XML: {e}{Style.RESET_ALL}")
            return xml_filepath

        records = root.findall(".//{http://www.openarchives.org/OAI/2.0/}record")
        print(f"{Fore.YELLOW}Found {len(records)} records in XML{Style.RESET_ALL}")

        seen_identifiers = set()
        unique_records = []
        duplicates_in_xml = 0

        for record in records:
            header = record.find(".//{http://www.openarchives.org/OAI/2.0/}header")
            if header is not None:
                identifier_elem = header.find(
                    "{http://www.openarchives.org/OAI/2.0/}identifier"
                )
                if identifier_elem is not None:
                    identifier = identifier_elem.text

                    if identifier not in seen_identifiers:
                        seen_identifiers.add(identifier)
                        unique_records.append(record)
                    else:
                        duplicates_in_xml += 1
                        print(
                            f"{Fore.RED}Duplicate XML record found: {identifier}{Style.RESET_ALL}"
                        )

        if duplicates_in_xml > 0:
            print(
                f"{Fore.YELLOW}Removed {duplicates_in_xml} duplicate records from XML{Style.RESET_ALL}"
            )

            cleaned_xml_path = xml_filepath.replace(".xml", "_cleaned.xml")

            new_root = ET.Element("collection")
            for recor in unique_records:
                new_root.append(record)

            tree = ET.ElementTree(new_root)
            tree.write(cleaned_xml_path, encoding="utf-8", xml_declaration=True)

            print(
                f"{Fore.GREEN}Cleaned XML saved to: {cleaned_xml_path}{Style.RESET_ALL}"
            )
            return cleaned_xml_path

        return xml_filepath

    def validate_and_clean_documents(
        self, documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        print(
            f"{Fore.CYAN}Starting validation of {len(documents)} documents...{Style.RESET_ALL}"
        )

        self.validation_stats["total_documents"] = len(documents)

        documents = self._remove_duplicates(documents)

        documents = self._validate_document_quality(documents)

        documents = self._clean_and_normalize(documents)

        documents = self._final_validation(documents)

        self.validation_stats["final_documents"] = len(documents)
        self._print_validation_report()

        return documents

    def _remove_duplicates(
        self, documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        print(f"{Fore.YELLOW}Removing duplicates...{Style.RESET_ALL}")

        seen_ids = set()
        no_id_duplicates = []

        for doc in documents:
            doc_id = doc.get("id", "")
            if doc_id and doc_id not in seen_ids:
                seen_ids.add(doc_id)
                no_id_duplicates.append(doc)
            elif not doc_id:
                no_id_duplicates.append(doc)

        id_duplicates_removed = len(documents) - len(no_id_duplicates)
        print(
            f"{Fore.BLUE}Removed {id_duplicates_removed} duplicate IDs{Style.RESET_ALL}"
        )

        seen_content = set()
        unique_documents = []

        for doc in no_id_duplicates:
            title = self._normalize_text(doc.get("title", ""))
            authors = sorted([self._normalize_text(a) for a in doc.get("authors", [])])
            date = doc.get("date", "")

            content_signature = f"{title}|{'|'.join(authors)}|{date}"

            if content_signature not in seen_content and title:
                seen_content.add(content_signature)
                unique_documents.append(doc)

        content_duplicates_removed = len(no_id_duplicates) - len(unique_documents)
        print(
            f"{Fore.BLUE}Removed {content_duplicates_removed} records with duplicate content{Style.RESET_ALL}"
        )

        self.validation_stats["duplicates_removed"] = (
            id_duplicates_removed + content_duplicates_removed
        )

        return unique_documents

    def _validate_document_quality(
        self, documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        print(f"{Fore.YELLOW}Validating document quality...{Style.RESET_ALL}")

        valid_documents = []

        for doc in documents:
            is_valid = True

            title = doc.get("title", "").strip()
            if not title:
                self.validation_stats["missing_titles"] += 1
                is_valid = False

            abstract = doc.get("abstract", "").strip()
            if not abstract:
                self.validation_stats["empty_abstracts"] += 1
                is_valid = False
            elif len(abstract) < 50:
                self.validation_stats["short_abstracts"] += 1
                is_valid = False

            if is_valid:
                valid_documents.append(doc)
            else:
                self.validation_stats["invalid_removed"] += 1

        print(
            f"{Fore.RED}Removed {self.validation_stats['invalid_removed']} invalid documents{Style.RESET_ALL}"
        )

        return valid_documents

    def _clean_and_normalize(
        self, documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        print(f"{Fore.YELLOW}Cleaning and normalizing data...{Style.RESET_ALL}")

        for doc in documents:
            if "title" in doc:
                doc["title"] = self._clean_text(doc["title"])

            if "abstract" in doc:
                doc["abstract"] = self._clean_text(doc["abstract"])

            if "authors" in doc:
                doc["authors"] = [
                    self._clean_text(author)
                    for author in doc["authors"]
                    if author.strip()
                ]

            if "keywords" in doc:
                doc["keywords"] = [
                    self._clean_text(kw) for kw in doc["keywords"] if kw.strip()
                ]

            if "date" in doc:
                doc["date"] = self._normalize_date(doc["date"])

        return documents

    def _final_validation(
        self, documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        print(f"{Fore.YELLOW}Final validation...{Style.RESET_ALL}")

        final_documents = []

        for doc in documents:
            if (
                doc.get("title", "").strip()
                and doc.get("abstract", "").strip()
                and len(doc.get("abstract", "")) >= 50
            ):
                final_documents.append(doc)

        return final_documents

    def _normalize_text(self, text: str) -> str:
        if not text:
            return ""

        text = text.lower().strip()

        text = re.sub(r"\s+", " ", text)

        text = re.sub(r"[^\w\s]", "", text)

        return text

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""

        text = "".join(char for char in text if ord(char) >= 32)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _normalize_date(self, date_str: str) -> str:
        if not date_str:
            return ""

        year_match = re.search(r"\b(19|20)\d{2}\b", str(date_str))
        return year_match.group() if year_match else str(date_str)

    def _print_validation_report(self):
        print("\n" + "=" * 60)
        print(f"{Fore.CYAN}DATA VALIDATION REPORT{Style.RESET_ALL}")
        print("=" * 60)

        stats = self.validation_stats

        print(
            f"{Fore.YELLOW}Original Documents:        {stats['total_documents']:,}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.RED}Duplicates Removed:        {stats['duplicates_removed']:,}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.RED}Invalid Documents Removed: {stats['invalid_removed']:,}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.RED}  - Missing Titles:        {stats['missing_titles']:,}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.RED}  - Empty Abstracts:       {stats['empty_abstracts']:,}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.RED}  - Short Abstracts:       {stats['short_abstracts']:,}{Style.RESET_ALL}"
        )
        print("-" * 40)
        print(
            f"{Fore.GREEN}Valid Documents:     {stats['final_documents']:,}{Style.RESET_ALL}"
        )

        if stats["total_documents"] > 0:
            retention_rate = (stats["final_documents"] / stats["total_documents"]) * 100
            print(
                f"{Fore.BLUE}Retention Rate:            {retention_rate:.1f}%{Style.RESET_ALL}"
            )

        print("=" * 60)


def main():
    from config import JSON_FILE

    validator = DataValidator()

    print(f"{Fore.CYAN}Loading document collection...{Style.RESET_ALL}")
    documents = load_json(JSON_FILE)

    backup_file = JSON_FILE.replace(".json", "_before_validation.json")
    save_json(documents, backup_file)
    print(f"{Fore.GREEN}Backup created: {backup_file}{Style.RESET_ALL}")

    clean_documents = validator.validate_and_clean_documents(documents)

    save_json(clean_documents, JSON_FILE)
    print(f"{Fore.GREEN}Validated collection saved to: {JSON_FILE}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

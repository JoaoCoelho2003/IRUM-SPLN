import requests
import time
import os
from typing import Optional
import xml.etree.ElementTree as ET
from config import *
from utils import ensure_dir

class RepositoriumExtractor:    
    def __init__(self, base_url: str = REPOSITORIUM_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        
    def extract_collection(self, collection_id: str, max_records: int = MAX_RECORDS) -> str:
        print(f"A iniciar extração da coleção {collection_id}")

        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<collection>\n'
        records_count = 0
        resumption_token = None

        while records_count < max_records:
            if resumption_token:
                params = {
                    "verb": "ListRecords",
                    "resumptionToken": resumption_token
                }
            else:
                params = {
                    "verb": "ListRecords",
                    "metadataPrefix": METADATA_PREFIX,
                    "set": collection_id
                }

            try:
                response = self.session.get(self.base_url, params=params, timeout=30)
                response.raise_for_status()
                response_xml = response.text
            except requests.RequestException as e:
                print(f"Erro na requisição: {e}")
                break

            if "noRecordsMatch" in response_xml:
                print("Sem registos encontrados.")
                break

            try:
                root = ET.fromstring(response_xml)
                records = root.findall(".//{http://www.openarchives.org/OAI/2.0/}record")
                for record in records:
                    xml_content += ET.tostring(record, encoding='unicode') + '\n'
                    records_count += 1
                    if records_count >= max_records:
                        break

                rt_elem = root.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken")
                if rt_elem is not None and rt_elem.text:
                    resumption_token = rt_elem.text.strip()
                    print(f"Novo resumptionToken: {resumption_token}")
                    time.sleep(1)
                else:
                    print("Fim dos registos.")
                    break

            except ET.ParseError as e:
                print(f"Erro ao fazer parse do XML: {e}")
                break

        xml_content += '</collection>'
        print(f"Extração concluída: {records_count} registos")
        return xml_content
    
    def _extract_batch(self, collection_id: str, offset: int) -> Optional[str]:
        params = {
            "verb": "ListRecords",
            "resumptionToken": f"{METADATA_PREFIX}///{collection_id}/{offset}"
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.text
            
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None
    
    def save_xml(self, xml_content: str, filepath: str = XML_FILE) -> None:
        ensure_dir(os.path.dirname(filepath))
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_content)
            
        print(f"XML guardado em: {filepath}")

def main():
    extractor = RepositoriumExtractor()
    
    collection_id = COLLECTIONS["msc_di"]
    xml_data = extractor.extract_collection(collection_id, max_records=100)
    
    extractor.save_xml(xml_data)
    
    print("Extração concluída com sucesso!")

if __name__ == "__main__":
    main()

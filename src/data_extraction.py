import requests
import time
import os
from typing import Tuple
import xml.etree.ElementTree as ET
from config import *
from utils import ensure_dir
import random

class CollectionExtractor:    
    def __init__(self, base_url: str = REPOSITORIUM_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def extract_multiple_collections(self, collections: dict, max_records: int = MAX_RECORDS) -> str:
        print(f"A iniciar extração de múltiplas coleções")
        print(f"Coleções disponíveis: {list(collections.keys())}")
        print(f"Objetivo total: {max_records} registos")
        print("="*60)

        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<collection>\n'
        total_records = 0
        collection_stats = {}

        for collection_name, collection_id in collections.items():
            if total_records >= max_records:
                print(f"Objetivo de {max_records} registos atingido!")
                break
                
            remaining_records = max_records - total_records
            print(f"\n📁 COLEÇÃO: {collection_name} ({collection_id})")
            print(f"Registos restantes necessários: {remaining_records}")
            print("-" * 40)
            
            try:
                collection_xml, records_extracted = self.extract_single_collection(
                    collection_id, remaining_records
                )
                
                if records_extracted > 0:
                    collection_records = self._extract_records_from_xml(collection_xml)
                    xml_content += collection_records
                    
                    total_records += records_extracted
                    collection_stats[collection_name] = records_extracted
                    
                    print(f"✅ Extraídos {records_extracted} registos de {collection_name}")
                    print(f"📊 Total acumulado: {total_records}/{max_records}")
                else:
                    print(f"❌ Nenhum registo encontrado em {collection_name}")
                    collection_stats[collection_name] = 0
                    
            except Exception as e:
                print(f"❌ Erro ao extrair de {collection_name}: {e}")
                collection_stats[collection_name] = 0
                continue

        xml_content += '</collection>'
        
        print("\n" + "="*60)
        print("📈 ESTATÍSTICAS FINAIS DA EXTRAÇÃO")
        print("="*60)
        for collection_name, count in collection_stats.items():
            percentage = (count / total_records * 100) if total_records > 0 else 0
            print(f"{collection_name:15}: {count:4d} registos ({percentage:5.1f}%)")
        print("-" * 40)
        print(f"{'TOTAL':15}: {total_records:4d} registos")
        print("="*60)
        
        return xml_content
    
    def extract_single_collection(self, collection_id: str, max_records: int) -> Tuple[str, int]:
        records_count = 0
        resumption_token = None
        consecutive_errors = 0
        max_consecutive_errors = MAX_CONSECUTIVE_ERRORS
        collection_records = ""

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

            success = False
            for attempt in range(3):
                try:
                    if attempt > 0:
                        delay = (2 ** attempt) + random.uniform(0, 1)
                        print(f"  Tentativa {attempt + 1} após {delay:.1f}s...")
                        time.sleep(delay)
                    
                    response = self.session.get(self.base_url, params=params, timeout=EXTRACTION_TIMEOUT)
                    response.raise_for_status()
                    response_xml = response.text
                    success = True
                    consecutive_errors = 0
                    break
                    
                except requests.RequestException as e:
                    print(f"  Erro na tentativa {attempt + 1}: {e}")
                    if attempt == 2:
                        consecutive_errors += 1

            if not success:
                if consecutive_errors >= max_consecutive_errors:
                    print(f"  Muitos erros consecutivos. A parar esta coleção.")
                    break
                else:
                    continue

            if "noRecordsMatch" in response_xml:
                print(f"  Sem mais registos nesta coleção.")
                break

            try:
                root = ET.fromstring(response_xml)
                records = root.findall(".//{http://www.openarchives.org/OAI/2.0/}record")
                
                batch_count = 0
                for record in records:
                    collection_records += ET.tostring(record, encoding='unicode') + '\n'
                    records_count += 1
                    batch_count += 1
                    if records_count >= max_records:
                        break

                print(f"  Lote: {batch_count} registos | Total da coleção: {records_count}")

                rt_elem = root.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken")
                if rt_elem is not None and rt_elem.text:
                    resumption_token = rt_elem.text.strip()
                    
                    delay = BASE_DELAY + random.uniform(0, 0.5)
                    time.sleep(delay)
                else:
                    print(f"  Fim dos registos desta coleção.")
                    break

            except ET.ParseError as e:
                print(f"  Erro ao fazer parse do XML: {e}")
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    break
                continue

        return collection_records, records_count
    
    def _extract_records_from_xml(self, xml_content: str) -> str:
        return xml_content
    
    def save_xml(self, xml_content: str, filepath: str = XML_FILE) -> None:
        ensure_dir(os.path.dirname(filepath))
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_content)
            
        print(f"\n💾 XML guardado em: {filepath}")
        
        file_size = os.path.getsize(filepath) / (1024 * 1024)
        print(f"📁 Tamanho do ficheiro: {file_size:.2f} MB")

def main():
    extractor = CollectionExtractor()
    
    xml_data = extractor.extract_multiple_collections(COLLECTIONS, max_records=MAX_RECORDS)
    
    extractor.save_xml(xml_data)
    
    print("\n🎉 Extração multi-coleção concluída com sucesso!")

if __name__ == "__main__":
    main()

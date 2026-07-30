import os, re, json, time, datetime, urllib.request
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv('/opt/sintezium/core/.env')

print('\n' + '='*70)
print('  🧠 SINTEZIUM V7: ОБОГАЩЕНИЕ БАЗЫ ЗНАНИЙ AI-АГЕНТОВ (NESTOR DESCI INGESTION)')
print('='*70 + '\n')

NESTOR_BASE_URL = 'https://nestor.minsk.by'
CATEGORIES_TO_INGEST = [
    '/kg/abc/soft-%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D1%8C/',
    '/kg/abc/%D1%80%D0%BE%D0%B1%D0%BE%D1%82%D0%BE%D1%82%D0%B8%D0%BA%D0%B0/',
    '/kg/abc/%D1%80%D0%B0%D0%B7%D0%BD%D0%BE%D0%B5-%D0%BA%D0%B8%D0%B1%D0%B5%D1%80%D0%BF%D0%B0%D0%BD%D0%BA/'
]

KNOWLEDGE_OUTPUT_DIR = '/opt/sintezium/knowledge'
KNOWLEDGE_FILE = os.path.join(KNOWLEDGE_OUTPUT_DIR, 'nestor_desci_knowledge.json')

def fetch_and_parse_category(category_url):
    full_url = NESTOR_BASE_URL + category_url
    print(f'[1/3] Загрузка рубрики: {full_url}...')
    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0 (Sintezium AI Bot)'})
        html_content = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        
        soup = BeautifulSoup(html_content, 'html.parser')
        article_links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if re.search(r'/kg/\d{4}/\d{2}/', href) or re.search(r'/kg/abc/', href):
                if href.startswith('/'):
                    article_links.append(NESTOR_BASE_URL + href)
                elif href.startswith('http'):
                    article_links.append(href)
                    
        return list(set(article_links))[:10]
    except Exception as e:
        print(f'  [FAIL] Ошибка загрузки рубрики {category_url}: {e}')
        return []

def build_knowledge_base():
    os.makedirs(KNOWLEDGE_OUTPUT_DIR, exist_ok=True)
    all_knowledge_entries = []
    
    for cat in CATEGORIES_TO_INGEST:
        links = fetch_and_parse_category(cat)
        print(f'  - Найдено {len(links)} статей...')
        
        for link in links[:3]:
            print(f'[2/3] Обогащение знаниями статьи: {link}...')
            try:
                req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0 (Sintezium AI Bot)'})
                page_html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
                soup = BeautifulSoup(page_html, 'html.parser')
                
                title = soup.title.string.strip() if soup.title else 'Без названия'
                paragraphs = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text().strip()) > 30]
                summary = ' '.join(paragraphs[:5])
                
                entry = {
                    'title': title,
                    'url': link,
                    'ingested_at': datetime.datetime.now().isoformat(),
                    'summary': summary[:1000],
                    'category': cat,
                    'tags': ['DeSci', 'Computer History', 'Sintezium Knowledge']
                }
                all_knowledge_entries.append(entry)
                time.sleep(0.5)
            except Exception as e:
                print(f'  [SKIP] Ошибка парсинга {link}: {e}')
                
    print(f'\n[3/3] Сохранение знания в {KNOWLEDGE_FILE}...')
    with open(KNOWLEDGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_knowledge_entries, f, ensure_ascii=False, indent=2)
        
    print(f'  [SUCCESS!] База знаний AI-Агентов Sintezium V7 пополнена!')

if __name__ == '__main__':
    build_knowledge_base()

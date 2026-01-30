import requests
from bs4 import BeautifulSoup

def extract_berlin_jobs(keyword):
    # 주소 끝에 슬래시(/) 필수!
    url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"Scanning Berlin for {keyword}...")
    try:
        response = requests.get(url, headers=headers)
        # 404가 뜨거나 리다이렉트 되면 검색 결과가 없는 것
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        # 클래스 이름보다는 구조로 찾기 (bjs-jlid 클래스 사용)
        # 만약 클래스가 바뀌어도 li 태그들을 다 가져오도록 함
        jobs = soup.find_all("li", class_="bjs-jlid")
        
        results = []
        
        for job in jobs:
            try:
                # h4 태그 안에 있는 링크가 진짜 직업 링크임
                h4 = job.find("h4")
                if not h4: continue
                
                link_tag = h4.find("a")
                if not link_tag: continue
                
                title = link_tag.text.strip()
                link = link_tag['href']
                
                # 회사 이름
                company_link = job.find("a", class_="bjs-jlid__b")
                company = company_link.text.strip() if company_link else "Berlin Startup"
                
                results.append({
                    "company": company,
                    "title": title,
                    "link": link,
                    "source": "BerlinStartupJobs"
                })
            except:
                continue
        return results
    except:

        return []

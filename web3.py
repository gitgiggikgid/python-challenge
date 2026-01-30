import requests
from bs4 import BeautifulSoup

def extract_web3_jobs(keyword):
    url = f"https://web3.career/{keyword}-jobs"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    
    print(f"[Web3] Scanning for {keyword}...")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        
        # 1. 이미지에 나온대로 table_row 클래스를 가진 tr들 다 찾기
        job_rows = soup.find_all("tr", class_="table_row")
        results = []

        for row in job_rows:
            try:
                # 2. 제목이 있는 div (job-title-mobile) 찾기
                title_div = row.find("div", class_="job-title-mobile")
                if not title_div:
                    continue
                
                # 3. 그 안의 a 태그에서 제목 텍스트와 링크 가져오기
                anchor = title_div.find("a")
                if not anchor:
                    continue
                
                title = anchor.get_text(strip=True)
                link = anchor['href'] # 이미지 보면 /principal-... 처럼 상대경로임
                
                # 4. 회사명 찾기 (이미지상 ps-2 클래스 주변 혹은 다른 div에 있을 확률 높음)
                # 우선 안전하게 해당 row 내의 텍스트 중 제목이 아닌 걸로 추정되는 부분 탐색
                company_div = row.find("div", class_="ps-2") # 이미지상 제목 바로 위 부모 div
                # 회사명 태그가 별도로 없다면 h3나 다른 div를 탐색하는 로직
                company = "Company Name" # 기본값
                
                # 보통 Web3는 제목 근처 h3에 회사명이 있음
                c_tag = row.find("h3")
                if c_tag:
                    company = c_tag.get_text(strip=True)

                results.append({
                    "company": company,
                    "title": title,
                    "link": f"https://web3.career{link}",
                    "source": "Web3.Career"
                })
            except Exception as e:
                print(f"Error parsing a row: {e}")
                continue
        
        print(f"[Web3] Successfully found {len(results)} jobs!")
        return results
    except Exception as e:
        print(f"[Web3] Connection Error: {e}")
        return []
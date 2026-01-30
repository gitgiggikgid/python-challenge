import requests
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    
    # 과제 템플릿에서 제공한 헤더 (이걸 쓰는 게 가장 모범답안)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    print(f"[WWR] Searching {url}...")
    try:
        response = requests.get(url, headers=headers)
        
        # 403 등 에러가 발생하면 빈 리스트 반환 (과제 지침 준수)
        if response.status_code != 200:
            print(f"[WWR] Access restricted by site (Status: {response.status_code}) - Skipping per instructions.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        
        # 검색 결과는 보통 <section class="jobs"> 안에 <li class="feature"> 등으로 존재
        jobs_container = soup.find("section", class_="jobs")
        
        # 만약 section.jobs가 없으면 article 구조일 수도 있으니 대비
        if not jobs_container:
            jobs_container = soup.find("article")
            
        if not jobs_container:
            print("[WWR] No job container found.")
            return []

        posts = jobs_container.find_all("li")
        results = []

        for post in posts:
            # 'view-all' 버튼 제외
            if "view-all" in post.get("class", []):
                continue
            
            # 정보 추출
            try:
                anchors = post.find_all("a")
                # 링크가 2개 이상이어야 정상적인 게시물 (로고 + 텍스트)
                if len(anchors) >= 2:
                    link = anchors[1]["href"]
                    # 링크가 상대경로(/...)인 경우만 처리
                    if link.startswith("/"):
                        full_link = f"https://weworkremotely.com{link}"
                        
                        title = post.find("span", class_="title").get_text(strip=True)
                        company = post.find("span", class_="company").get_text(strip=True)
                        
                        results.append({
                            "company": company,
                            "title": title,
                            "link": full_link,
                            "source": "WeWorkRemotely"
                        })
            except:
                continue
        
        print(f"[WWR] Found {len(results)} jobs!")
        return results

    except Exception as e:
        print(f"[WWR] Error occurred: {e}")
        return []
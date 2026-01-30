from flask import Flask, render_template
from extractors.wwr import extract_wwr_jobs
from extractors.web3 import extract_web3_jobs
from extractors.berlin import extract_berlin_jobs  # 여기 추가됨!

app = Flask("JobScraper")

@app.route("/")
def home():
    keyword = "python" # 원하는 검색어로 변경 가능
    
    print(f"Scraping WWR for {keyword}...")
    wwr = extract_wwr_jobs(keyword)
    
    print(f"Scraping Web3 for {keyword}...")
    web3 = extract_web3_jobs(keyword)
    
    print(f"Scraping BerlinStartupJobs for {keyword}...")
    berlin = extract_berlin_jobs(keyword) # 여기 실행!
    
    # 3개 리스트 합치기
    jobs = wwr + web3 + berlin
    
    print(f"Total {len(jobs)} jobs found.")
    return render_template("home.html", keyword=keyword, jobs=jobs, count=len(jobs))

if __name__ == "__main__":
    with app.app_context():
        rendered_html = home()
        with open("index.html", "w", encoding="utf-8") as file:
            file.write(rendered_html)
        print("✅ Done! 'index.html' generated successfully.")
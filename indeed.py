import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=50&l=Centreville%2C+VA+20120&fromage=any&limit={LIMIT}"
# URL = f"https://www.indeed.com/jobs?q=python&limit=50&radius=25&start=0"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]

    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"}).get_text(strip=True)
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    # company_anchor = company.find("a")
    # if company_anchor is not None:
    #     print(company_anchor.string)
    # else:
    #     print(company.string)
    # print(job_id)
    return{"title": title, "company": company, "location": location, "link": f"https://www.indeed.com/viewjob?jk={job_id}"}


def extract_jobs(last_page):
    jobs = []

    for page in range(last_page):
        # result = requests.get(f"{URL}&start={1*LIMIT}")
        print(f"Scrapping Indeed - Page: {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    # print(jobs)
    return jobs

    # print(result.status_code)
    # # print(results)

    # for result in results:
    #     title = result.find("h2", {"class":"title"}).find("a")["title"]
    #     company = result.find("span", {"class":"company"}).get_text(strip=True)
    #     # company_anchor = company.find("a")
    #     # if company_anchor is not None:
    #     #     print(company_anchor.string)
    #     # else:
    #     #     print(company.string)

    #     print(title, company)

def get_jobs():
    last_page = get_last_page()
    # jobs = extract_jobs(last_page)
    jobs = extract_jobs(last_page)

    return jobs
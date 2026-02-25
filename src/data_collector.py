import requests
from bs4 import BeautifulSoup
import json
import time
import os

# Refined corpus of 20+ URLs for ICICI Prudential MF
URLS = [
    # ICICI Prudential Bluechip Fund
    "https://groww.in/mutual-funds/icici-prudential-bluechip-fund-direct-growth",
    "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-bluechip-fund",
    "https://www.moneycontrol.com/mutual-funds/nav/icici-prudential-bluechip-fund-direct-plan-growth/PPR381",
    "https://groww.in/blog/icici-prudential-bluechip-fund-review",
    
    # ICICI Prudential Flexicap Fund
    "https://groww.in/mutual-funds/icici-prudential-flexicap-fund-direct-growth",
    "https://www.icicipruamc.com/mutual-fund/equity-funds/icici-prudential-flexicap-fund",
    "https://www.etmoney.com/mutual-funds/icici-prudential-flexi-cap-fund-direct-growth/41130",
    "https://groww.in/blog/icici-prudential-flexi-cap-fund-review",
    
    # ICICI Prudential ELSS Tax Saver
    "https://groww.in/mutual-funds/icici-prudential-elss-tax-saver-fund-direct-growth",
    "https://www.icicipruamc.com/mutual-fund/tax-saving-funds/icici-prudential-elss-tax-saver-fund",
    "https://www.indmoney.com/mutual-funds/icici-prudential-elss-tax-saver-fund-direct-growth",
    "https://groww.in/blog/icici-prudential-elss-tax-saver-fund-review",
    
    # FAQs & Investor Services
    "https://groww.in/help/mutual-funds",
    "https://groww.in/help/mutual-funds/tax/how-to-download-capital-gains-statement",
    "https://groww.in/help/mutual-funds/elss/lock-in-period",
    "https://groww.in/help/mutual-funds/investing/what-is-expense-ratio",
    "https://groww.in/help/mutual-funds/investing/what-is-exit-load",
    "https://groww.in/help/mutual-funds/investing/what-is-nav",
    "https://groww.in/help/mutual-funds/investing/what-is-folio-number",
    "https://www.icicipruamc.com/investor-services/investor-faq",
    "https://www.icicipruamc.com/resources/fund-documents",
    "https://www.icicipruamc.com/resources/factsheets",
    "https://www.icicipruamc.com/resources/statutory-disclosures",
    "https://www.icicipruamc.com/about-us",
    "https://www.icicipruamc.com/mutual-fund/equity-funds",
    "https://www.icicipruamc.com/mutual-fund/tax-saving-funds",
    "https://groww.in/blog/how-to-invest-in-mutual-funds",
    "https://groww.in/blog/mutual-fund-investing-for-beginners",
    "https://groww.in/academy/guides/what-is-elss",
    "https://groww.in/academy/guides/icici-prudential-mutual-fund",
    "https://groww.in/help/mutual-funds/investing/min-sip-amount"
]

def scrape_url(url):
    print(f"Scraping {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            if url.endswith(".pdf"):
                return {
                    "source": url,
                    "title": "PDF Document: " + url.split("/")[-1],
                    "content": "[PDF Content - Binary data skipped for now. Focus on HTML guides.]"
                }
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract main text content
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.extract()
            
            # Focus on article or main content if available
            main_content = soup.find('article') or soup.find('main') or soup.body
            text = main_content.get_text(separator=' ') if main_content else soup.get_text(separator=' ')
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return {
                "source": url,
                "title": soup.title.string.strip() if soup.title else url,
                "content": text
            }
        else:
            print(f"Failed to fetch {url}: Status {response.status_code}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return None

def main():
    data = []
    if not os.path.exists("data"):
        os.makedirs("data")
        
    for url in URLS:
        result = scrape_url(url)
        if result:
            data.append(result)
        time.sleep(1.5) # Politeness
        
    with open("data/raw_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Finished scraping {len(data)} pages. Saved to data/raw_data.json")

if __name__ == "__main__":
    main()

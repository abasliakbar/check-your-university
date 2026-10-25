# Check Your University

A straightforward web app to help applicants see which university programs they are eligible for based on their test scores. 

## Data scraping

The program list and cutoff scores are scraped directly from qebulol.az using a Python script. The scraper currently uses these 2027 group pages:

- [1-ci qrup](https://qebulol.az/1-ci-qrup-kecid-ballari-2027/)
- [2-ci qrup](https://qebulol.az/2-ci-qrup-kecid-ballari-2027/)
- [3-cü qrup](https://qebulol.az/3-cu-qrup-kecid-ballari-2027/)
- [4-cü qrup](https://qebulol.az/4-cu-qrup-kecid-ballari-2027/)
- [5-ci qrup](https://qebulol.az/5-ci-qrup-kecid-ballari-2027/)

To re-run the scraper:

```bash
cd scraper
# If you don't have a virtual environment:
python3 -m venv venv
source venv/bin/activate
# Install requirements
pip install -r requirements.txt
# Run the scraper
python scrape.py
```

This regenerates the JSON files under `data/groups/`, which the live app fetches. The app shows paid and state-funded cutoffs separately; the eligibility filter includes programs where the entered score meets either cutoff.

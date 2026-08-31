# Check Your University

A straightforward web app to help applicants see which university programs they are eligible for based on their test scores. 

## Data scraping

The program list and cutoff scores are scraped directly from [qebulol.az](https://qebulol.az) using a Python script. To re-run the scraper (for example, for the next admission cycle or if cutoff scores are updated):

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

This will automatically re-generate the JSON files under the `data/groups/` directory, which the live app fetches.

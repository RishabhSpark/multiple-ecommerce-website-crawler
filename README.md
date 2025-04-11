# Product URL Web Crawler

A powerful and customizable web crawler built with Python and Selenium to extract product URLs from multiple e-commerce websites, including support for infinite scrolling and JavaScript-heavy sites like Nykaa Fashion.

## Features

- Extracts product links from one or more collection URLs.
- Supports custom patterns per website.
- Automatically scrolls and detects lazy-loaded content.
- Uses JavaScript injection for dynamic websites like Nykaa.
- Easily configurable through JSON/YAML configs.
- Logs progress and avoids duplicates.

## Requirements

- Python 3.8+
- Google Chrome
- ChromeDriver

### Python Dependencies

Install the dependencies with:

```bash
pip install -r requirements.txt


### Github Actions
This workflow runs when triggered manually on GitHub under Actions → Run workflow.
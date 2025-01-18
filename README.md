# BoxOfficeMojo Scraper: Scrapy + Selenium + PostgreSQL

## Overview
This repository contains a robust implementation for scraping movie data from the **BoxOfficeMojo** website using **Scrapy** and **Selenium**. The project collects data about top-grossing movies, including their rank, title, lifetime gross, year, budget, MPAA rating, and runtime. Additionally, the scraped data is stored in a **PostgreSQL database** for further analysis.

---

## Features

1. **Scrapy Framework Integration**
   - Scrapy is used as the primary framework for web scraping, handling requests, responses, and item pipelines efficiently.

2. **Selenium for JavaScript Rendering**
   - Selenium is utilized to manage pages with dynamic content, ensuring accurate scraping of JavaScript-loaded elements like movie details.

3. **Custom Middleware**
   - Includes custom middleware for proxy handling and integrating Selenium with Scrapy.

4. **PostgreSQL Database Integration**
   - Scraped data is stored in a PostgreSQL database with a defined schema for structured and persistent storage.

5. **Dynamic Pagination**
   - Handles multiple pages of results dynamically, scraping only movies within a defined year range.

6. **Detailed Data Extraction**
   - Collects detailed data for each movie, including:
     - **Rank**
     - **Title**
     - **Lifetime Gross**
     - **Year**
     - **Budget**
     - **MPAA Rating**
     - **Running Time**

7. **Scalable Architecture**
   - Modular design with clear separation of spiders, middlewares, settings, and pipelines for scalability and maintainability.

---

## Code Highlights

### 1. Spider: `BoxOfficeSpider`
- Handles crawling the BoxOfficeMojo website.
- Implements dynamic pagination and uses Selenium to render pages and extract data.

### 2. Middleware
- **CustomProxyMiddleware**: Configures requests to use a proxy.
- **CustomSeleniumMiddleware**: Manages Selenium driver options, including proxy setup and headless mode.

### 3. Pipeline: `PostgresPipeline`
- Inserts scraped data into a PostgreSQL database with automatic table creation.

### 4. Settings
- Configured for Scrapy-Selenium integration.
- Optimized with user-agent settings and appropriate Selenium driver options.

### 5. Database Schema
PostgreSQL table creation script:
```sql
CREATE TABLE IF NOT EXISTS movies (
    rank TEXT,
    title TEXT,
    lifetime_gross TEXT,
    year TEXT,
    budget TEXT,
    mpaa_rating TEXT,
    running_time TEXT
);

imdb_scraper/
│
├── imdb_scraper/
│   ├── spiders/
│   │   └── boxoffice_spider.py      # Main spider script
│   ├── middlewares.py               # Middleware for proxies and Selenium
│   ├── pipelines.py                 # PostgreSQL pipeline
│   └── settings.py                  # Scrapy settings
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation


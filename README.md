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


# Installation and Setup

## 1. Install Dependencies
Python 3.8+ is required.  
Install the required Python packages by running the following command:

pip install scrapy scrapy-selenium psycopg2-binary


This will install:
- `scrapy`: A powerful web scraping framework.
- `scrapy-selenium`: Integrates Selenium with Scrapy for scraping dynamic pages.
- `psycopg2-binary`: A PostgreSQL adapter for Python to interact with your database.

## 2. Proxy Manager
To manage proxies, download and use the **Luminati Proxy Manager** from the following link:

https://github.com/luminati-io/luminati-proxy/


Follow the instructions in the repository to configure the proxy manager and integrate it into your scraping project.

## 3. Download and Configure Chrome WebDriver
For Selenium to interact with Chrome, you need to download the **Chrome WebDriver**.

1. Visit the official site for Chrome WebDriver: [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/)
2. Download the appropriate version based on your installed Chrome browser.
3. Set the path to the `chromedriver` executable in your project. For example:

SELENIUM_DRIVER_EXECUTABLE_PATH = r'/Users/masoud/Downloads/chromedriver'


Make sure the path corresponds to where you have saved the `chromedriver` on your system.

---

With these steps completed, you'll be ready to start scraping with Scrapy, Selenium, and manage proxies using Luminati.

### Run the Spider

To run the Scrapy spider named `boxoffice` and output the scraped data to a file called `boxoffice.csv`, use the following command:

```bash
scrapy crawl boxoffice -o boxoffice.csv

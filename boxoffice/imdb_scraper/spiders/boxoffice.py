from scrapy_selenium import SeleniumRequest
from scrapy.spiders import Spider
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BoxOfficeSpider(Spider):
    name = "boxoffice"
    allowed_domains = ["boxofficemojo.com"]
    start_urls = [
        "https://www.boxofficemojo.com/chart/top_lifetime_gross/?area=XWW"
    ]
    page_number = 0
    # Define year range
    start_year = 2018
    end_year = 2023

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=3,
                screenshot=False,
            )

    def parse(self, response):
        driver = response.meta["driver"]
        movie_data = []  # Store all movie data from current page
        found_movies = False  # Flag to track if we found any movies in our year range

        # Wait for the table to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.mojo-body-table"))
            )
        except Exception as e:
            self.log(f"Error waiting for the table to load: {e}")
            return

        # Extract rows from the table
        rows = driver.find_elements(By.CSS_SELECTOR, "table.mojo-body-table tr")
        if not rows:
            self.log("No rows found in the table.")
            return

        # First collect all basic data from the table
        for row in rows[1:]:  # Skip header row
            try:
                # Get year first to check if we should process this movie
                year = int(row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text)
                
                # Only process movies within our year range
                if self.start_year <= year <= self.end_year:
                    found_movies = True
                    
                    # Extract basic info
                    rank = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
                    title_element = row.find_elements(By.CSS_SELECTOR, "td:nth-child(2) a")
                    if title_element:
                        title = title_element[0].text
                        movie_url = title_element[0].get_attribute('href')
                    else:
                        title = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
                        movie_url = None
                    
                    lifetime_gross = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text

                    movie_data.append({
                        'rank': rank,
                        'title': title,
                        'lifetime_gross': lifetime_gross,
                        'year': str(year),
                        'url': movie_url
                    })

            except Exception as e:
                self.log(f"Error collecting basic data: {e}")

        # Now process each movie's details
        for movie in movie_data:
            try:
                if movie['url']:
                    # Navigate to movie detail page
                    driver.get(movie['url'])
                    
                    # Wait for summary values to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".mojo-summary-values"))
                    )
                    
                    summary_values = driver.find_element(By.CSS_SELECTOR, ".mojo-summary-values")
                    
                    # Get Budget
                    budget = "N/A"
                    budget_element = summary_values.find_elements(By.XPATH, ".//div[span[text()='Budget']]//span[2]")
                    if budget_element:
                        budget = budget_element[0].text
                    
                    # Get MPAA
                    mpaa = "N/A"
                    mpaa_element = summary_values.find_elements(By.XPATH, ".//div[span[text()='MPAA']]//span[2]")
                    if mpaa_element:
                        mpaa = mpaa_element[0].text
                    
                    # Get Running Time
                    running_time = "N/A"
                    running_time_element = summary_values.find_elements(By.XPATH, ".//div[span[text()='Running Time']]//span[2]")
                    if running_time_element:
                        running_time = running_time_element[0].text

                    time.sleep(1)  # Small delay to avoid overwhelming the server
                else:
                    budget = mpaa = running_time = "N/A"

                yield {
                    'rank': movie['rank'],
                    'title': movie['title'],
                    'lifetime_gross': movie['lifetime_gross'],
                    'year': movie['year'],
                    'budget': budget,
                    'mpaa_rating': mpaa,
                    'running_time': running_time
                }

            except Exception as e:
                self.log(f"Error processing details for {movie['title']}: {e}")
                yield {
                    'rank': movie['rank'],
                    'title': movie['title'],
                    'lifetime_gross': movie['lifetime_gross'],
                    'year': movie['year'],
                    'budget': 'N/A',
                    'mpaa_rating': 'N/A',
                    'running_time': 'N/A'
                }

        # After processing all movies on the current page, check if we should move to next page
        if found_movies:  # Only continue if we found movies in our year range
            self.page_number += 200
            next_page = response.urljoin(self.start_urls[0] + f"&offset={self.page_number}")
            self.log(f"Navigating to next page: {next_page}")
            yield SeleniumRequest(url=next_page, callback=self.parse, wait_time=3)
        else:
            self.log("No more movies found in the specified year range. Stopping.")
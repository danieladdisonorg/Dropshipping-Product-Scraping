# Dropshipping-Product-Scraping
Data Scraper Project

Description

This project consists of two Python scripts: main_data_scraper and product_info. They are designed to automate the extraction and processing of product information from eCommerce websites using web scraping and browser automation technologies. The primary goal is to gather data about products, including product characteristics and images.

The project includes non-standard solutions to bypass anti-bot mechanisms, flexible data processing methods, and handling dynamic content.

Project Structure

main_data_scraper:

The main script for scraping data from web pages.
Collects data from multiple pages, including links to individual products and their attributes.
Takes into account anti-bot measures such as hiding automation using Selenium and using various User-Agent headers to mimic real users.

product_info:

An additional script to collect detailed information about each product (images, models, compatibility).
Uses dynamic interaction with page elements to collect data.
Saves data in CSV format with subsequent cleaning and processing for ease of use.

Key Features

Selenium for Browser Automation:

Used to work with dynamic content (e.g., buttons that appear only after user interactions).
Data is loaded after clicks or interaction with elements, which would be impossible without using a real browser.
Runs in headless mode to speed up the process without UI interaction.

Bypassing Anti-Bot Protections:

Includes methods to hide automation, such as using different User-Agent headers, adding delays between requests, and hiding signs of automated behavior through Chrome options.
Random delays between requests to reduce the likelihood of being blocked.

Handling Dynamic Content:

The scripts efficiently interact with pages and elements that load via JavaScript.
Automated navigation, button clicks, and handling pop-ups are implemented.

Data Processing and Cleaning:

Extracts key data such as images, model numbers, and compatibility and saves it in a convenient CSV format.
Processed data includes concatenating model and year information for each product.
Each entry is accompanied by the product image, which is a valuable addition for data analysis.
Non-Standard Solutions
Interactive Element Interaction: Instead of regular HTML parsing using BeautifulSoup, the project uses Selenium to perform actions on page elements, allowing it to handle dynamically loaded data and avoid issues with site blocking.

Using Random User-Agents and Delays: Instead of using a single fixed User-Agent, the project randomly generates different agents, which helps bypass anti-bot filters and makes actions on the site appear more like those of a real user.


Flexible Image Handling: The script features a mechanism to retrieve product images, even if the image is not available by default. If no image is found, a "No Image" entry is recorded in the CSV.

Multi-Tasking with WebDriverWait: To improve stability and proper interaction with page elements, the Selenium WebDriverWait library is used, allowing the script to wait for elements to appear before interacting with them.

Requirements:
-Python 3.6+
-Selenium
-WebDriver Manager
-BeautifulSoup
-lxml
-requests
-csv

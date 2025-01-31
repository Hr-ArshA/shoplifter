# Advanced Web Crawler

![image created with https://mann-e.com/](banner.jpg)

## Project Overview

This project aims to build a powerful **web crawler** that collects product information (such as price, title, description, and image) from multiple e-commerce websites. The crawler stores the data in a MySQL database while ensuring performance optimization and reliability. It is designed to be flexible, scalable, and resistant to common challenges like rate limiting, CAPTCHA, and IP blocking.

The crawler is capable of crawling **multiple domains** with different HTML structures and uses robust **error management** to handle various HTTP errors. It also features advanced **request management** and **data storage** for high-quality, sustainable web scraping.

## Features

### 1. Request Management (Rate Limiting)
   - **Rate Limiting**: Prevents overloading the target websites by controlling the rate of requests sent.
   - **Queue Management**: Uses queues to manage requests and ensure an even distribution of requests across the websites.
   - **Automatic Retries**: Implements retry logic for failed requests (e.g., for HTTP 429, 500 errors).
   
### 2. Multi-Domain Support
   - The crawler can collect data from multiple websites, even if they have different **HTML structures**.
   - Each website can be customized with its own **XPath** or **CSS selectors** for scraping specific elements.
   - **Separate rules** for different domains allow flexible configurations.

### 3. Data Storage
   - Stores scraped data in a **MySQL database**.
   - Automatically checks for **duplicate products** and updates the records with the latest information (e.g., price, description, etc.).
   - Database schema designed for fast queries and scalability.

### 4. Error Management
   - **HTTP Error Handling**: Handles common HTTP errors (e.g., 404, 500, 429) with custom error messages.
   - Implements **retry mechanisms** for temporary issues such as rate limiting or server errors.
   - Logs errors in a structured format for easy debugging and monitoring.

### 5. Security Challenges
   - **Bypass CAPTCHA**: Implements solutions to bypass simple CAPTCHA systems using services like **Anti-Captcha** or other techniques.
   - Prevents CAPTCHA issues from blocking the crawler by automating the data acquisition process.

### 6. Proxy Usage
   - Supports **proxy rotation** to prevent IP blocking and ensure anonymity.
   - The system can switch between multiple proxies for each request, reducing the risk of IP bans.

### 7. Flexible Structure
   - The system is highly customizable through a **configuration file**.
   - The configuration file allows users to modify settings such as:
     - **Domains to crawl**
     - **XPath/CSS selectors for each domain**
     - **Retry settings**
     - **Rate limiting configuration**
   - This structure makes it easy to add new websites or modify the scraping logic.

### 8. Evaluation Criteria
   The project will be evaluated based on the following factors:
   - **Code Readability and Quality**: Well-organized, clean, and well-commented code.
   - **Adherence to SOLID Principles**: Follows SOLID principles for object-oriented design.
   - **Scalability**: Ability to scale for large amounts of data and multiple domains.
   - **Performance**: Efficient use of resources like time and memory.
   - **Professional Tools**: Utilizes professional tools like *Redis*, *Docker*, and **Scrapy** to manage concurrency and tasks.

## Websites to Crawl

- **[Shein](https://www.shein.com)**: A popular global fashion e-commerce platform.
- **[Zara](https://www.zara.com)**: An international clothing and accessories retailer.

## Installation & Setup

### Prerequisites

- **Python 3.x** or higher
- **MySQL** installed and configured
- **Scrapy** installed: `pip install scrapy`


### Clone the Repository

```bash
git clone https://github.com/your-username/advanced-web-crawler.git
cd advanced-web-crawler
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up the Database

1. Create a MySQL database for storing the product data.
2. Update your database connection details in the `settings.py` file.

### Run the Crawler

1. To run the spider for Zara:

   ```bash
   scrapy crawl zara
   ```


## Customizing the Crawler

To scrape different websites or modify the scraping logic, follow these steps:

1. Update the `settings.py` file with the new domain and URL settings.
2. Add the new **XPath** or **CSS selectors** for the elements you want to scrape.
3. Modify or extend the **spider** code to match the structure of the target website.
4. Add new rules or adjust existing ones in the **configuration file**.

## Contributing

We welcome contributions to improve and expand the functionality of the crawler. Here's how you can contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes and commit them.
4. Submit a pull request for review.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Scrapy**: A powerful and flexible web scraping framework used for crawling.
- **Redis**: Distributed task queue system used for parallel execution.
- **MySQL**: The relational database used to store the scraped data.

---

> "Data is the new oil, and this crawler is the refinery."

---

This README file contains everything you need to understand, set up, and contribute to the **Advanced Web Crawler** project. Happy crawling! 🚀


---

### Key Features of This Markdown:

1. **Sectioned Layout**: The README is broken down into logical sections such as project overview, features, installation, contributing, and more.
2. **Clear Formatting**: Proper use of headings, bullet points, and code blocks makes it easy to read and follow.
3. **Links & References**: Hyperlinks to the official websites and GitHub repository make it easy for users to find more information.
4. **Command-Line Instructions**: Clear installation and execution instructions in a terminal-friendly format.

This structure should make the repository clear and easy to understand for anyone browsing it.

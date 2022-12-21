# soldListingScraper
A simple webscraper that gathers data on sold listings for a chosen designer/category.

# What is Grailed? 🤔
As someone with a passion for fashion and the online market for high-end clothing, I have become a huge fan of Grailed - an online platform that allows individuals to buy and sell designer and sartorial clothing. While using the platform, I realized that designer pieces could be seen as speculative assets, similar to stocks or cryptocurrencies, with the potential for significant returns. To take advantage of this opportunity, I decided to use a data analysis approach for market research and eventually plan to create a machine learning model to help predict closing prices. In this post, I will focus on the first step towards that goal: using Python and Selenium to gather sold item data from Grailed through a web scraper.

As a quick disclaimer, I'm mostly a self-taught coder, so if you see any glaring issues with my code or have any suggestions feel free to reach out! I would love to hear your thoughts!

# Resources 🚗
You'll probably need all of these if you want to follow along:
- [Python](https://www.python.org/)
- [Selenium](https://www.selenium.dev/)
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (Get the drivers pertaining to your browser of choice)
- [Selenium Documentation for Python Coders](https://selenium-python.readthedocs.io/)

### Why Selenium?
Some readers with advanced technical knowledge may be wondering why I chose to use Selenium for this project. While Selenium is a powerful framework for browser automation, many people argue that more lightweight options such as BeautifulSoup or data scraping-specific options like Scrapy would be more suitable. While these are valid points, I opted for Selenium due to the fact that certain components on the Grailed.com website, like the item feed, require a full browser to load properly. While other frameworks and libraries do offer work arounds for this, I found Selenium to be the easiest solution in the short term, especially since gathering the data is only the first step in my project. 

In terms of speed, if you want to improve the run-time for a similar program, I would advise using Selenium for the navigation alongside a faster parser like BeautifulSoup to gather the data from the HTML.

# Instructions to follow along?
Read my blog post about it here: https://yood2.github.io/2022/12/12/grailed-scraper/

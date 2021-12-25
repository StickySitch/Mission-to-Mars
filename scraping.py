# Importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    exePath = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **exePath, headless=True)

    newsTitle, newsParagraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": newsTitle,
        "news_paragraph": newsParagraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit mars NASA news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    # Adding delay for loading page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    newsSoup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slideElem = newsSoup.select_one('div.list_text')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        newsTitle = slideElem.find('div',class_='content_title').get_text()


        # Use the parent element to find the paragraph text
        newsP = slideElem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return newsTitle, newsP


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)


    # Find and click the full image button
    fullImageElem = browser.find_by_tag('button')[1]
    fullImageElem.click()


    # Parse the resulting html with soup
    html = browser.html
    imgSoup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        imgUrlRel = imgSoup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URl to create an absolute URL
    imgURL = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{imgUrlRel}'


    return imgURL


def mars_facts():
    try:
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
        return None

    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html(classes='table table-striped')


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



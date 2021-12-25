# Importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Set up Splinter
exePath = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **exePath, headless=False)

def mars_news(browser):

    # Visit mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Adding delay for loading page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    newsSoup = soup(html, 'html.parser'

    # Add try/except for error handling
    try:
        slideElem = newsSoup.select_one('div.list_text')
        #slideElem.find('div',class_='content_title')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        newsTitle = slideElem.find('div',class_='content_title').get_text()
        #newsTitle


        # Use the parent element to find the paragraph text
        newsP = slideElem.find('div', class_='article_teaser_body').get_text()
        #newsP
    except AttributeError:
        return None,None
    return newsTitle, newsP

# Jet Propulsion Lab
exePath = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **exePath, headless=False)
def featured_image(browser):
    # Visit URL
    url  = 'https://spaceimages-mars.com/'
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
    imgURL = f'https://spaceimages-mars.com/{imgUrlRel}'


    return imgURL


def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    return df.to_html()
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html()
    #browser.quit()






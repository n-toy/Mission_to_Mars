# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager ## Ran into many issues trying to run ChromeDriver. This StackOverflow answer provides clarity on this library: https://stackoverflow.com/a/52878725
import datetime as dt

def scrape_all():
    #initiate headless driver for deployment
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path,headless = True)
    news_title, news_paragraph = mars_news(browser)
    hemi1, hemi2, hemi3, hemi4 = mars_hemispheres(browser)
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemisphere1": hemi1,
      "hemisphere2": hemi2,
      "hemisphere3": hemi3,
      "hemisphere4": hemi4,
      "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ## JPL Space Images Featured Image


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None
    
    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url
 
# ## Mars Facts
def mars_facts():
    try:
        df = pd.read_html('https://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap

    return df.to_html(classes = "table table-striped")




# Obtain high-res images fo the hemispheres. 
# Capture both image URL string and hemisphere title
# Use Python dictionary to store the data using the keys 'img_url' and 'title'
# Append the dictionary with the image URL string and the hemisphere title to a list. This list will contain on dictionary for each hemisphere

### Mars Hemispheres
def mars_hemispheres(browser):
    #Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #Beautiful Soup to read in html
    html = browser.html
    hemi_soup = soup(html,'html.parser')
    #Build links for 4 hemisphere webpages we need to visit
    images = hemi_soup.find("div",class_ = 'collapsible results')
    link_images = images.find_all("a",class_ = 'itemLink product-item')
    
    #Empty list to hold our hemisphere name, url to click, and then picture url to use
    img_location = []
    #Iterate through the 4 images found
    for link in link_images:
        #If there is a name associated with the html tag, then capture it!
        href_link = link['href']
        if len(link.get_text())>1:
            img_location.append({'name':link.get_text(),'url':f'https://astrogeology.usgs.gov/{href_link}'})

    #Fort he 4 pics, access the URL of each. And then grab the href pointing to the high res photo of each hemi
    for i in range(0,len(img_location)):
        #Visit the URL pages
        browser.visit(img_location[i]['url'])
        #Read into Beautiful Soup and parse
        html = browser.html
        img_soup = soup(html, 'html.parser')
        #Find the container for the picture button, and grab the HREF
        linky_link = img_soup.find('div',class_ = 'downloads').find('a')['href']
        img_location[i]['pic_url'] = linky_link
    return img_location[0]['pic_url'],img_location[1]['pic_url'],img_location[2]['pic_url'],img_location[3]['pic_url']


if __name__ == "__main__":
    #If running as script, print scraped data
    print(scrape_all())
 
# Mission_to_Mars

## Resources
  Software: Python 3.7.3, Jupyter Notebooks
  Libraries: MongoDB, Pandas, Flask, Splinter, BeautifulSoup
  
## Project Overview
  Develop a web application that scrapes data from NASA webpages, and displays the data using Flask. The Website https://mars.nasa.gov/news/ is scraped by using Splinter to control an instance of Google Chrome using ChromeDriver. The library BeautifulSoup was used to parse through the HTML of the website to pull in NASA article data. 
  
  Along with NASA article data images were scraped and pulled from https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars. In the same method of using Splinter, and BeautifulSoup the direct links to high resolution photos is parsed and captured. Mars facts are captured from https://space-facts.com/mars/ and captured in its HTML format. 
  
  Finally, high resolution photos of the 4 hemispheres of Mars are parsed and captured as well. The source of these photos is https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars . All of the above data points are captured, and inserted into a NoSQL (Mongo) database to be held. All collected information is later called during a Flask App to be displayed. The Flask App also has the functionality to scrape data again from the above data sources.

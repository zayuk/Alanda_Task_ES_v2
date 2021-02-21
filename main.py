import pandas as pd
import sys
import warnings
# Importing requests doesn't work quite well since it gets blocked by Cloudflare, saved error message to show later
# If one scrapes autotrader the wrong way the IP may get blocked nonetheless it seems
# This simple script is able to scrape over 1400 listings without proxies
# I read online that the limit is ~1200 per IP. This is either no longer true or people scraped it in a different way
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Suppressing the pandas future regex warning
warnings.simplefilter(action='ignore', category=FutureWarning)

# I use sys.argv to pass search arguments through the terminal. Arguments are brand, postcode, radius, pages to scrape.
brands = sys.argv[1:]
postcode = sys.argv[2]
radius = sys.argv[3]
pages = int(sys.argv[4])
print("Searching for:")
print("Brand:", sys.argv[1])
print("Postcode:", sys.argv[2])
print("Radius:", sys.argv[3])
print("# Pages:", sys.argv[4])

# Initialize all lists for the table
brand_search = []
titles = []
ad_links = []
subtitles = []
prices = []
seller_ratings = []
specs = []

# First loop input decides how many pages we scrape, second goes through the brands we want to search by
# Initially I didn't use sys.argv and hardcoded car brands so the script is able to search for multiple brands
# on a single run. I later realized this is not very necessary so I implemented the sys.args to take 1 brand at a time
for page in range(1, pages):
    print("Scraping page #", page)
    for brand in brands:
        # I used Python 3.6+'s f strings here to pass some expressions in the search link.
        req_url = f"https://www.autotrader.co.uk/car-search?sort=distance&" \
                  f"postcode={postcode}&radius={radius}&onesearchad=Used&onesearchad=Nearly%20New&" \
                  f"onesearchad=New&make={brand}&page={page}"
        req = urlopen(req_url)
        page_html = req.read()
        req.close()
        page_soup = BeautifulSoup(page_html, "html.parser")
        listings = page_soup.find_all("li", {"class": "search-page__result"})
        for listing in listings:
            ad_link_container = listing.find("article", {"class": "product-card"})
            information_container = listing.find("div", {"class": "product-card-content"})
            # add searched brand to the list
            brand_search.append(brand)
            # add the title to the list
            title = information_container.find("h3", {
                "class": "product-card-details__title"})
            if title:
                titles.append(title.text)
            else:
                titles.append("N/A")

            # add link to the list
            ad_link = ad_link_container.find("a", {
                "class": "js-click-handler listing-fpa-link tracking-standard-link"}).attrs['href']
            if ad_link:
                ad_links.append(ad_link)
            else:
                ad_links.append("N/A")

            # add subtitle to the list
            subtitle = information_container.find("p", {"class": "product-card-details__attention-grabber"})
            if subtitle:
                subtitles.append(subtitle.text)
            else:
                subtitles.append("N/A")

            # add price to the list
            price = information_container.find("div", {"class": "product-card-pricing__price"})
            if price:
                prices.append(price.text)
            else:
                prices.append("N/A")

            # add seller rating to the list
            seller_rating = information_container.find("p", {"class": "product-card-seller__rating-number"})
            if seller_rating:
                seller_ratings.append(seller_rating.text)
            else:
                seller_ratings.append("N/A")

            spec = listing.find("ul", {"class": "listing-key-specs"})
            if spec:
                specs.append(spec.text)
            else:
                specs.append("N/A")

        # This looks at the page numbers on the bottom of the page, -2 since one is the arrow
        pagination = page_soup.find_all('li', {'class': 'pagination--li'})[-2]
        # Comparing it then with the page number to make sure it stops before crashing the script
        if int(pagination.text) <= page:
            brands.remove(brand)

print("Creating pandas data frame...")
# Create pandas data frame
pandas_table = pd.DataFrame(
    {'Searched brand': brand_search,
     'Title': titles,
     'Ad link': ad_links,
     'Subtitle': subtitles,
     'Price': prices,
     'Seller rating': seller_ratings,
     'Details': specs})
print("Formatting pandas table...")
# Clean up data to remove space, /n and so on
# to_json adds "\" characters because it apparently tries to circumvent other issues. So the extra \ should be correct
# replacing £ with GBP, as well as other weird characters since they causes encoding issues with to_json
# it seems stringing together .replace statements is faster than other methods •
pandas_table['Title'] = pandas_table['Title'].str.strip().str.replace(r'•', ', ').str.replace(r'£', 'GBP ')
pandas_table['Ad link'] = 'https//autotrader.co.uk' + pandas_table['Ad link']
pandas_table['Subtitle'] = pandas_table['Subtitle'].str.strip().str.replace(r'•', ', ').str.replace(r'£', 'GBP ')
pandas_table['Price'] = pandas_table['Price'].str.strip().str.replace(r'•', ', ').str.replace(r'£', 'GBP ')
pandas_table['Seller rating'] = pandas_table['Seller rating'].str.strip()
# These specification details are given as list which can sometimes have all or some entries.
# Decided to put them into one column since it can be inferred to what they refer, especially after visiting the site.
pandas_table['Details'] = pandas_table['Details'].str.strip().str.replace(r'\n', ', ')

# Create the json output in a file called output.json
print("Outputting to JSON...")
pandas_table.to_json('output.json', orient='index')
print("Done!")

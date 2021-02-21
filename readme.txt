Alanda Scraping Task
by Edward Sutulov
Scraping target: www.autotrader.co.uk
Method: HTML scraping
Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 16:33:24) [MSC v.1928 32 bit (Intel)] on win32

     /\        | |      | |               | |            / ____|
    /  \  _   _| |_ ___ | |_ _ __ __ _  __| | ___ _ __  | (___   ___ _ __ __ _ _ __   ___ _ __
   / /\ \| | | | __/ _ \| __| '__/ _` |/ _` |/ _ \ '__|  \___ \ / __| '__/ _` | '_ \ / _ \ '__|
  / ____ \ |_| | || (_) | |_| | | (_| | (_| |  __/ |     ____) | (__| | | (_| | |_) |  __/ |
 /_/    \_\__,_|\__\___/ \__|_|  \__,_|\__,_|\___|_|    |_____/ \___|_|  \__,_| .__/ \___|_|
                                                                              | |

To code this I've used PyCharm as an IDE and a virtual environment.
I decided to go for HTML scraping since I have some experience with BeautifulSoup and feedparser from my previous
scraper at Sinclair Capital.
I check all 5 websites’ robots.txt to determine which one blocks what for scraping purposes.
I decide to go with autotrader.co.uk since it seems a bit more difficult than others since most other
websites don’t block any queries. I do that to compensate for the easier HTML scraping.
Plus, I like cars and got curious about the prices.
Indeed autotrader blocked my scraper initially when using requests.get.
I used the less common urllib to do my queries which worked quite well.
Please check the comments within main.py to understand some of my methodology.
I've exported my entire virtual environment plus code as well as requirements.txt on Git so that everything is there.
The JSON file on GitHub should contain my last scrape which got 1286 results searching for Audi cars
in 1500 mile radius of SW1P4JX. This is a total of 100 pages of autotrader search results.
Each entry contains the searched brand, title of the ad, link to the ad, subtitle, price, seller rating and
details which outline specifications like date of registration, chasis type, mileage, engine liters,
engine power, transmission type, fuel type, owner history, and emission compliance type.
I bundled the details entry into one since each add can contain all or a subset of the aforementioned details.

There might be bugs and/or exceptions thrown especially if the script is not launched properly so please see this:

**Usage**:
The script takes several arguments to execute:
brand: Car manufacturer e.g BMW, Audi
postcode: What postcode it should search for
radius: what miles radius within that postcode
#pages: how many pages do you wish to scrape

After it is finished running there should be an output file called output.json.
There might be characters such as this: \ at first glance but that is apparently correct json output behaviour and
any json parser should easily see those and remove them as needed.
The export is a continuous line of code which can be easily seen properly when input into a formatter such as:
https://jsonformatter.curiousconcept.com/

**So an example run via the terminal would be**:

main.py Audi SW1P4JX 1500 3

This will scrape for 2-3 pages of Audi cars within a 1500 mile radius of SW1P4JX postcode.

If the car manufacturer has two names e.g Aston Martin, the correct syntax would be to use a +:

main.py Aston+Martin SW1P4JX 1500 3


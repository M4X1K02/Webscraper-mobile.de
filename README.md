# Webscraper-mobile.de
This webscraper scrapes certain listings on the german mobile.de website. It only "works" with the Surfshark VPN extension.

### Disclaimer
**This scraper was tested a year ago and did not really work, since the anti-bot detection on the mobile.de website is on another level.
I am by no means a Software Engineer or a professional programmer, this project just so happened for learning purposes and out of curiosity in my free time.**


Although I did manage to scrape some listings, which you can find in the SQLite DB.
It uses Selenium for scraping combined with an automation of the Surfshark extension to stay undetected, which was probably part of the problem, since they just outright ban IPs coming from VPN providers much more easily, or put captchas infront of them.
To increase the chance of not being spotted as a bot, completely new sessions with a new IP and Header were used.

* You can filter your searches by model and manufacturer here: modelConfig.py
* Specific search filters can be adjusted here: filterConfig.py (reduces uninteresting results and scraping time)

Feel free to copy some useful parts (maybe the searchFilter?) and create your own scraper, if you feel up to the challenge of getting past the heavy mobile.de bot-detection.


Possible improvements:
* Use a dedicated proxy service with residential proxies from Germany. This should increase your chances of not being detected by a lot.
* Try to scrape much much slower (if using one IP/Session). Something close to what a human would do (~minute per site?).
* Do not delete cookies during a session.


### Legal disclaimer

I have not harmed the integrity of the mobile.de website, nor have I copied a substantial amount of its database.
Also, the scraped data is not off-limits to regular people searching the web, and it does not contain any sensitive information.

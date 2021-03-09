# craigslist-scraper

## Adding filters
* Filters can be added to the application as comma separated json in ```filters.json``` file. 
Each json in the list will be considered as separate filer set and the scraping will be performed.

## Updating the look back window
* Current look-back window is set to 7 days. It will get all the posts older than 7 days. If this 
want to be changed update the ```look_back_days``` parameter in the ```config.ini``` file.
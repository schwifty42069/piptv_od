Piptv On Demand (pod) Module Basic Documentation 
====================
***


*class* - pod.ImdbQuery(self, search, media_type) -> **ImdbQuery Object**
        
>Simple IMDB query class for scraping title names, title codes and series/season/episode data

*parameters* 

| Name  | Type | Description |
| ------------- | ------------- | ------------- |
| search  | str  | search words for query |
| media_type  | str  | Type of media ("tv" or "movie") |

*method* - pod.ImdbQuery.format_search_words(self) -> **Returns:** *formatted_words*, **Type:** *str*,  **Desc:** *url formatted search words*

>Method run at instantiation of class, formats search terms for URL                         
   
*method* - pod.ImdbQuery.scrape_title_codes(self) -> **void** 

>Method used to scrape the title codes of titles retrieved from 
 query, **updates title_codes attribute of class**

*method* - pod.ImdbQuery.scrape_media_titles(self) -> **void**

>Method used to scrape title names of titles retrieved from query,
 **updates titles attribute of class**

*staticmethod* - pod.ImdbQuery.get_series_season(title_code) -> **Returns:** *num*, **Type:** *int*, **Desc:** *number of seasons for a given series*

>Requires "tv" media_type, retrieves number of seasons for
 a given title_code

*staticmethod* - pod.ImdbQuery.get_season_episodes(title_code, season) -> **Returns:** *num*, **Type:** *int*, **Desc:** *number of episodes for a given season*

>Retrieves number of episodes for a given title_code and season
    
*parameters*
    
| Name  | Type | Description |
| ------------- | ------------- | ------------- |
| search  | str  | search words for query |
| media_type  | str  | Type of media ("tv" or "movie") |
               
*staticmethod* - pod.ImdbQuery.scrape_episode_titles(title_code, season) -> **Returns:** *titles*, **Type:** *list*, **Desc:** *list of episode titles for given season*

>Retrieves list of episode titles for a given season

*parameters*

| Name  | Type | Description |
| ------------- | ------------- | ------------- |
| search  | str  | search words for query |
| media_type  | str  | Type of media ("tv" or "movie") |

**Usage example**

```
from pod import ImdbQuery
from pprint import pprint

# create ImdbQuery object (pass media title and media_type)
imdb_query = ImdbQuery("Its Always Sunny in Philadelphia", "tv")

# scrape title codes
imdb_query.scrape_title_codes()

# scrape media title names
imdb_query.scrape_media_titles()

# print scraped title names
print("\nMedia titles:\n")
pprint(imdb_query.titles)

# print corresponding title codes
print("\nTitle codes:\n")
pprint(imdb_query.title_codes)

[Out] >>>

Media titles:

["1. It's Always Sunny in Philadelphia (2005) (TV Series) ",
 "2. It's Always Sunny in Philadelphia (2013) (TV Episode) ",
 "3. It's Always Sunny in Philadelphia (2015) (TV Episode) ",
 "4. It's Always Sunny in Philadelphia (2006) (TV Episode) ",
 "5. It's Always Sunny in Philadelphia: Sunny Side Up (2008) (Video) ",
 "6. It's Always Sunny in Philadelphia Season 3: Sunny Side Up (2008) (Video) ",
 "7. It's Not Always Funny in Philadelphia (2016) (TV Episode) ",
 "8. It's Always Sunny in Philadelphia Season 4 (TV Episode) ",
 "9. It's Always Sunny in Philadelphia Season 3 (TV Episode) ",
 '10. Charlie Day talks "It\'s Always Sunny in Philadelphia" (2015) (TV '
 'Episode) ']

Title codes:

['tt0472954',
 'tt3743426',
 'tt4413268',
 'tt1015034',
 'tt1422672',
 'tt1422671',
 'tt5363326',
 'tt1670879',
 'tt1670878',
 'tt7709208']
````


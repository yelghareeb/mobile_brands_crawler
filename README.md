# 1. Introduction

I made this small project to crawl the mobile brands from [Mobile Shop](http://mobileshop.com.eg/en), and send me incremental updates on email for the following events
  - A new mobile phone added to the website
  - A new mobile phone deleted from the website
  - A change in the price of a mobile phone

# 2. Components

## 2.1. Scrapper
This is the entry point of the application. The scrapper is responsible of fetching all the phone models that exist on the website at the time of running the script, and building the **knowledge_base**, then storing the knowledge base on disk.
I used the **BeautifulSoup** parser library to parse the HTML, and the **Pickle** package to serialize the knowledge_base to disk, to serve as the old knowledge base for the next run.
## 2.2. Comparator
This class is used to extract information from the new and old knowledge bases. This class contains 3 methods.
  - get_new_phones
  - get_removed_phones
  - get_updated_phones

## 2.3. Reporter
This class is used to send email reports to my email address with the information extracted from steps 1 & 2.

# Usage
To use this app, modify the "*send_mail.py*" and include your Gmail & password, then run the startup.bat file.

```sh
$ startup.bat
```

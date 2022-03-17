### AWS Lambda Scraper
* **Summary**
    
    A simple tool that periodically downloads subscriber-only content to S3 for future references. Currently, the
    content platform does not allow user to browse past contents, hence the creation of the tool
    
* **Folder Structure**

    root/ \
    |-packages/ <- dependencies \
    |-scraper.py <- main function(s) \
    |-others/ <- not required by lambda 
    
* **Some Notes**

    * Credential Management \
    Instead of storing the `username` and `password` as (plain) text, we can supply such information by event
    trigger which is configured outside of the function. This setup also helps when the user would like to update the
    password without having to modify the code
    
    * Stock Market Open Dates \
    TBD - needs to find a reliable source for calendar
    
    * S3 Data Storage \
    TBD - currently the free tier has 5GB available for the first 12 months
    
    * Email/SMTP \
    TBD - I used to program such function in Matlab. I see Python has package to handle similar tasks
    
    * Scraping Interval
    It makes sense to apply random delays between 0ms and 10ms so the IP address won't be blacklisted
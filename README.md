# javaScrape
Web page script scraper + parser

---------------------------------

java[Scrape]s a given URL for <script> tags, and returns a list of three categories:
  * Locally-hosted scripts
  * Externally-hosted scripts
  * Internal page scripts
  
Then iterates through each [currently just local] script for matches against a list of patterns.
  - This list is easily modified at the bottom head of the script.
  - Next feature goal includes pattern sub-groups, such as 'IP addresses' > private and localhost IP references
    ~ Another list will target possible credentials, and one list may include a variety of dangerous code patterns.
    ~ These lists will correspond to an argparse switch so they may be individually disabled.
  
Upcoming change :
  > Take input args or file to receive custom patterns.
  
---------------------------------
Setup:

pip install -r requirements.txt


Usage:
 
./jScrape -u https://www.iana.org/domains/reserved

 
 
 
Example Output:
 
![screen](https://user-images.githubusercontent.com/85598459/121372915-a3cf6280-c90c-11eb-9272-ea45c4456681.png)


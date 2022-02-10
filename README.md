# Near real-time scraping from Strava.com using Selenium and Kafka

**Part of Data Management project | UniMiB**

The porpose of the project is to create a collection of Strava activites and make them availble according to user's sport preference through Kafka (possible topics are: Running, Cycling, Water sports and Other).

**Note:** to avoid the Too Many Requests status code, there's random time sleep after the scraping of each activity. It avoids the error but increases the time needed for each ID; to keep scraping in real time is possible to change the difference between IDs from 1 to 100, like in *scraping_producer.py.*

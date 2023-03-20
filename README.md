# Near real-time scraping from Strava.com using Selenium and Kafka

***Part of the Data Management project | UniMiB***

The purpose of the project is to create a collection of Strava activities and make them available according to user's sport preference through Kafka (possible topics are: Running, Cycling, Water sports and Other).

![Copy of Add a subheading_page-0001 (2)](https://user-images.githubusercontent.com/63108350/153359094-8f23d7ed-c2b3-4c4d-bc74-682c3a85fb36.jpg)


**Note:** to avoid the Too Many Requests status code, there's random time sleep after the scraping of each activity. It avoids the error, but increases the time needed for each ID; to keep scraping in real-time it is possible to change the difference between IDs from 1 to 100, like in *scraping_producer.py.*


[![Big picture of the project](https://github.com/Aziz4785/stylist.ai/blob/master/bigpicture.jpg)](https://github.com/Aziz4785/stylist.ai/blob/master/bigpicture.jpg)

link to edit the image : https://drive.google.com/file/d/1DSfWRgtU-0kk6xvRn2hk7EyXIFcfVX89/view?usp=sharing

## Configuration of the server
Before running the server, you need to create a config_server.py file in the SERVER directory of the project
```bash

# Create a config_server.py file with this content
OPENAI_API_KEY = 'your-api-key'
db_uri = "mongodb://mongodb:27017/"
db_name = "mydatabase"

```
## Run the server
```bash
# at project root:

docker-compose up server # add --build after "up" If you're running it for the first time or after modifying the server code
#and wait ...
```
## Run the tests on server
```bash
# at project root:

docker-compose up test # add --build after "up" If you're running it for the first time or after modifying the test
#and wait ...
```

## Configuration of zalando scraper
Before running the scraper, you need to create a config.py file in the ZALANDO_SCRAPER directory of the project.
```bash

# Create a config.py file with this content
OPENAI_API_KEY = 'your-api-key'
db_uri = "mongodb://localhost:27017/"
db_name = "mydatabase"

```

## Run the zalando scraper
```bash
cd ZALANDO_SCRAPER/zalando_text_scraper
py main.py

```

## shut down containers : 
```bash
docker-compose down

```

## Import the mongodatabase (from local machine to container)
```bash
# at project root:
mongorestore --uri "mongodb://localhost:27017/" /path/to/dump_on_your_local_machine

```

## Export the mongodatabase (from container to local machine)
```bash
# at project root:

docker ps #to get ids of containers

docker exec -it <mongodb_container_id> bash #enter inside the container

mongodump --uri "mongodb://localhost:27017/" --db <db_name> --out /dump #create a dump of the "mydatabase" database and place it in the /dump directory inside the container.

exit #exit the container

docker cp <mongodb_container_name>:/dump ./dump # Copy the Dump to Your Host Machine
```
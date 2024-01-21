
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

docker-compose up # add --build If you're running it for the first time or after modifying the server code

```
## Run the tests on server
```bash
# at project root:

docker-compose run server python -m unittest tests/test_embedding_catalog1.py

```

## Configuration of zalando scraper
Before running the scraper, you need to create a config.py file in the ZALANDO_SCRAPER directory of the project.
```bash

# Create a config.py file with this content
OPENAI_API_KEY = 'your-api-key'
db_uri = "mongodb://mongodb:27017/"
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
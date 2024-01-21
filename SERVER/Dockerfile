# SERVER/Dockerfile
FROM python:3.8

WORKDIR /server

COPY . /server

RUN pip install -r requirements.txt

# Make the entrypoint script executable
RUN chmod +x /server/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/server/entrypoint.sh"]

CMD ["sh", "-c", "python wait_for_mongo.py && python server3.py"]

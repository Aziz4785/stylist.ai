FROM python:3.8

WORKDIR /server

COPY . /server

RUN pip install -r requirements.txt

#download NLTK data during the build : 
RUN python -m nltk.downloader punkt

EXPOSE 5000

# Set a default command, for example, starting the server.
#for development
CMD ["python", "main.py"] 

# for production : Use Gunicorn to serve the Flask app. Adjust the number of workers and threads as necessary.
#CMD ["gunicorn", "-w","4","-b", "0.0.0.0:5000", "server3:app","--timeout", "120"]
#-b 0.0.0.0:5000 tells Gunicorn to bind to port 5000 on all network interfaces.
#-w 4 specifies the number of worker processes. This number should be adjusted based on your server's CPU cores and the load you expect

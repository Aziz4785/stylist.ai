from server3 import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #for developmenet , tells Flask to listen on all network interfaces within the container, making it accessible through the Docker host
    #app.run() #for production
from rdio_collabo import app, rdioOAuth

if __name__ == '__main__':
    rdioOAuth.BuildConsumerAndClient(app.config["CONSUMER_KEY"], app.config["CONSUMER_SECRET"])
    app.run(debug=True)

from rdio_collabo import app, rdioOAuthManager

if __name__ == '__main__':
    rdioOAuthManager.BuildConsumerAndClient(app.config["CONSUMER_KEY"], app.config["CONSUMER_SECRET"])
    app.run(debug=True)

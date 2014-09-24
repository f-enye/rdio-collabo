from rdio_collabo import app

import webservice

if __name__ == '__main__':
    webservice.authenticate(app.config["CONSUMER_KEY"], app.config["CONSUMER_SECRET"])
    app.run(debug=True)

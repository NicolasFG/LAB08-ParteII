from flask import Flask
from flask import jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, time, timedelta


app = Flask(__name__)


limiter = Limiter(key_func=get_remote_address, app=app)

@app.route('/rate-limit-me')
@limiter.limit("600/minute")
def rateLimit():
    return jsonify(Result="Rate-Limit-Success"), 200

@app.route('/throttle-me')
def throttle():
    return jsonify(Result="Throttle-Limit-Success"), 200

@app.errorhandler(429)
def resource_not_found(e):
    key = get_remote_address()
    limiter.storage.clear(key=key)
    return jsonify(error=str(key)), 429

if __name__ == "__main__":
    app.run(debug=True, port=7000)

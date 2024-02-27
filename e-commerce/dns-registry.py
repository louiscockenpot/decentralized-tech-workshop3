from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/getServer')
def get_server():
    return jsonify(code=200, server="localhost:3001")

if __name__ == '__main__':
    app.run(debug=True, port=3002)

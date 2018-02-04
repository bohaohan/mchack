import json

__author__ = 'bohaohan'
from flask import Flask
from flask import request
from testExtAndSum import *
from CxExtractor import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World! '


@app.route('/get_sum', methods=['POST'])
def extract():
    url = request.form['url']
    print url
    sum_, title = testExtAndSum(url)
    result = {
        "url": url,
        "summary": sum_,
        "title": title

    }
    return json.dumps(result)


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=2333)

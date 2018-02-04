import json

__author__ = 'bohaohan'
from flask import Flask
from flask import request
from testExtAndSum import *


app = Flask(__name__, static_url_path='')

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


@app.route('/get_sum', methods=['POST'])
def extract():
    url = request.form['url']
    print url
    sum_, title, kws = testExtAndSum(url)
    result = {
        "url": url,
        "summary": sum_,
        "title": title,
        "keyword": kws

    }
    return json.dumps(result)


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=23334)


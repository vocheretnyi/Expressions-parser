from flask import Flask, render_template, request, jsonify, Response
from function import Function
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calc', methods=['POST'])
def calc():
    try:
        data = json.loads(request.form['data'])
        func = Function(data['f'])
        res = func.calc(float(data['x']))
        tokens = '   '.join(list(map(str, func.tokens)))
        start = data['tab']['from']
        finish = data['tab']['to']
        delta = data['tab']['step']
        xs = []
        while start < finish:
            xs.append(start)
            start += delta
        ys = []
        for i in xs:
            ys.append(func.calc(i))
        return jsonify(result=res, tokens=tokens, tab=list(zip(xs, ys)))
    except BaseException as e:
        return Response(status=400, response=str(e))


if __name__ == '__main__':
    app.run()

from flask import Flask, request

app = Flask(__name__)

def readcsv():
    file = "weather.csv"
    with open(file) as fh:
        headers = tuple(fh.readline().strip().split(","))
        data = [
            dict(zip(headers, _.strip().split(",")))
            for _ in fh.readlines()
        ]
    return data

def filter_by_field(data, field, value):
    return filter(
        lambda _: _[field] == value,
        data
    )

@app.route('/query', methods=['GET'])
def weather():
    data = readcsv()
    limit = int(request.args.get('limit') or len(data))
    for field, value in request.args.items():
        if field == 'limit':
            continue
        data = filter_by_field(data, field, value)

    return dict(
        data=list(data)[:limit]
    )

if __name__ == "__main__":
    app.run()

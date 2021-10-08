from flask import Flask, render_template, request
from Report import report


results = report.build_report('./data')

drivers_names = list()
with open("./abbreviations.txt", 'r') as f:
    for line in f.read().split('\n'):
        temp = {'abbr': line[:3], 'fullname': line[4:].split('_')[0]}
        drivers_names.append(temp)


app = Flask(__name__)

@app.route("/report")
def report():
    return render_template('report.html', results=results)


@app.route("/report/drivers/",  methods=['GET'])
def drivers_first():
    driver_id = request.args.get('driver_id')
    order = request.args.get('order')
    if driver_id:
        for driver in drivers_names:
            if driver['abbr'] == driver_id:
                for r in results:
                    if driver['fullname'] == r.name:
                        return f'{r.name} | {r.team} | {str(r.result)}'
        return 'Driver_id is not correct. Please, try again', 404
    elif order == 'desc':
        return render_template('report.html', results=results[::-1], order=order)
    return render_template('drivers.html', drivers=drivers_names)


if __name__ == "__main__":
    app.run(debug=True)


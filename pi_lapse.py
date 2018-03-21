# run with:
# source venv/bin/activate
# export FLASK_APP=pi_lapse.py
# flask run -h '192.168.10.1'
# result will be at:
# http://192.168.10.1:5000/
from flask import Flask, render_template, flash, request, Markup
from wtforms import Form, validators, IntegerField, FloatField, TextField
from datetime import datetime, timedelta
import timelapse
import time

# App config
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d411f2b6176a'

class ReusableForm(Form):
    bulb = FloatField('bulb', validators=[validators.required()])
    interval = IntegerField('interval', validators=[validators.required()])
    number = IntegerField('number', validators=[validators.optional()])

@app.route("/", methods=['GET', 'POST'])
def index():

    form = ReusableForm(request.form)

    # create default values for first landing on page

    if request.method == 'POST':

        # initial form value hecks
        if form.validate():
            bulb = int(request.form['bulb'])
            interval = int(request.form['interval'])
            number = int(request.form['number'])
            print bulb, interval, number
            # results = test_timer(bulb, interval, number)
            message = "Calculated."
            print message
            timelapse_obj = timelapse.Timelapse(bulb, interval, number)
            # timelapse.start_time = time.time()
            timelapse_obj.start()
        else:
            print form.errors
            message = "Error"
        flash(message)

    return render_template('index.html', form=form)

# if __name__ == "__main__":
#     app.run()

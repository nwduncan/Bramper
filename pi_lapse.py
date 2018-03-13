# run with:
# export FLASK_APP=website.py
# flask run -h '192.168.10.1'
# result will be at:
# http://192.168.10.1:5000/
from flask import Flask, render_template, flash, request, Markup
from wtforms import Form, validators, IntegerField, FloatField, TextField
from datetime import datetime, timedelta
import timelapse
import time
import Adafruit_CharLCD as LCD

# App config
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
# app.config['SECRET_KEY'] = '7d441f27d441f27567d411f2b6176a'

# wiring variables
LCD_RS = 25
LCD_EN = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 18
LCD_D7 = 22

# lcd variables
LCD_BL = 4
LCD_COL = 16
LCD_ROWS = 2

lcd = LCD.Adafruit_CharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_COL, LCD_ROWS, LCD_BL)

class ReusableForm(Form):
    bulb = FloatField('bulb', validators=[validators.required()])
    interval = IntegerField('interval', validators=[validators.required()])
    number = IntegerField('number', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def index():

    form = ReusableForm(request.form)

    # create default values for first landing on page

    if request.method == 'POST':

        # initial form value hecks
        if form.validate():
            bulb = request.form['bulb']
            interval = request.form['interval']
            number = request.form['number']
            print bulb, interval, number
            # results = test_timer(bulb, interval, number)
            message = "Calculated."
            print message
            # timelapse = timelapse.Timelapse(lcd, 5, 10, 10)
            # timelapse.start_time = time.time()
            # timelapse.start()
        else:
            print form.errors
            message = "Error"
        flash(message)

    return render_template('index.html', form=form)

# if __name__ == "__main__":
#     app.run()

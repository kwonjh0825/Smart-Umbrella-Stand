from tkinter import image_names
import RPi.GPIO as GPIO
import spidev, time
from flask import Flask, redirect, url_for, render_template, request
from liq_level import analog_read

liq_level = 0
lev_high = int()
lev_mid = int()
lev_low = int()


# spi = spidev.SpiDev()
# spi.open(0,0)

# def analog_read(channel):
#     r = spi.xfer2([1, (8 + channel) << 4, 0])
#     adc_out = ((r[1]&3) << 8) + r[2]
#     return adc_out

# while True:
#     reading = analog_read(0)
#     voltage = reading * 3.3 / 1024
#     print("Reading=%d\tVoltage=%f" % (reading, voltage))
#     time.sleep(1)


app = Flask(__name__)

@app.route('/water', methods = ['GET', 'POST'])
def water():
    if request.method == 'GET':
        liq_level = analog_read(0)
        if liq_level >= lev_high:
            # liquid level danger
            return render_template('liquid_level.html', image_file = 'level_danger.gif')
        elif liq_level >= lev_mid:
            # liquid level higt
            return render_template('liquid_level.html', image_file = 'level_high.gif')
        elif liq_level >= lev_low:
            # liquid level middle
            return render_template('liquid_level.html', image_file = 'level_middle.gif')
        else:
            # liquid level low
            return render_template('liquid_level.html', image_file = 'level_low.gif')

    
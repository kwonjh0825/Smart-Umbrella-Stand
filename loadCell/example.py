# import sys
import time
def loadCell(pin1, pin2):
    # EMULATE_HX711=False

    referenceUnit = 246

    # print('hello')

    # if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
    # else:
    #     from emulated_hx711 import HX711

    # def cleanAndExit():
    #     print("Cleaning...")

    #     if not EMULATE_HX711:
    #         GPIO.cleanup()
            
    #     print("Bye!")
    #     sys.exit()

    hx = HX711(pin1, pin2) # Pyhsical pin => 15, 13

    hx.set_reading_format("MSB", "MSB")

    hx.set_reference_unit(referenceUnit)

    hx.reset()

    hx.tare()

    # print("Tare done! Add weight now...")
    while(1):
        val = hx.get_weight(5)
    
        print(int(val))

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
        
loadCell(12, 25)

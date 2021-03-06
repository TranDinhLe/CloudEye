def on_received_string(receivedString):
    serial.write_string(receivedString)
radio.on_received_string(on_received_string)

def on_data_received():
    global cmd
    cmd = serial.read_until(serial.delimiters(Delimiters.HASH))
    radio.send_number(parse_float(cmd))
    if parse_float(cmd) == 2:
        basic.show_number(0)
    elif parse_float(cmd) == 3:
        basic.show_leds("""
            # . . . #
                        . # . # .
                        . . # . .
                        . # . # .
                        # . . . #
        """)
serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)

cmd = ""
radio.set_group(1)

def on_forever():
    pass
basic.forever(on_forever)

import nxt
import nxt.locator

# ENDERECO MAC DO NXT 01 (COM DISPLAY BOM E EMITINDO SONS MANEIROS)
NXT_MAC_ADDRESS = "00:16:53:09:81:69"

with nxt.locator.find() as b:
    # Get the motor connected to the port A.
    mymotor = b.get_motor(nxt.motor.Port.A)
    # Full circle in one direction.
    mymotor.turn(25, 360)
    # Full circle in the opposite direction.
    mymotor.turn(-25, 360)
    print(b.get_device_info())
    print(b.get_firmware_version())
    b.play_sound_file(False, "avemaria.mp3")
    print(b.get_battery_level())
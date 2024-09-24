import nxt
import nxt.locator
import nxt.backend.bluetooth as bluetooth
import nxt.brick

# ENDERECO MAC DO NXT 01 (COM DISPLAY BOM E EMITINDO SONS MANEIROS)
NXT_MAC_ADDRESS = "00:16:53:09:81:69"
MESSAGE = b'OI BLUETOOTH :)'

nxt_brick = nxt.locator.find(host=NXT_MAC_ADDRESS)
# Get the motor connected to the port A.
mymotor = nxt_brick.get_motor(nxt.motor.Port.A)
# Full circle in one direction.
mymotor.turn(25, 360)
# Full circle in the opposite direction.
mymotor.turn(-25, 360)
#nxt_brick.message_write(inbox=1, message=MESSAGE)
#message = nxt_brick.message_read(1, True)
#print(f'MENSAGEM LIDA DO MAILBOX 1 DO NXT {message}')
print(nxt_brick.get_device_info())
print(nxt_brick.get_firmware_version())
nxt_brick.close()
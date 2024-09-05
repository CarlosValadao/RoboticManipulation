import nxt.locator
from nxt.bluesock import BlueSock

def connect_to_nxt():
    # Substitua '00:16:53:XX:XX:XX' pelo endereço Bluetooth do seu NXT Brick
    btsock = BlueSock('00:16:53:XX:XX:XX')  
    if btsock:
        nxt_brick = btsock.connect()
        print("Conectado ao NXT Brick via Bluetooth!")
        return nxt_brick
    else:
        print("Não foi possível encontrar o NXT Brick.")
        return None

nxt_brick = connect_to_nxt()

nxt_brick.sock.close()
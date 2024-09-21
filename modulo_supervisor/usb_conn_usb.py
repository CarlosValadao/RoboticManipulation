import nxt.locator

def connect_to_nxt():
    nxt_brick = nxt.locator.find_one_brick()
    if nxt_brick:
        print("Conectado ao NXT Brick via USB!")
        return nxt_brick
    else:
        print("Não foi possível encontrar o NXT Brick.")
        return None

nxt_brick = connect_to_nxt()

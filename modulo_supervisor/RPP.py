# Robotics PBL Protocol

from typing import Final

# Header message type
RESPONSE: Final = '2'
POSITION: Final = '3'


def parse_message(message: str) -> tuple[int]|int:
    message_head = message[0]
    message_tail = message[2:]
    if message_head == RESPONSE:
        response_type = int(message_tail)
        return response_type
    elif message_head == POSITION:
        (x_pos, y_pos) = message_tail.split(sep=';')
        return (int(x_pos), int(y_pos.replace('\x00', '')))

def format_message(type: int, code: int) -> str:
    return f'{type};{code}'
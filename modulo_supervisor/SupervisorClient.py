from nxt.locator import find
from nxt.brick import Brick
from constants import MAILBOX1, MAILBOX10
import RPP
from threading import Thread
from nxt.locator import BrickNotFoundError
from time import sleep

# By default use MAILBOX0 to send messages
# and MAILBOX10 do receive/read messages

# this SupervisorBluetoothClient pretend
# manage the communication between the
# supervisor and the robot
class SupervisorClient:
    def __init__(self, nxt_bluetooth_mac):
        self._is_nxt_connected: bool = False
        self._nxt_brick: Brick = self.establish_nxt_con(nxt_bluetooth_mac)
        # as soon as messages are read
        # they're stored here
        self.received_messages: list[tuple[int]|int] = []
        # it is a mutex
        self._have_new_message: bool = False
        self._there_is_running_program_on_nxt: bool = False

    def connect_to_nxt(self, nxt_bluetooth_mac: str) -> Brick|None:
        try:
            nxt_brick = find(self.nxt_bluetooth_mac)
            self._is_nxt_connected = True
            return nxt_brick
        except BrickNotFoundError:
            print("NXT está inalcançável :/")
            print("Tentando se conectar novamente")
            self._is_nxt_connected = False
            return None
    
    # force the connection with the nxt
    # ad infinitum
    def force_nxt_con(self, nxt_bluetooth_mac) -> Brick:
        while not self._is_nxt_connected:
            nxt_brick = self.connect_to_nxt(nxt_bluetooth_mac)
            sleep(0.5)
        return nxt_brick

    def establish_nxt_con(self, host: str) -> Brick:
        nxt_brick = self.connect_to_nxt(host)
        if not nxt_brick:
            nxt_brick = self.force_nxt_con(host)
        return nxt_brick

    def send_message(self, message: str) -> None:
        self._nxt_brick.message_write(MAILBOX1, message)
    
    def _read_message(self) -> tuple[int]|int:
        try:
            (inbox, received_message) = self._nxt_brick.message_read(MAILBOX10, 0, True)
            self._have_new_message = True
            return received_message
        # empty mailbox
        except:
            self._have_new_message = False
    
    def read_all_messages(self) -> None:
        hasActiveProgram = self._is_running_program_on_nxt()
        while hasActiveProgram:
            received_message = self._read_message()
            if self._have_new_message:
                data = RPP.parse_message(received_message)
                self.received_messages.append(data)
            hasActiveProgram = self._is_running_program_on_nxt()
        self.close_nxt_con()
    
    def get_all_messages(self) -> None:
        return
    
    def close_nxt_con(self) -> None:
        return self._nxt_brick.close()
    
    def _is_running_program_on_nxt(self) -> bool:
        try:
            if self._nxt_brick.get_current_program_name():
                return True
        # NoActiveProgramError - no active program on nxt
        except:
            return False
    
    def get_nxt_brick(self) -> Brick|None:
        return self._nxt_brick
    
    def get_latest_message(self) -> tuple[int]|int:
        return self.received_messages[-1]

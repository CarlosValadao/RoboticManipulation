from nxt.locator import find
from nxt.brick import Brick
from nxt.error import DirectProtocolError
from constants import MAILBOX1, MAILBOX3, MAILBOX10, NXT_BLUETOOTH_MAC_ADDRESS
import RPP
from threading import Thread
from nxt.locator import BrickNotFoundError
from nxt.error import DirectProtocolError
from time import sleep
from os import name, system
from Assets import datetime_formated

# By default use MAILBOX1 to send messages
# and MAILBOX10 do receive/read messages

# Manages the communication between the supervisor and the robot over Bluetooth
class SupervisorClient:
    def __init__(self, nxt_bluetooth_mac):
        self._is_nxt_connected: bool = False
        self._nxt_brick: Brick = self.establish_nxt_connection(nxt_bluetooth_mac)
        # As soon as messages are read they're stored here
        self._aux_recv_data_msg: list[tuple[int]] = []
        self._recv_data_msg: list[tuple[int]] = []
        self._recv_response_msg: list[int] = []
        # mutexes
        self._have_new_data_message: bool = False
        self._have_new_response_message: bool = False
        self._there_is_running_program_on_nxt: bool = False
    
    # --- Connection Management ---
    
    def connect_to_nxt(self, nxt_bluetooth_mac: str) -> Brick|None:
        try:
            nxt_brick = find(host=nxt_bluetooth_mac)
            self._is_nxt_connected = True
            self.show_success_message('Connected on NXT :]')
            return nxt_brick
        except BrickNotFoundError:
            self.clear_console()
            self.show_warning_message("NXT is unreachable")
            self.show_warning_message("Trying to connect agin...")
            self._is_nxt_connected = False
            return None
    
    """force the connection with the NXT, ad infinitum every 500ms
    
    :param str nxt_bluetooth_mac: NXT MAC address
    
    :return: The nxt Brick object
    :rtype: nxt.Brick.Brick
    """
    def force_nxt_connection(self, nxt_bluetooth_mac: str) -> Brick:
        while not self._is_nxt_connected:
            nxt_brick = self.connect_to_nxt(nxt_bluetooth_mac)
            sleep(0.5)
        return nxt_brick

    def establish_nxt_connection(self, host: str) -> Brick:
        nxt_brick = self.connect_to_nxt(host)
        if not nxt_brick:
            nxt_brick = self.force_nxt_connection(host)
        return nxt_brick

    def close_nxt_connection(self) -> None:
        return self._nxt_brick.close()
    
    # --- Message Handling ---
    
    def send_message(self, request_code) -> None:
        try:
            formatted_msg = RPP.format_message(request_code=request_code)
            self._nxt_brick.message_write(MAILBOX1, formatted_msg)
        except DirectProtocolError:
            self.show_warning_message("It's impossible to send messages\
                                    - there's nothing running on NXT")
    
    def _read_message(self, mailbox: int, is_data_msg: bool) -> str:
        try:
            (inbox, received_message) = self._nxt_brick.message_read(mailbox, 0, True)
            if is_data_msg:
                self._have_new_data_message = True
            else:
                self._have_new_response_message = True
            return received_message.decode()
        except DirectProtocolError:
            return ''
    
    def _read_all_messages(self, mailbox: int, is_data_msg: bool) -> None:
        has_active_program = self._is_running_program_on_nxt()
        while has_active_program:
            received_message = self._read_message(mailbox, is_data_msg)
            data = RPP.parse_message(received_message)
            if self._have_new_data_message:
                self._recv_data_msg.append(data)
                self._have_new_data_message = False
            elif self._have_new_response_message:
                self._recv_data_msg.append(data)
                self._have_new_response_message = False
            print(f'[RECEIVED] -> {datetime_formated()} - {data}')
            has_active_program = self._is_running_program_on_nxt()
        self.show_warning_message("It's impossible to read new messages - \
                                there's nothing running on NXT")
        self.show_warning_message('Ending NXT connection')
        self.close_nxt_connection()
    
    def get_data_msgs(self) -> list[tuple[int]]:
        if self._recv_data_msg:
            temp = self._recv_data_msg.copy()
            self._recv_data_msg = []
            return temp
        return []
    
    def get_response_msgs(self) -> list[int]:
        if self._recv_response_msg:
            temp = self._recv_response_msg.copy()
            self._recv_response_msg = []
            return temp
        return []
    
    # --- Utilities ---
    
    """Start two threads that catch all the messages from the NXT Brick
        from two differents mailboxes, using self._read_all_messages
    """
    def catch_all_messages(self) -> None:
        Thread(target=self._read_all_messages, kwargs={'mailbox': MAILBOX3, 'is_data_msg': True}).start()
        Thread(target=self._read_all_messages, kwargs={'mailbox': MAILBOX3, 'is_data_msg': False}).start()
    
    def _is_running_program_on_nxt(self) -> bool:
        try:
            current_program_name = self._nxt_brick.get_current_program_name()
            if current_program_name:
                self._current_program_name = current_program_name
                return True
        except DirectProtocolError:
            self._current_program_name = None
            return False
    
    def get_nxt_brick(self) -> Brick|None:
        return self._nxt_brick

    def clear_console(self) -> None:
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def show_warning_message(self, message) -> None:
        print(f'[WARNING] - {message}')
    
    def show_success_message(self, message) -> None:
        print(f'[SUCCESS] - {message}')
    
if __name__ == '__main__':
    supervisor_client = SupervisorClient(NXT_BLUETOOTH_MAC_ADDRESS)
    request_message = RPP.format_message(request_code=0)
    supervisor_client.send_message(request_message)
    supervisor_client.catch_all_messages()
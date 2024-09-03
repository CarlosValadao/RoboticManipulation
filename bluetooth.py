import bluetooth

def list_bluetooth_devices():
    print("Procurando dispositivos Bluetooth...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
    
    if not nearby_devices:
        print("Nenhum dispositivo encontrado.")
        return None

    print("Dispositivos encontrados:")
    for idx, (addr, name) in enumerate(nearby_devices, start=1):
        print(f"{idx}: {name} - {addr}")
    
    return nearby_devices

def connect_bluetooth_device(device_address, port=1):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
        sock.connect((device_address, port))
        print("Conexão Bluetooth estabelecida com sucesso!")
        return sock
    except bluetooth.btcommon.BluetoothError as err:
        print(f"Erro ao conectar: {err}")
        return None

def main():
    nearby_devices = list_bluetooth_devices()
    
    if not nearby_devices:
        return

    try:
        device_index = int(input("Digite o número do dispositivo ao qual deseja conectar: ")) - 1
        if device_index < 0 or device_index >= len(nearby_devices):
            print("Número inválido.")
            return

        device_address, device_name = nearby_devices[device_index]
        print(f"Tentando conectar ao dispositivo {device_name}...")
        sock = connect_bluetooth_device(device_address)
        
        if sock:
            # Enviar dados de exemplo
            sock.send("Olá, Android!")
            print("Mensagem enviada!")
            sock.close()
    except ValueError:
        print("Entrada inválida.")

if __name__ == "__main__":
    main()

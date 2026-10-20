from struct import pack, unpack
import json

SOCKET_PATH = '/tmp/pi-manager.sock'

def receive_exact_bytes(sock, target_amount):
    accumulated_data = b''  # Start with an empty byte string
    
    # Keep looping as long as we haven't reached our target
    while len(accumulated_data) < target_amount:
        # Calculate how many bytes are STILL missing
        bytes_remaining = target_amount - len(accumulated_data)
        
        # Ask the socket ONLY for the remaining chunk
        # (This is the socket read step we will test on the Pi later)
        packet = sock.recv(bytes_remaining)
        
        # Safety check: If the socket returns nothing, the other side disconnected unexpectedly
        if not packet:
            raise ConnectionError("Socket closed prematurely.")
            
        # Append the new chunk to our pile
        accumulated_data += packet
        
    return accumulated_data

# --- RECEIVE LOGIC ---
def read_message(sock, MAX_PAYLOAD=1<<20, timeout=5):
    # Step A: Get the 4-byte header using our extraction loop
    if timeout > 0:
        sock.settimeout(timeout)
    header_bytes = receive_exact_bytes(sock, 4)
    
    # Step B: Unpack the tuple and grab the first element [0]
    payload_length = unpack('>I', header_bytes)[0]
    if payload_length > MAX_PAYLOAD:
        raise ValueError(f"payload to large: {payload_length} bytes")
    # Step C: Use the extraction loop again to get the exact JSON payload
    raw_json_bytes = receive_exact_bytes(sock, payload_length)
    
    # Step D: Turn bytes back into text and parse the dictionary
    return json.loads(raw_json_bytes.decode('utf-8'))


# --- SEND LOGIC ---
def write_message(sock, data_dict):
    # Step A: Convert the dictionary to raw bytes
    json_bytes = json.dumps(data_dict).encode('utf-8')
    
    # Step B: Create the 4-byte header out of the length integer
    header = pack('>I', len(json_bytes))
    
    # Step C: Slam them together and push them into the socket stream
    sock.sendall(header + json_bytes)
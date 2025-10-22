from pymavlink import mavutil

# Connect to our simulator
connection = mavutil.mavlink_connection("tcp:127.0.0.1:14550")

while True:
    # Receive next mavlink message
    msg = connection.recv_msg()
    # If no message, continue loop
    if not msg:
        continue
    # If message type is HEARTBEAT, print it
    if msg.get_type() == 'HEARTBEAT':
        print(msg)

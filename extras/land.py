import time
from pymavlink import mavutil

connection = mavutil.mavlink_connection("tcp:127.0.0.1:14550",source_system=255,source_component=5)

connection.wait_heartbeat()
print("Got heartbeat")    

# Define a function used to send commands in the future
# Unused params are left at 0
def send_command(command,confirmation,param1=0,param2=0,param3=0,param4=0,param5=0,param6=0,param7=0):
    """
    Send a COMMAND_LONG message to (sys,comp) = (1,1)
    """
    connection.mav.command_long_send(
        1,1,
        command,
        confirmation,
        param1,
        param2,
        param3,
        param4,
        param5,
        param6,
        param7
        )


# Now we need to arm the vehicle
print("Sending LAND")
send_command(
    mavutil.mavlink.MAV_CMD_NAV_LAND  , # Command
    0, # Confirmation
    param4=float('nan'),
    param5=51.4234178,
    param6=-2.6715506,
    param7=0 # Altitude
    )

# Check if land was successful
msg = connection.recv_match(type="COMMAND_ACK",blocking=True)
print(msg)
if msg.result != mavutil.mavlink.MAV_RESULT_ACCEPTED:
    print("Error sending LAND")
    exit()

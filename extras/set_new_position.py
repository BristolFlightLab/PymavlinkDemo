import time
from pymavlink import mavutil

connection = mavutil.mavlink_connection("tcp:127.0.0.1:14550",source_system=255,source_component=5)

connection.wait_heartbeat()
print("Got heartbeat")    

msg = connection.recv_match(type="GLOBAL_POSITION_INT",blocking=True)

# Get current system time from last msg
time_pair = (time.time(), msg.time_boot_ms)

# Setup the bitfields to tell the vehicle to ignore velocity and accelerations
ignore_velocity = (mavutil.mavlink.POSITION_TARGET_TYPEMASK_VX_IGNORE
    | mavutil.mavlink.POSITION_TARGET_TYPEMASK_VY_IGNORE
    | mavutil.mavlink.POSITION_TARGET_TYPEMASK_VZ_IGNORE
    | mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_RATE_IGNORE
    )

ignore_accel = (mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE
    | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE
    | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE
    )

print("Set new position")

def set_position(lat,lng,alt):
    connection.mav.set_position_target_global_int_send(
        time_pair[1]+int(round((time.time()-time_pair[0])*1000)),
        1,
        1,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        (ignore_velocity | ignore_accel),
        int(lat*(10**7)), # Lat (degE7)
        int(lng*(10**7)), # Long (degE7)
        alt, # Altitude
        0,0,0, # Velocities
        0,0,0, # Accels
        0, # Yaw
        0 # Yaw rate
        )

set_position(51.425,-2.671,50)
time.sleep(0.5)

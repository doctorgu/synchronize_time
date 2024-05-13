"""synchronize time by NTP server"""

import math
import socket
import struct
from datetime import datetime, timezone
import win32api

# https://gist.github.com/nihal111/23faa51c3f88a281b676dcbac77ce015

# List of servers in order of attempt of fetching
server_list = [
    "pool.ntp.org",
    "time.windows.com",
    "ntp.iitb.ac.in",
    "time.nist.gov",
]

"""
Returns the epoch time fetched from the NTP server passed as argument.
Returns none if the request is timed out (5 seconds).
"""


def get_time_ntp(addr):
    """get time ntp"""

    # http://code.activestate.com/recipes/117211-simple-very-sntp-client/
    time_1970 = 2208988800  # Thanks to F.Lundh
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # data = "\x1b" + 47 * "\0"
    data = bytes("\x1b" + 47 * "\0", "utf-8")
    try:
        # Timing out the connection after 5 seconds, if no response received
        client.settimeout(5.0)
        client.sendto(data, (addr, 123))
        data, _ = client.recvfrom(1024)
        if data:
            epoch_time = struct.unpack("!12I", data)[10]
            epoch_time -= time_1970
            return epoch_time
    except socket.gaierror:
        return None
    except socket.timeout:
        return None


def main():
    """Iterates over every server in the list until it finds time from any one."""

    for server in server_list:
        epoch_time = get_time_ntp(server)
        if not epoch_time:
            print("Could not find time from " + server)
            continue

        # SetSystemTime takes time as argument in UTC time.
        # UTC time is obtained using fromtimestamp() with timezone.utc flag
        utc_time_new = datetime.fromtimestamp(epoch_time, timezone.utc)
        utc_time_cur = datetime.now(timezone.utc)
        # make time little faster because computer time slower always
        if utc_time_new.timestamp() == math.floor(utc_time_cur.timestamp()):
            print("Time synchronized already")
            break

        # pylint:disable=c-extension-no-member
        win32api.SetSystemTime(
            utc_time_new.year,
            utc_time_new.month,
            utc_time_new.weekday(),
            utc_time_new.day,
            utc_time_new.hour,
            utc_time_new.minute,
            utc_time_new.second,
            0,
        )
        # Local time is obtained using fromtimestamp()
        local_time = datetime.fromtimestamp(epoch_time)
        print(
            "Time updated to: "
            + local_time.strftime("%Y-%m-%d %H:%M")
            + " from "
            + server
        )
        break


main()

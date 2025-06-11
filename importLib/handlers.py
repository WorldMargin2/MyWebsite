from hashlib import sha256
import time

def get_hash_code(t:time.time)-> str:
    """
    Returns a hash code for the given time string.
    :param t: time string
    :return: hash code
    """
    return sha256(str(t).encode()).hexdigest()




def restart():
    """
    Restarts the current script.
    """
    import sys
    import subprocess
    import os
    subprocess.call([sys.executable] + sys.argv)
    sys.exit(0)
    os._exit(0)  # Ensure the script exits after restart

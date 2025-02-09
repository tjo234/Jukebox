#!/usr/bin/env
import json
import subprocess

class JukeboxOS():
    """
    Handles OS level commands for reboot, etc...
    """
    @staticmethod
    def reboot():
        """
        Reboots the entire server.
        """
        subprocess.run(["sudo reboot"])  

    @staticmethod
    def restart_mpd():
        """
        Restarts only the MPD service (useful when things get stuck)
        """
        subprocess.run(["systemctl restart mpd"])  


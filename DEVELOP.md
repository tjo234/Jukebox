# Kiosk Mode
`sudo apt install xdotool unclutter sed`
`nano ~/kiosk.sh`
`chmod u+x ~/kiosk.sh`

## Kiosk Shell Script

### ~/kiosk.sh
```
#!/bin/bash
xset s noblank
xset s off
xset -dpms

unclutter -idle 0.5 -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/$USER/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/$USER/.config/chromium/Default/Preferences

/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk https://pimylifeup.com https://www.adafruit.com &

while true; do
   xdotool keydown ctrl+Next; xdotool keyup ctrl+Next;
   sleep 10
done
```

## Kiosk Service

`sudo nano /lib/systemd/system/kiosk.service`

### kiosk.service
```
[Unit]
Description=Chromium Kiosk
Wants=graphical.target
After=graphical.target

[Service]
Environment=DISPLAY=:0.0
Environment=XAUTHORITY=/home/pi/.Xauthority
Type=simple
ExecStart=/bin/bash /home/pi/kiosk.sh
Restart=on-abort
User=pi
Group=pi

[Install]
WantedBy=graphical.target
```
`sudo systemctl enable kiosk.service`
`sudo systemctl start kiosk.service`
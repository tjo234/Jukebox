# Kiosk for Pi5

https://github.com/thagrol/Guides/blob/main/boot.pdf

1. Create the autostart directory:
`mkdir -p /home/pi/.config/autostart`

2. Create /home/pi/.config/autostart/startup.desktop
`sudo nano /home/pi/.config/autostart/startup.desktop`

3. Add the following three lines:
```
[Desktop Entry]
Type=Application
Exec=chromium --kiosk http://localhost/fullscreen
```
Replace mouespad with the command of your choice.

4. Logout and login or reboot

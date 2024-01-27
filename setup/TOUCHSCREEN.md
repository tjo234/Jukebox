1. Find the name of your touchscreen

`xinput --list`

MUST BE RUN ON THE ACTUAL TOUCHSCREEN DEVICE, NOT REMOTE VIA SSH

2. Create a config file in `/usr/share/X11/xorg.conf.d/90-rotate.conf` and use the following:

```
Section "InputClass"
    Identifier    "RotateTouchCW"
    MatchProduct    "Your Touchscreen Name"
    Option    "TransformationMatrix" "0 1 0 -1 0 1 0 0 1"
EndSection
```

More info: https://wiki.ubuntu.com/X/Config/Input

So here's the full recipe:

3. Edit `/boot/config.txt` 

`display_rotate=1`
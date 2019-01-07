# Enable Loopback 
sudo modprobe snd-aloop


# Record Devices List 
arecord -L 

# Play Devices List 
aplay -L

# Reload Alsa 
sudo alsa force-reload

# Config doesnt seem to work
```
pcm.!default {
    type plug       # <-- no { here
    slave.pcm {
        type multi
        slaves {
            a { channels 2 pcm "hw:CARD=PCH,DEV=0" }  # the real device
            b { channels 2 pcm "hw:CARD=Loopback,DEV=0" }  # the loopback driver
        }
        bindings {
            0 { slave a channel 0 }
            1 { slave a channel 1 }
            2 { slave b channel 0 }
            3 { slave b channel 1 }
        }
    }
    ttable [
        [ 1 0 1 0 ]   # left  -> a.left,  b.left
        [ 0 1 0 1 ]   # right -> a.right, b.right
    ]
}
```
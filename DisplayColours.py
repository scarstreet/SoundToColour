import numpy as np
import SoundToColour as stc
import matplotlib.pyplot as plt
from PIL import ImageColor

song_path = 'm-il.mp3'
song = stc.soundToColor(song_path)

pause = song[0]['end']

fig, ax = plt.subplots(nrows=1, ncols=1)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

for i in song:
    try:
        hex = i['colour']
        rgb = ImageColor.getcolor(hex, "RGB")
        rgb = (rgb[0]/255, rgb[1]/255, rgb[2]/255)
        ax.set_facecolor(rgb)
    except:
        pass
    plt.pause(pause-0.005)

plt.show()


# **Sound to Colour**
This is a small python project that aims to convert sound to colour and add the information for the beatmap of the rhythm game "Chromesthesia". Inspired by a type of synesthesia that allows people to see sounds as colours, shapes or other visual elements. The process of this conversion will be refered to as color synchronization.

## How It Works

The color synchronization function works by reading the music beforehand and inserting the color output for the beatmap when called. So the beatmap must first be prepared and then be inserted with the hexadecimal color codes afterward. The color is added based on when the song will be triggered. Since at most each in-game note would only be inserted for each beat, the colors are calculated per beat, then we decide which color the note should be pressed based on the color for each tempo.


We are able to obtain the tempo by first detecting the onset strength of the song and then getting the estimated tempo in beats per minute. Onset is the beginning of a musical note or other sound. In librosa, it is the is determined by the following equation:

  

Meanf( MAX(0, S[f ,t] - ref[f, t- lag])

  

Where ref is S after local max filtering along the frequency axis and ref is a pre-computed reference spectrum with the same shape as S is available as an option. It will be calculated from S if it is not provided. Then we obtain the seconds per beat by the equation spb = 60 / T . Where spb is the seconds per beat and T is the tempo in beats per minute.

  

After obtaining the spb, we’d need to assign a color for each beat interval. The color is assigned based on its pitch and loudness. For loudness, we must first obtain the root mean square of the sample, which represents the average of the track’s amplitude over a period of time, which happens to be its spb. From the sample, the amplitude is squared then averaged over a period of time, afterwards used to calculate the root mean result (What Is "RMS (Root Mean Square)"?, 1997). Below is an example of the rms for one whole song.

  
  

Pitch on its own is somewhat a rigid concept, therefore we will use a more quantitative value which is known as a MIDI note number. We can obtain a midi note number by the frequency of a sound sample. To get the frequency of one sample, we use fast fourier transform to convert the amplitude in the time domain to be in a frequency domain. When the frequency domain is made, we take the frequency that has the highest magnitude. This frequency is known to be the most dominant frequency of the whole sample, therefore it will represent as the dominating frequency of this one beat that will be used to generate the color.

  

![](https://lh3.googleusercontent.com/4ZVI1k0seTydP_TVJsdl1sIImCz3Q-e8uhJYpXeomNG4SFOAbQZ5qPi0eWO2gMAwYC3ydd6z8zr_4qZBPQrA5YiOIr2KjmqESw3E-NeALA_UPBtnlE-ACGRvJgvXjJsrz9I3tTlzCEgfchJgyA)

After getting the frequency, we are able to obtain the Midi note number by the formula m = 12*log2(f/440Hz)+69 Where m is the midi note number and f is the input frequency. In the execution however, we do not use this function. We simply obtain it by a function provided by the Librosa package.

All the previously obtained Midi is then stored in a python list of dictionaries, along with a few other values within the dictionary, which are the seconds in which the sample starts and ends and its amplitude.

After obtaining the midi of each beat, we are able to apply color to them by the color-music system. According to the color-music system, the first pitch which is C starts with a red, then C# is red-orange, D is orange, D# is orange-yellow, E is yellow, F is green, and so on until B which is violet. This can easily fit the HSV system for each octave. This is because the HSV system’s initial hue, 0°, starts with red and ends with red at 360°. The color will start as red again for the next octave, but to show a difference of octave from the color, we’ll adjust the value to be higher and gradually less saturated for each increasing octave.

![](https://lh3.googleusercontent.com/fj_UGTrbAmjizDV1akoXkvQIIiXqHlWIN3RKEoZlMqnlj6h0kURt1OYHt1JKPGIuD1nEMVxe2MmvRmSYw_hZtly3JV9i3Xn84esVELDQ1WHVjn_Ruy7j_hbCBALXcot-A3m4zU3WsNf1PVvazw)

To take into account the loudness of the sound of that beat, we’ll take the sample’s amplitude and compare it to the highest amplitude of the song. A sample with a higher amplitude will have lower saturation and higher value.

The colors are then converted from HSV format to hexadecimal so that it would be easier for the unity application to read. After the format conversion, the hexadecimal string is returned and assigned to the dictionary in the list. After obtaining the python dictionary of samples with each their respective hexadecimal codes, we read the premade beatmap. For each note within the beatmap, we check the appearance time and under which beat it falls under based on the previous dictionary. The note’s information is then inserted with the color code of the sample dictionary.



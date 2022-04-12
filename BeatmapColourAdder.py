from SoundToColour import soundToColor

# D:\Projects\unity\Chromesthesia\Chromesthesia\Assets\AssetsUI\Assets-main\Resources
path = input("input resources folder location:")
if(path[-1] != '\\'):
  path += '\\'
songlistPath = path + 'songlist.txt'

def getFromInfo(categ, info):
  c = [i for i in info if categ in i][0]
  c = c.split('=')[-1]
  return c

with open(songlistPath) as songlist:
    folders = songlist.readlines()
    folders = [f if f[-1]!='\n' else f[:-1] for f in folders]
    for folder in folders:
      infoPath = path + 'Songs\\' + folder +'\\info.txt'
      with open(infoPath) as infotxt:
        info = infotxt.readlines()
        info = [i if i[-1] != '\n' else i[:-1] for i in info]
        
        songName = getFromInfo('> audio=', info) + '.mp3'
        bmEasy = getFromInfo('> beatmap-easy=', info) + '.txt'
        bmNormal = getFromInfo('> beatmap-normal=', info) + '.txt'
        bmHard = getFromInfo('> beatmap-hard=', info) + '.txt'
        
        songPath = path + 'Songs\\' + folder + '\\' + songName
        bmEasyPath = path + 'Songs\\' + folder + '\\' + bmEasy
        bmNormalPath = path + 'Songs\\' + folder + '\\' + bmNormal
        bmHardPath = path + 'Songs\\' + folder + '\\' + bmHard
        
        beatMapFiles = [bmEasyPath,bmNormalPath,bmHardPath]
        
        colourDictionary = soundToColor(songPath)
        for bmPath in beatMapFiles:
          try:
            bm = []
            with open(bmPath) as bmTxt:
              bm = bmTxt.readlines()
              bm = [b if b[-1] != '\n' else b[:-1] for b in bm]
              contentIndex = bm.index('<body>') + 1
              content = bm[contentIndex:]
              content = [c.split(',') for c in content]
              for c in content:
                time = c[-1] if int(c[0]) == 0 else c[5]
                time = float(time)
                for color in colourDictionary:
                  if(color['start'] <= time < color['end']):
                    c[1] = color['colour']
                    break
              content = [','.join(c) for c in content]
              bm[contentIndex:] = content
              # for b in bm:
              #   print(b)
              bm = '\n'.join(bm)
            bmTxt = open(bmPath, 'w')
            bmTxt.write(bm)
            print(songName + " || " + bmPath + " - done")
          except:
            print(songName + " || " + bmPath + " - ERROR!!! file may have incorrect format")



from pprint import pprint, pformat
from sys import exit
from typing import Dict
from xml.etree.cElementTree import parse
import xmltodict

phonemeTable = {'a':'aa', 'i':'iy', 'M':'uw', 'e':'eh', 'o':'ow', 'k':'k', 'k\'':'k', 'g':'g', 'g\'':'g', 'N':'nx', 'N\'':'nx', 's':'s', 'S':'sh', 'z':'z', 'Z':'zh', 'dz':'z', 'dZ':'jh', 't':'t', 't\'':'t', 'ts':'ts', 'tS':'ch', 'd':'d', 'd\'':'d', 'n':'n', 'J':'n', 'h':'hx', 'h\\':'hx', 'C':'hx', 'p\\':'f', 'p\\\'':'f', 'b':'b', 'b\'':'b', 'p':'p', 'p\'':'p', 'm':'m', 'm\'':'m', 'j':'yx', '4':'r', '4\'':'r', 'w':'w', 'N\\':'n'}

def phonemeConvert(phnms: str) -> str:
    if phnms == str(phnms):
        return ''.join(phonemeTable[x] for x in phnms.split())
    else:
        try:
            return ''.join(phonemeTable[x] for x in phnms['#text'].split())
        except:
            return '_'



obj:Dict = xmltodict.parse(open('ready steady.vsqx', encoding='utf-8').read())
version = list(obj.keys())[0][3]
obj = next(iter(obj.values()))
print(type(obj))
if version == '3':
    msPerTick: float = (1/(float(obj['masterTrack']['tempo'][0]['bpm'])/60))*180
else:
    msPerTick: float = (1/(float(obj['masterTrack']['tempo'][0]['v'])/60))*180
def ticksToMs(ticks:int) -> float:
    return ticks*msPerTick

def noteToNote(note:int) -> int:
#    return note - 35
   return round((2 ** ((note - 69)/12))*440)

print(msPerTick)
lastTick = 0

if version == '3':
    for x in obj['vsTrack']['musicalPart']['note']:
        startPost = int(x['posTick'])
        duration = int(x['durTick'])
        if int(startPost) != lastTick:
            print('[_<' + str(startPost - lastTick) + '>' + ']', end='')
        print('[' + phonemeConvert(x['phnms']) +'<' + str(round(ticksToMs(duration))) + ',' + str(noteToNote(int(x['noteNum']))) + '>' + ']', end='')
        lastTick = startPost + duration
else:
    for x in obj['vsTrack']['vsPart']['note']:
        startPost = int(x['t'])
        duration = int(x['dur'])
        if int(startPost) != lastTick:
            print('[_<' + str(startPost - lastTick) + '>' + ']', end='')
        print('[' + phonemeConvert(x['p']) +'<' + str(round(ticksToMs(duration))) + ',' + str(noteToNote(int(x['n']))) + '>' + ']', end='')
        lastTick = startPost + duration
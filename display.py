import datetime
import math
import subprocess

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = 24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

width = disp.width
height = disp.height
font = ImageFont.truetype('/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf', 12)

logs = []
min = 100
max = 0

for line in open('/tmp/ambient.csv'):
  items = line.split(',')

  items[1] = float(items[1])
  items[2] = float(items[2])

  if min > items[2]:
    min = items[2]
  if max < items[2]:
    max = items[2]

  logs.append(items)

image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

max = math.ceil(max)
min = math.floor(min)

bottom = 54

# Axis label
draw.text((0, 0), str(max),  font=font, fill=255)
draw.text((0, bottom-4), str(min),  font=font, fill=255)
draw.text((24,bottom), "{}-{}".format(logs[0][0][6:], logs[-1][0][6:]),  font=font, fill=255)

# Axis border
draw.line((16,6,16,bottom), fill=255)
draw.line((16,bottom,128,bottom), fill=255)

# Line graph
bx = 16
by = 6

for index, item in enumerate(logs):
  # calculate
  x = 16 + index
  y = (1 - (item[2] - min) / (max - min)) * (bottom - 6) + 6

  draw.line((bx,by,x,y), fill=255)

  bx = x
  by = y

# Latest value
last = 0
if by < 24:
  last = 24

draw.text((86,last), "{}\n{}°C".format(logs[-1][0][6:], logs[-1][2]),  font=font, fill=255)

# Internet reachability
res = subprocess.call(['ping','-c','1','45.32.60.194'])
if res == 0:
  draw.text((112,bottom),"BT", font=font, fill=255)

disp.image(image)
disp.display()


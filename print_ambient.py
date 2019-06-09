import smbus
import time
import datetime

i2c = smbus.SMBus(1)
address = 0x5c

# Wake up sensor
try:
    i2c.write_i2c_block_data(address,0x00,[])
except:
    pass

# Measure
time.sleep(0.003)
i2c.write_i2c_block_data(address,0x03,[0x00,0x04])

# Read
time.sleep(0.5)
block = i2c.read_i2c_block_data(address,0,6)
hum = float(block[2] << 8 | block[3])/10
tmp = float(block[4] << 8 | block[5])/10

# Print
dt_now = datetime.datetime.now()
print(dt_now.strftime('%m/%d %H:%M'), hum, tmp, sep=",")

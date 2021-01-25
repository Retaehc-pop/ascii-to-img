from digi.xbee.devices import XBeeDevice
import base64
from os import path
from PIL import Image
import re

PORT = 'COM11'
BAUD = 19200
ser = XBeeDevice(PORT, BAUD)
try:
    ser.open()
    def data_receive_callback(xbee_message):
        global line
        global lines
        global oldline
        global realdata
        data = xbee_message.data.decode("utf-8", 'ignore')
        data = re.sub('0123456789abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNNM+/-', '', data)
        if data == "-":
            print(data)
            x = 0
            while path.exists('img%s.png' % str(x)):
                x += 1
            with open("file.txt", 'r') as f:
                content = f.read()
            with open("file.txt", 'w') as f:
                f.truncate()
            content += "=" * (4 - len(content) % 4)
            imgdata = base64.b64decode(content)
            with open('img%s.png' % str(x), 'wb')as f1:
                f1.write(imgdata)
            try:
                im = Image.open('img%s.png' % str(x))
                im.show()
            except:
                im = Image.open('corrupt.jpg')
                im.show()
        elif data[:6] == 'TOTAL:':
            lines = int(data[6:])
            print(lines)
        elif data[:5] == 'Time:':
            timew = float(data[5:])
            print(timew)
        else:
            line = int(data[:4])
            realdata = data[4:]
            if lines != line:
                if line > lines:
                    lines = line
                else:
                    print(lines-line)
                    print(lines-line)
                    print(lines-line)
                    print(lines-line)
                    for i in range(lines - line):
                        with open("file.txt", "a") as f2:
                            f2.write('A'*110)
                    lines=line
            lines -= 1
            with open("file.txt", "a") as f2:
                f2.write(realdata)
            print(line)
            print(realdata)


    ser.add_data_received_callback(data_receive_callback)
    print("Wait to start")
    input()
finally:
    print("error port not found")
    ser.close()

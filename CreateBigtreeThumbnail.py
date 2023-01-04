import base64

from UM.Logger import Logger
from cura.Snapshot import Snapshot
from PyQt6.QtCore import QByteArray, QIODevice
from ..Script import Script

class CreateBigtreeThumbnail(Script):
    def __init__(self):
        super().__init__()

    def encodeSnapShot(self, width, height):
        result = ""
        img = Snapshot.snapshot(width, height)

        result += ";"+(hex(width)[2:]).rjust(4,'0')+(hex(height)[2:]).rjust(4,'0')+"\n"
        for ypos in range(0,height):
            result += ";"
            for xpos in range(0,width):
                data = img.pixel(xpos, ypos)
                encoded = (hex(((data & 0x00F80000) >> 8 ) | ((data & 0x0000FC00) >> 5 ) | ((data & 0x000000F8) >> 3 ))[2:]).rjust(4,'0')
                if encoded == "0020" or encoded == "0841" or encoded == "0861":
                    encoded = "0000"
                result = result + encoded
            result += "\n"    
        return result

    def getSettingDataString(self):
        return """{
            "name": "Create Bigtree Thumbnail",
            "key": "CreateBigtreeThumbnail",
            "metadata": {},
            "version": 2,
            "settings":
            {}
        }"""

    def execute(self, data):
        Logger.log("d", "CreateBigtreeThumbnail:execute")

        snapshot_gcode = ""
        snapshot_gcode = snapshot_gcode + self.encodeSnapShot(70,70)
        snapshot_gcode = snapshot_gcode + self.encodeSnapShot(95,80)
        snapshot_gcode = snapshot_gcode + self.encodeSnapShot(95,95)
        snapshot_gcode = snapshot_gcode + self.encodeSnapShot(160,140)
        snapshot_gcode = snapshot_gcode + self.encodeSnapShot(200,200)
        snapshot_gcode = snapshot_gcode + "; bigtree thumbnail end\n\n"

        data[0] = snapshot_gcode + data[0]
        return data
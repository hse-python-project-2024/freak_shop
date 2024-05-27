from aenum import Enum

class Fingers(Enum):

    _init_ = 'value string'

    THUMB = 1, 'two thumbs'
    INDEX = 2, 'offset location'
    MIDDLE = 3, 'average is not median'
    RING = 4, 'round or finger'
    PINKY = 5, 'wee wee wee'

    def __str__(self):
        return self.string

x = Fingers.PINKY
print(x.value)

from midea.command import base_command

VERSION = '0.1.7'


class packet_builder:

    def __init__(self):
        self.command = None

        # # this is an incoming control packet (to the ac)
        # # Always starts with 5a5a
        # 0x5a, 0x5a, \
        # # message type
        # 0x01, 0x11, \
        # # packet length
        # 0x68, \
        # # dunno
        # 0x00, 0x44, 0x80, \
        # # message id
        # 0x84, 0x5e, 0x00, 0x00, \
        # # date and time
        # 0x79, 0x87, 0x36, 0x01, 0x19, 0x05, 0x14, 0x14, \
        # # device id  (note the hex is reversed, so this is 0x0e0000003f0c = 15393162805004
        # 0x0c, 0x3f, 0x00, 0x00, 0x00, 0x0e, \
        # # dunno after this.
        # 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        # 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xa2, 0xcb, 0xfd, 0x80, 0xad, 0xd7, 0x2f, 0xdf,
        # 0x57, 0x0b, 0x2f, 0x04, 0x55, 0xc0, 0x43, 0x71, 0x6d, 0x42, 0x10, 0xee, 0x3a, 0x6a, 0x84, 0x1a,
        # 0x06, 0x43, 0x9c, 0xcf, 0x87, 0x78, 0xba, 0xdd, 0x70, 0xf0, 0x33, 0xe0, 0x00, 0x3f, 0x79, 0x08,
        # 0xc8, 0xd0, 0xb6, 0x32, 0xfe, 0x4f, 0x44, 0xb9, 0x24, 0xa9, 0xae, 0x6a, 0x3a, 0xef, 0x62, 0xb3,
        # 0xc3, 0x80, 0x33, 0x12, 0x1f, 0x89, 0xe4, 0x4f

        # Init the packet with the header data. Weird magic numbers, I'm not sure what they all do, but they have to be there (packet length at 0x4)
        self.packet = bytearray([
            0x5a, 0x5a, 0x01, 0x11, 0x5c, 0x00, 0x20, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x0e, 0x03, 0x12, 0x14, 0xc6, 0x79, 0x00, 0x00,
            0x00, 0x05, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00
        ])

    def set_command(self, command: base_command):
        self.command = command.finalize()

    def finalize(self):
        # Append the command data to the packet
        self.packet.extend(self.command)
        # Append a basic checksum of the command to the packet (This is apart from the CRC8 that was added in the command)
        self.packet.extend([self.checksum(self.command[1:])])
        # Ehh... I dunno, but this seems to make things work. Pad with 0's
        self.packet.extend([0] * (46 - len(self.command)))
        # Set the packet length in the packet!
        self.packet[0x04] = len(self.packet)
        return self.packet

    def checksum(self, data):
        return 255 - sum(data) % 256 + 1

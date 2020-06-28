# coding=Big5
from smartcard.System import readers
from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace
from resources.namespaces import ns_smartcard


@ns_smartcard.route('')
class SmartCardResource(Resource):
    def get(self):
        """
        Ū�����O�d
        """
        # define the APDUs used in this script
        SelectAPDU = [0x00, 0xA4, 0x04, 0x00, 0x10, 0xD1, 0x58, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                      0x00, 0x00, 0x00, 0x11, 0x00]

        ReadProfileAPDU = [0x00, 0xca, 0x11, 0x00, 0x02, 0x00, 0x00]

        # get all the available readers
        r = readers()
        print("Available readers:", r)

        reader = r[0]
        print("Using:", reader)

        connection = reader.createConnection()
        connection.connect()

        data, sw1, sw2 = connection.transmit(
            SelectAPDU)
        print("Select Applet: %02X %02X" % (sw1, sw2))

        data, sw1, sw2 = connection.transmit(ReadProfileAPDU)
        # print data
        print("Command: %02X %02X" % (sw1, sw2))
        print('Card Number : %s' % ''.join(chr(i) for i in data[0:12]))
        print('Name : %s' % ''.join(chr(i) for i in data[12:18]))
        print('ID Number : %s' % ''.join(chr(i) for i in data[32:42]))
        print('Birthday : %s' % ''.join(chr(i) for i in data[43:49]))
        print('Sex : %s' % ''.join(chr(i) for i in data[49:50]))
        print('Card Date : %s' % ''.join(chr(i) for i in data[51:57]))

        name = ''.join(chr(i) for i in data[12:18])

        return make_response(jsonify('123456'), 200)
#!/usr/bin/env python
import unittest

from webwol import format_wol


class WolFormatTestCase(unittest.TestCase):
    def test_wol_format(self):
        """Tests that wake-on-lan packets match the specified format.

        Wake-On-Lan "Magic Packets" have the following format:

        ffffffffffffmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmac
        macmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmac
        macmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmacmac
        """
        sync_stream = bytes(b"\xff\xff\xff\xff\xff\xff")
        mac_bytes = bytes(b"\xc0\xff\xee\xbe\xee\xef" * 16)
        expected_packet = sync_stream + mac_bytes

        self.assertEqual(format_wol("c0:ff:ee:be:ee:ef"), expected_packet)


if __name__ == "__main__":
    unittest.main()

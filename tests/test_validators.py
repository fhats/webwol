#!/usr/bin/env python
import unittest

from webwol import reject_config


class ValidatorsTestCase(unittest.TestCase):
    def test_good_config(self):
        good_config = {"a": "aa:aa:aa:aa:aa:aa"}
        self.assertFalse(reject_config(good_config))

    def test_type_and_depth(self):
        bad_configs = [
            {"b": 1},
            {"c": ["ab", "cd"]},
            {"d": {"e": "fg"}}
        ]
        for config in bad_configs:
            self.assertTrue(reject_config(config))

    def test_mac_non_mac(self):
        only_non_mac = {"badmac": "not-a-mac"}
        self.assertTrue(reject_config(only_non_mac))

        mixed_mac_nonmac = {"badmac": "not-a-mac", "goodmac": "01:23:45:67:89:ab"}
        self.assertTrue(reject_config(mixed_mac_nonmac))


if __name__ == "__main__":
    unittest.main()

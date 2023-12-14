#!/usr/bin/env
import unittest

from jukebox._model import get_db_connection

class TestJukebox(unittest.TestCase):
    def test_connection(self):
        db = get_db_connection()
        self.assertTrue(db != None)
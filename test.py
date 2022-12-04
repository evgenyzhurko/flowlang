import unittest
import logging

from flowlang.tests import *
from flowlang.base_library.tests import *

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(created)f - %(message)s')
    unittest.main()
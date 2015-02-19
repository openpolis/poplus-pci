#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from test_popit import *
from test_mapit import *

__author__ = 'guglielmo'

# log format (if used in tests)
FORMAT = "[PCI | %(levelname)s] %(message)s"
logging.basicConfig(level = logging.WARN, format=FORMAT)

## invoke tests
if __name__ == '__main__':
    import oktest
    oktest.run(r'.*Test$')

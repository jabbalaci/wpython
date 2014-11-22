#!/usr/bin/env python2
# encoding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
from django.utils.datastructures import SortedDict

def main():
    d = SortedDict({'b': 1, 'a': 2, 'c': 3})
    print(d)
    print(sys.argv[1:])

##############################################################################

if __name__ == "__main__":
    main()

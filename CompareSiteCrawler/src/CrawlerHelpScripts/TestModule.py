'''
Module to test stuff
'''

import re

match = re.match('[0-9]{10,13}', '837463718372')
print match
if match:
    print 'match bij 1'
else:
    'geen match bij 1'
match = None
print match
if match:
    print 'match bij 2'
else:
    print 'geen match bij 2'
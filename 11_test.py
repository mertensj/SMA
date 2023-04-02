#!/usr/bin/python3

import datetime
from SMA import *

sb = SMA()

# TOTAL DAY Wh COUNTER
sb.getLogger('txt')
# PER HOUR Wh TODAY
#print(sb.getLogger())
#print('DAY TOTAL : ',sb.value('productivity_day'))
#totalWh = sb.value('productivity_total')
print('Total Wh Counter : ',sb.value('productivity_total'))

sb.logout()


tup1 = ('physics', 'chemistry', 1997, 2000);
tup2 = (1, 2, 3, 4, 5 );
tup3 = "a", "b", "c", "d";

for x in tup3: print(x) 


import time

print("time.ctime() : %s" % time.ctime())
print("time.asctime() : %s" % time.asctime())
print("time.gmtime() : %s" % str(time.gmtime()))

import calendar

# cal = calendar.month(2023, 1)
# print("Here is the calendar:")
# print(cal)
# cal2 = calendar.calendar(2023,w=2,l=1,c=6)
# print(cal)

calendar.prcal(2023,w=2,l=1,c=6)
calendar.prmonth(2023,1,w=2,l=1)
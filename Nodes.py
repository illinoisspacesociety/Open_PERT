from datetime import datetime, timedelta
import Class

source = "TestSave1.p"
# source = "TestSave2.p"

epoch = Class.datetime(2019, 3, 13)

A = Class.Node()    # event
A.name = "A"        # name
A.label = "Test_A"
A.dur = 10          # duration
A.dep = []          # dependencies on other events
A.start = datetime(2019, 3, 13)           # start time, can be pushed back if dependencies incomplete
A.end = A.start + timedelta(days=A.dur)   # end time, can be later than earliest completion time

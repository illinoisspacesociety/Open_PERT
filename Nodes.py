import Class

epoch = Class.datetime(2019, 3, 13)

A = Class.Node()    # event
A.name = "A"        # name
A.dur = 10          # duration
A.dep = []          # dependencies on other events
A.start = Class.datetime(2019, 3, 13)           # start time, can be pushed back if dependencies incomplete
A.end = A.start + Class.timedelta(days=A.dur)   # end time, can be later than earliest completion time

B = Class.Node()
B.name = "B"
B.dur = 25
B.dep = []
B.start = Class.datetime(2019, 3, 13)
B.end = B.start + Class.timedelta(days=B.dur)

C = Class.Node()
C.name = "C"
C.dur = 10
C.dep = ["A"]
C.start = Class.datetime(2019, 3, 13)
C.end = C.start + Class.timedelta(days=C.dur)

D = Class.Node()
D.name = "D"
D.dur = 10
D.dep = ["C", "A"]
D.start = Class.datetime(2019, 3, 13)
D.end = D.start + Class.timedelta(days=D.dur)
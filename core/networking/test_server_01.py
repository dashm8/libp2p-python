
def handlerdef():
    print("hello world!!!")
s = ServerTcp("0.0.0.0",4444)
s.handlers["msgtype"] = handlerdef
s.Run()
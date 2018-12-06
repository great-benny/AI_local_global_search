import time
import datetime

currTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
logFileName = 'log_' + currTime + '.txt'

# if os.path.exists('log.txt'):
#   os.remove('log.txt')

LogFile = open(logFileName, 'a')


# calculate the overall attacks among n queens. cost=0 represents for no attacks, which is the problem goal.
def calc_cost(boardlist):
    cost = 0
    boardsize = boardlist.__len__()

    # print('boardlist= \n', boardlist) # Debug

    for i in range(0, boardsize):
        for j in range(i + 1, boardsize):
            if abs(boardlist[i] - boardlist[j]) == abs(i - j):
                cost += 1

    return cost

def call_time():
    # ts = time.gmtime()
    # st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
    st = str(datetime.datetime.now()) #.strftime('%Y-%m-%d_%H-%M-%S')

    return st

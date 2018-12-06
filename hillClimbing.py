from utility import *
import copy
import inspect

TotalSucc = 0   # Total number of successful runs
TotalSteps = 0  # Sum up all steps from each run to a total number

class hillClimb:
    def __init__(self, verbocity, boardsize, passboard=None):
        # TODO check options
        # self.totalsucc = 0
        # self.totalnumsteps = 0

        self.verbocity = verbocity
        self.boardsize = boardsize
        # self.boardlist = passboard.boardlist
        self.cboard = passboard
        self.cost = 0

    def hcSolution(self):
        global TotalSteps
        global TotalSucc
        global LogFile

        OnceSteps = 0

        while 1:
            currViolations = calc_cost(self.cboard.boardlist)
            # print('currViolations = ', currViolations) # Debug
            # print('before lower cost: ')
            # print(self.board.boardlist)
            # print(self.board)
            self.cboard.boardlist = self.getlowercostboard(self.cboard.boardlist)
            # print('after lower cost: ')
            # print(self.board.boardlist)
            # print(self.board)
            newCost = self.cost
            # print('newCost = ', newCost) # Debug
            # self.printFrame()  # Debug
            if currViolations == newCost:
                break
            TotalSteps += 1
            OnceSteps += 1
            # print('Total num of steps: ', TotalSteps) # Debug
            if self.verbocity == True:
                print('Search', OnceSteps, ', Board Attacks:', newCost, '  Current solution is', self.cboard.boardlist)
                strLine = 'Search ' + str(OnceSteps) + ', Board Attacks: ' + str(newCost) + '   Current solution is' + \
                          str(self.cboard.boardlist)
                LogFile.write(strLine + '\n')
            # self.printFrame() # Debug

            # if currViolations == newCost:
            #     break

        if newCost != 0:
            if self.verbocity == True:
                print('\nGOAL FAIL!   The current BEST solution is', self.cboard.boardlist)
                strLine = '\nGOAL FAIL!   The current BEST solution is ' + str(self.cboard.boardlist)
        else:
            if self.verbocity == True:
                print('\nGOAL SUCCEED!   The solution is', self.cboard.boardlist)
                strLine = '\nGOAL SUCCEED!   The solution is ' + str(self.cboard.boardlist)
                TotalSucc += 1

        LogFile.write(strLine + '\n')

        # print('Total success: ', TotalSucc) # Debug

    # this function tries moving every queen to every spot, with only one move
    # and returns the move that has the least number of violations
    def getlowercostboard(self, boardlist):
        global TotalSteps

        self.cost = calc_cost(boardlist)
        # print('oldcost = ', self.cost) # Debug
        lowestavailable = boardlist

        # while 1:
        #     indexes = random.sample(range(0, boardlist.__len__() - 1), 2)
        for i in range(0, boardlist.__len__()):
            for j in range(i + 1, boardlist.__len__()):
                # try placing the queen newly and see if it's better or not
                tryboardlist = copy.deepcopy(lowestavailable)
                # print('\nbefore: tryboardlist = ', tryboardlist, 'oldcost = ', oldcost)
                tryboardlist[i], tryboardlist[j] = lowestavailable[j], lowestavailable[i]
                newcost = calc_cost(tryboardlist)
                # print('after tryboardlist = ', tryboardlist, 'newcost = ', newcost)

                # print('newcost, oldcost = ', newcost, ', ', oldcost) # Debug

                if newcost < self.cost:
                    self.cost = newcost
                    lowestavailable = tryboardlist
                    # print('newcost = ', newcost, ' lowestavailable= ', lowestavailable) # Debug
                    # print('newcost = ', newcost) # Debug
                    # TotalSteps += 1
                    # print('Total num of steps: ', TotalSteps) # Debug
                    break

        return lowestavailable

    def getTotalNumSteps(self):
        global TotalSteps
        # print('Print: ', TotalSteps) # Debug

        return TotalSteps

    def getTotalSucc(self):
        global TotalSucc
        # print('Print: ', TotalSucc) # Debug

        return TotalSucc

    def printFrame(self):
        callerframerecord = inspect.stack()[1]  # 0 represents this line
        # 1 represents line at caller
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        print(info.filename, info.lineno, info.function)

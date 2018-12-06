#!/usr/bin/python
 
from random import randint
import sys,copy
from utility import *

from termcolor import colored

from optparse import OptionParser
try:
  import psyco
  psyco.full()
except ImportError:
  pass

from hillClimbing import *
from geneticAlgo import *

"""
cowboy code, but seems to work
USAGE: python prog <numberruns=1> <verbocity=False>
"""

startLogTime = ''

class board:
    def __init__(self, dim=8):
        self.dim = dim
        self.boardlist = self.genList(dim)   # initialize the boardlist
        self.board = [[0 for i in range(0, dim)] for j in range(0, dim)]  # initialize the board's dimension

    # define how to print the board
    def __repr__(self):
        self.list2board()
        mstr = ''
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if self.board[i][j] == 'Q':
                    mstr = mstr + colored(str(self.board[i][j]), color='yellow', attrs=['bold', 'reverse']) + ' '
                else:
                    mstr = mstr + str(self.board[i][j]) + ' '
            mstr = mstr + '\n'

        return mstr

    def genList(self, genslen):
        qlist = list()

        for i in range(0, genslen):
            qlist.append(i)

        reslist = Chromosome(copy.deepcopy(qlist))
        qlist_copy = copy.deepcopy(qlist)
        for i in range(0, qlist_copy.__len__()):
            randGenIdx = randint(0, qlist_copy.__len__() - 1)
            randGen = qlist_copy[randGenIdx]
            qlist_copy.remove(randGen)
            reslist[i] = randGen

        return reslist

    def list2board(self):
        # place queens at right places on the square board
        self.board = [[0 for i in range(0, self.dim)] for j in range(0, self.dim)]  # re-initialize the board's dimension
        for i in range(0, self.dim):
            self.board[i][self.boardlist[i]] = 'Q'


class queens:
  def __init__(self, boardsize, numruns, verbocity):
    #TODO check options
    self.totalRuns = numruns
    self.totalSucc = 0
    self.totalNumSteps = 0
    self.verbocity = verbocity
    self.boardsize = boardsize
    self.numRuns = numruns


  def runSolution(self, method):
    global LogFile


    if method == 'HC':
        strLine = '< Start solution by hill-climbing ... >'
        print(strLine)
        LogFile.write(strLine + '\n')
    elif method == 'GA':
        strLine = '< Start solution by genetic algorithm ...>'
        print(strLine)
        LogFile.write(strLine + '\n')

    for i in range(0, self.numRuns):
      if self.verbocity == True:
        _st = call_time()
        if i == 0:
            global startLogTime
            startLogTime = _st
        print(colored('======================================', 'yellow'))
        strLine = 'RUN' + str(i + 1) + '   ' + _st
        print(colored(strLine, 'yellow'))
        print(colored('======================================', 'yellow'))
        LogFile.writelines(['======================================\n', strLine+'\n',
                            '======================================\n'])


      self.mboard = board(self.boardsize)

      if method == 'HC':
        self.mhillClimb = hillClimb(verbocity=self.verbocity, boardsize=self.boardsize, passboard=self.mboard)
        self.mhillClimb.hcSolution()
      elif method == 'GA':
        self.mgeneAlgo = geneticAlgo(boardsize=self.boardsize)
        self.mboard.boardlist = self.mgeneAlgo.gaSolution()

      print('The final configuration of board:')
      print(self.mboard)

 
  def printstats(self, method):
    if method == 'HC':
      self.totalSucc = self.mhillClimb.getTotalSucc()
      self.totalNumSteps = self.mhillClimb.getTotalNumSteps()
    elif method == 'GA':
      self.totalSucc = self.mgeneAlgo.getTotalSucc()
      self.totalNumSteps = self.mgeneAlgo.getTotalNumSteps()

    _st = call_time()

    global startLogTime
    print('============================================================')
    print('Begin Time:  ', startLogTime)
    print('Finish Time: ', _st)
    print('Total Runs: ', self.totalRuns)
    print('Total Success: ', self.totalSucc)
    print('Success Percentage: ', float(self.totalSucc)/float(self.totalRuns))
    print('Average number of steps: ', float(self.totalNumSteps)/float(self.totalRuns))
    print('============================================================')

    LogFile.writelines(['============================================================\n',
                        'Begin Time: ' + startLogTime + '\n',
                        'Finish Time: ' + _st + '\n',
                        'Total Runs: ' + str(self.totalRuns) + '\n',
                        'Total Success: ' + str(self.totalSucc) + '\n',
                        'Success Percentage: ' + str(float(self.totalSucc)/float(self.totalRuns)) + '\n',
                        'Average number of steps: ' + str(float(self.totalNumSteps) / float(self.totalRuns)) + '\n',
                        '============================================================\n'
                        ])
 
if __name__ == '__main__':
 
  parser = OptionParser()
  parser.add_option('-q', '--quiet', dest='verbose',
                   action='store_false', default=True,
                   help="Don't print all the moves... wise option if using large numbers")
 
  parser.add_option('-m', '--numrun', dest='runs', help='Number of runs', default=10, type='int') # type = string(Default), int, long, choice, float and complex

  parser.add_option('-s', '--boardsize', dest='dims', help='Size of board', default=8, type='int')

  parser.add_option('-a', '--algorithm', dest='algo', help='Method of solution', default='HC')
  # parser.add_option('--algorithm', dest='algo', help='Method of solution', default='GA')

  (options, args) = parser.parse_args()

  t1 = str(datetime.datetime.now())

  mboard = queens(verbocity=options.verbose, numruns=options.runs, boardsize=options.dims)
  mboard.runSolution(method=options.algo)
  mboard.printstats(method=options.algo)

  t2 = str(datetime.datetime.now())
  datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
  diff = datetime.datetime.strptime(t2, datetimeFormat) \
         - datetime.datetime.strptime(t1, datetimeFormat)

  print('>>> Total Elapsed Time: ', diff)
  LogFile.write('>>> Total Elapsed Time: ' + str(diff) + '\n')
  LogFile.close()

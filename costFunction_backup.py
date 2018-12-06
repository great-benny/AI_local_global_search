import random, copy

class costFunc:
    def __init__(self, boardsize=8):
        self.boardsize = boardsize
        self.cost = 0


    def calc_cost(self, boardlist):
        cost = 0
        # seqlist = self.board2list(tboard)

        # print('boardlist= \n', boardlist) # Debug

        for i in range(0, self.boardsize):
            for j in range(i + 1, self.boardsize):
                # print('self.boardsize = ', self.boardsize)
                # print('i, j = ', i, j)
                if abs(boardlist[i] - boardlist[j]) == abs(i - j):
                    cost += 1

        return cost

        # these are separate for easier debugging
        # totalhcost = 0
        # totaldcost = 0
        #
        # for i in range(0, self.boardsize):
        #     for j in range(0, self.boardsize):
        #         # if this node is a queen, calculate all violations
        #         if tboard.board[i][j] == 'Q':
        #             # subtract 2 so don't count self
        #             # sideways and vertical
        #             totalhcost -= 2
        #             for k in range(0, self.boardsize):
        #                 if tboard.board[i][k] == 'Q':
        #                     totalhcost += 1
        #                 if tboard.board[k][j] == 'Q':
        #                     totalhcost += 1
        #             # calculate diagonal violations
        #             k, l = i + 1, j + 1
        #             while k < self.boardsize and l < self.boardsize:
        #                 if tboard.board[k][l] == 'Q':
        #                     totaldcost += 1
        #                 k += 1
        #                 l += 1
        #             k, l = i + 1, j - 1
        #             while k < self.boardsize and l >= 0:
        #                 if tboard.board[k][l] == 'Q':
        #                     totaldcost += 1
        #                 k += 1
        #                 l -= 1
        #             k, l = i - 1, j + 1
        #             while k >= 0 and l < self.boardsize:
        #                 if tboard.board[k][l] == 'Q':
        #                     totaldcost += 1
        #                 k -= 1
        #                 l += 1
        #             k, l = i - 1, j - 1
        #             while k >= 0 and l >= 0:
        #                 if tboard.board[k][l] == 'Q':
        #                     totaldcost += 1
        #                 k -= 1
        #                 l -= 1
        # return ((totaldcost + totalhcost) / 2)

    # this function tries moving every queen to every spot, with only one move
    # and returns the move that has the least number of violations
    def getlowercostboard(self, boardlist):
        oldcost = self.calc_cost(boardlist)
        print('oldcost = ', oldcost)
        lowestavailable = boardlist

        # while 1:
        #     indexes = random.sample(range(0, boardlist.__len__() - 1), 2)
        for i in range(0, boardlist.__len__()):
            for j in range(i+1, boardlist.__len__()):
                # try placing the queen newly and see if it's better or not
                tryboardlist = copy.deepcopy(lowestavailable)
                # print('\nbefore: tryboardlist = ', tryboardlist, 'oldcost = ', oldcost)
                tryboardlist[i], tryboardlist[j] = lowestavailable[j], lowestavailable[i]
                newcost = self.calc_cost(tryboardlist)
                # print('after tryboardlist = ', tryboardlist, 'newcost = ', newcost)

                # print('newcost, oldcost = ', newcost, ', ', oldcost) # Debug

                if newcost < oldcost:
                    oldcost = newcost
                    self.cost = newcost
                    lowestavailable = tryboardlist
                    # print('newcost = ', newcost, ' lowestavailable= ', lowestavailable) # Debug
                    # print('newcost = ', newcost) # Debug
                    # break

        # move one queen at a time, the optimal single move by brute force
        # for q_row in range(0, self.boardsize):
        #     for q_col in range(0, self.boardsize):
        #         if mboard.board[q_row][q_col] == 'Q':
        #             # get the lowest cost by moving this queen
        #             for m_row in range(0, self.boardsize):
        #                 for m_col in range(0, self.boardsize):
        #                     if mboard.board[m_row][m_col] != 'Q':
        #                         # try placing the queen here and see if it's any better
        #                         tryboard = copy.deepcopy(mboard)
        #                         tryboard.board[q_row][q_col] = 0
        #                         tryboard.board[m_row][m_col] = 'Q'
        #                         thiscost = self.calc_cost(tryboard)
        #                         if thiscost < lowcost:
        #                             lowcost = thiscost
        #                             lowestavailable = tryboard

        return lowestavailable

    def getCurrentCost(self):
        return self.cost

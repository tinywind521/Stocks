from numpy import *
import pymysql
from datetime import *
from threading import Thread
import csv
import time


def loadUserAffectionFromDb():
    connectImpl = pymysql.connect(user='****', password='****', host='****', db='*****')
    cursorImpl = connectImpl.cursor()

    selectSql = "select userid, actorid, sum(sqrt(cost)) as total_sqrt_cost \
                from user_big_actor_daily_cost where date>'2016/4/1' and \
                userid in (select userid from (select userid, count(DISTINCT actorid) as actor_count, sum(cost) as sum_cost \
                from user_big_actor_daily_cost group by userid \
                having actor_count>2 and sum_cost>=10) t)\
                GROUP BY userid,actorid"
    cursorImpl.execute(selectSql)
    currData = cursorImpl.fetchall()
    cursorImpl.close()
    connectImpl.close()
    print('user affection data has been loaded at '+str(datetime.now()))
    return currData


def loadOfficeId():
    connectImpl = pymysql.connect(user='****', password='****', host='****', db='*****')
    cursorImpl = connectImpl.cursor()

    selectSql = "select * from office_id"
    cursorImpl.execute(selectSql)
    currData = cursorImpl.fetchall()
    cursorImpl.close()
    connectImpl.close()
    print('office id has been loaded at '+str(datetime.now()))
    return set(currData)


def loadValidActorid(fileName='validActor.txt'):
    validActorList = []
    for actor in open(fileName).readlines():
        validActorList.append(int(actor.strip()))
    return set(validActorList)


def filterActorid(actorIdSet, officeIdSet):
    validActorList = []
    for actor in actorIdSet:
        if actor not in officeIdSet:
            validActorList.append(actor)
    print('original actor:'+str(len(actorIdSet))+' office actor:'+str(len(officeIdSet))+' filtered actor:'+str(len(validActorList)))
    return validActorList


def getVectorWithAffDict(actorDict):
    actorArr = array(actorDict.items())
    scoreValidActorArr = actorArr[nonzero(actorArr[:, 1] >= 5)[0]]
    scorePercArr = scoreValidActorArr[:,1]/sum(actorDict.values())
    if len(scorePercArr) == 0:
        return []
    scorePercArr /= max(scorePercArr)
    scorePercArr *= 10
    validActorIndex = nonzero(scorePercArr >= 1)[0]
    if len(validActorIndex) < 2:
        return []

    validActorArr = vstack((scoreValidActorArr[validActorIndex,0],scorePercArr[validActorIndex])).T
    return validActorArr


def getUserAffectDict(rawAffTuple):
    userAffDict = {}
    for everyLine in rawAffTuple:
        userid, actorid, energy_cost = everyLine
        if userid not in userAffDict:
            userAffDict[userid] = {}
        userAffDict[userid][actorid] = energy_cost
    print('raw user affection dict has been generated at '+str(datetime.now()))
    return userAffDict


def getValidUerAccectDict(userAffDict):
    validUserAffDict = {}
    validActorset = set([])
    for user in userAffDict:
        currActorAffArr = getVectorWithAffDict(userAffDict[user])
        if len(currActorAffArr) == 0:
            continue
        validActorset = validActorset.union(currActorAffArr[:,0])
        validUserAffDict[user] = currActorAffArr
    print('filtered user affection dict has been generated at '+str(datetime.now()))
    return validUserAffDict, validActorset


def getUserAffectMat(userAffDict, userList, actorList):
    m, n = len(userList), len(actorList)
    affMat = zeros((m, n))

    print('start to generate affection mat at '+str(datetime.now()))
    processCount = 0
    for user in userAffDict:
        userIndex = userList.index(user)
        for line in userAffDict[user]:
            processCount += 1
            if processCount % 10000 == 0:
                print(processCount, datetime.now())
            actor, score = line
            actorIndex = actorList.index(actor)
            affMat[userIndex, actorIndex] = score
    return affMat


def getGaps(m, n):
    doubSectArea = m*m/n
    gaps = [0]*n
    for i in range(1,n):
        lastN = gaps[i-1]
        currN = sqrt(doubSectArea+lastN**2)
        gaps[i] = int(currN)
        print(i, currN, gaps[i])
    gaps.append(m)
    return gaps


def singleThread(simMat, affMat, currRange):
    m, n = shape(affMat)

    print('range:', currRange, 'start to generate similar mat at '+str(datetime.now()))
    processCount, zeroCount = [0]*2
    for i in range(currRange[0], currRange[1]):
        for j in range(n):
            if i > j:
                processCount += 1
                if processCount % 100000 == 0:
                    print('range:', currRange, processCount, zeroCount, processCount-zeroCount, datetime.now())
                iScoreArr = affMat[:, i]
                jScoreArr = affMat[:, j]
                scoreMultipArr = multiply(iScoreArr, jScoreArr)
                simDegree = sum(scoreMultipArr)
                if simDegree == 0:
                    zeroCount += 1
                    continue
                simMat[i, j] = simDegree
    print('range:', currRange, 'finished to generate similar mat at '+str(datetime.now()))


def getSimilarMat(affMat, threCount):
    m, n = shape(affMat)
    simMat = zeros((n, n))
    gapList = getGaps(n, threCount)

    threadList = [Thread(target=singleThread, args=(simMat, affMat, [gapList[i], gapList[i+1]],)) for i in range(threCount)]
    for thread in threadList:
        thread.start()
        time.sleep(1)
    for thread in threadList:
        thread.join()
    simMat = simMat.T + simMat
    return simMat


def exportToCsv(currMat,fileName):
    currArr = array(currMat)
    rawFile = csv.writer(open(fileName, 'wb+'), dialect='excel')
    for i in range(len(currArr)):
        rawFile.writerow(currArr[i])

officeIdSet = loadOfficeId()
validActorSet = loadValidActorid()
rawAffTuple = loadUserAffectionFromDb()
userAffDict = getUserAffectDict(rawAffTuple)
validUserAffDict, validActorset = getValidUerAccectDict(userAffDict)

userList = validUserAffDict.keys()
actorList = list(set(filterActorid(validActorset, officeIdSet))&validActorSet)
print(len(userList), len(actorList))

affMat = getUserAffectMat(validUserAffDict, userList, actorList)
simMat = getSimilarMat(affMat, 4)

print('start to calc laplace matrix at '+str(datetime.now())+'\n')
diagMat = mat(sum(simMat, axis=1).A*eye(len(simMat)))
# lapMat = dialect - simMat

print('start to calc ordinary eig matrix at '+str(datetime.now())+'\n')
eigVal,eigVec = linalg.eig(lapMat)

print('start to calc diag mat sqrl i matrix at '+str(datetime.now())+'\n')
diagMatSqrtI = sqrt(diagMat).I

print('start to calc normal laplace matrix at '+str(datetime.now())+'\n')
normLapMat = diagMatSqrtI*lapMat*diagMatSqrtI

print('start to calc normal eig matrix at '+str(datetime.now())+'\n')
normEigVal, normEigVec = linalg.eig(normLapMat)

print('start to calc norm eig vectors matrix at '+str(datetime.now())+'\n')
normEigVecTrans = normEigVec*diagMatSqrtI

print('start to export sim_mat at '+str(datetime.now())+'\n')
exportToCsv(simMat, 'sim_1.csv')
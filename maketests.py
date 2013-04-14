from sys import *

def makeStatDict(filename):
    print 'Getting Team Stats...'
    f = open(filename, 'r')

    statdict = {}

    currentteam = ''
    for line0 in f:
        line = line0.strip()
        splitline = [x for x in line.split('\t') if x != '']
        linelen = len(splitline)
        if linelen == 1:
            currentteam = splitline[0]
            statdict[currentteam] = []
            w10 = [0,0,0,0,0,0,0,0,0,0]
            l10 = [0,0,0,0,0,0,0,0,0,0]
            pf10 = [0,0,0,0,0,0,0,0,0,0]
            pa10 = [0,0,0,0,0,0,0,0,0,0]
            w = 0
            l = 0
            wh = 0
            lh = 0
            pf = 0
            pa = 0
        
        else:
            date = dateToInt(splitline[0])
            statdict[currentteam].append([date, w, l, \
                                          sum(w10[-5:]), sum(l10[-5:]), \
                                          sum(w10), sum(l10), \
                                          wh, lh, \
                                          w-wh, l-lh, \
                                          pf, pa, \
                                          sum(pf10[-5:]), sum(pa10[-5:]), \
                                          sum(pf10), sum(pa10)])


            forscore = int(splitline[4].split('-')[0])
            againstscore = int(splitline[4].split('-')[1])
            pf += forscore
            pa += againstscore
            pf10.pop(0)
            pf10.append(forscore)
            pa10.pop(0)
            pa10.append(againstscore)

            didwin = forscore > againstscore
            if didwin:
                w += 1
                l10.pop(0)
                l10.append(0)
                w10.pop(0)
                w10.append(1)
                if splitline[5].strip() == 'H':
                    wh += 1
            else:
                l += 1
                w10.pop(0)
                w10.append(0)
                l10.pop(0)
                l10.append(1)
                if splitline[5].strip() == 'H':
                    lh += 1

    f.close()
    return statdict


def makeGameDict(filename):
    print 'Getting Game Outcomes...'
    f = open(filename, 'r')

    gamedict = {}

    hometeam = ''
    for line0 in f:
        line = line0.strip()
        splitline = [x for x in line.split('\t') if x != '']
        linelen = len(splitline)

        if linelen == 1:
            hometeam = splitline[0]
##            print '\t' + hometeam
            continue

        date = dateToInt(splitline[0])

        if splitline[3] == 'P':
            spread = 0
        else:
            spread = splitline[3]
        if spread == 'NL':
            continue
        spread = float(spread)

        if splitline[5] == 'H':
            hscore = int(splitline[4].split('-')[0])
            vscore = int(splitline[4].split('-')[1])
        else:
            hscore = int(splitline[4].split('-')[1])
            vscore = int(splitline[4].split('-')[0])
            spread *= -1

        awayteam = splitline[1]

        if splitline[5] == 'H':
            try:
                gamedict[date].append(((spread, vscore-hscore), (hometeam, awayteam)))
            except:
                gamedict[date] = [((spread, vscore-hscore), (hometeam, awayteam))]

    f.close()
    return gamedict


def dateToInt(date0):
        monthconv = {}
        monthconv['10'] = '0'
        monthconv['11'] = '1'
        monthconv['12'] = '2'
        monthconv['1'] = '3'
        monthconv['2'] = '4'
        monthconv['3'] = '5'
        monthconv['4'] = '6'
        monthconv['5'] = '7'
        monthconv['6'] = '8'

        date = date0.split('/')
        month = monthconv[date[0]]
        day = date[1]
        if len(day) == 1:
            day = '0' + day
        date = int(month + day)
        return date


def getStats(statdict, team, date):
    gamelist = statdict[team]
    for game in gamelist:
        if game[0] == date:
            return game[1:]
    print date, gamelist
    print 'No game found!'
    return None


if __name__ == "__main__":
    year = argv[1]

    stats = makeStatDict('data/' + year + 'spreads.mky')
    games = makeGameDict('data/' + year + 'spreads.mky')
    gamedays = games.keys()
    gamedays.sort()

    print 'Writing games...'
    outfile = open('data/' + year + 'sprd.mky', 'w')

    for gameday in gamedays:
        gamelist = games[gameday]
        for game in gamelist:
            scores, teams = game
            spread, result = scores
            hometeam, awayteam = teams

            outfile.write(str(spread) + '\t' + str(result) + '\n')

            homestats = getStats(stats, hometeam, gameday)
            homeline = hometeam
            for stat in homestats:
                homeline += '\t' + str(stat)
            outfile.write(homeline + '\n')

            awaystats = getStats(stats, awayteam, gameday)
            awayline = awayteam
            for stat in awaystats:
                awayline += '\t' + str(stat)
            outfile.write(awayline + '\n')

            outfile.write('\n')

    outfile.close()

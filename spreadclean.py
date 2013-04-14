from sys import *

if __name__ == "__main__":
    teamnames = {}
    teamnames['ATLANTA HAWKS'] = 'Atlanta'
    teamnames['BOSTON CELTICS'] = 'Boston'
    teamnames['CHARLOTTE BOBCATS'] = 'Charlotte'
    teamnames['CHARLOTTE HORNETS'] = 'Charlotte'
    teamnames['CHICAGO BULLS'] = 'Chicago'
    teamnames['CLEVELAND CAVALIERS'] = 'Cleveland'
    teamnames['DALLAS MAVERICKS'] = 'Dallas'
    teamnames['DENVER NUGGETS'] = 'Denver'
    teamnames['DETROIT PISTONS'] = 'Detroit'
    teamnames['GOLDEN STATE WARRIORS'] = 'Golden St.'
    teamnames['HOUSTON ROCKETS'] = 'Houston'
    teamnames['INDIANA PACERS'] = 'Indiana'
    teamnames['LOS ANGELES CLIPPERS'] = 'LA Clippers'
    teamnames['LOS ANGELES LAKERS'] = 'LA Lakers'
    teamnames['MEMPHIS GRIZZLIES'] = 'Memphis'
    teamnames['VANCOUVER GRIZZLIES'] = 'Vancouver'
    teamnames['MIAMI HEAT'] = 'Miami'
    teamnames['NEW ORLEANS HORNETS'] = 'N. Orleans'
    teamnames['NEW ORLEANS'] = 'N. Orleans'
    teamnames['MILWAUKEE BUCKS'] = 'Milwaukee'
    teamnames['MINNESOTA TIMBERWOLVES'] = 'Minnesota'
    teamnames['NEW JERSEY NETS'] = 'New Jersey'
    teamnames['N. ORL./OKLA. CITY HORNETS'] = 'NO/OKC'
    teamnames['NEW YORK KNICKS'] = 'New York'
    teamnames['ORLANDO MAGIC'] = 'Orlando'
    teamnames['PHILADELPHIA 76ERS'] = 'Philadelphia'
    teamnames['PHOENIX SUNS'] = 'Phoenix'
    teamnames['PORTLAND TRAILBLAZERS'] = 'Portland'
    teamnames['PORTLAND TRAIL BLAZERS'] = 'Portland'
    teamnames['SACRAMENTO KINGS'] = 'Sacramento'
    teamnames['SAN ANTONIO SPURS'] = 'San Antonio'
    teamnames['SEATTLE SUPERSONICS'] = 'Seattle'
    teamnames['TORONTO RAPTORS'] = 'Toronto'
    teamnames['UTAH JAZZ'] = 'Utah'
    teamnames['WASHINGTON WIZARDS'] = 'Washington'
    teamnames['CHARLOTTE HORNETS'] = 'Charlotte'
    teamnames['GOLDEN ST. WARRIORS'] = 'Golden St.'
    teamnames['WASHINGTON BULLETS'] = 'Washington'

    subs = {}
    subs['H1'] = 'H'
    subs['H2'] = 'H'
    subs['HN'] = 'H'
    subs['HN1'] = 'H'
    subs['HN2'] = 'H'

    subs['V1'] = 'V'
    subs['V2'] = 'V'
    subs['VN'] = 'V'
    subs['VN1'] = 'V'
    subs['VN2'] = 'V'

    subs['\''] = '.5 '

    subs['New Orleans'] = 'N. Orleans'

    year = argv[1]
    rawfile = open('./data/' + year + 'spreads.raw', 'r')
    writefile = open('./data/' + year + 'spreads.mky', 'w')

    for line0 in rawfile:
        line = line0.strip()
        if line == '':
            continue

        if line in teamnames.values():
            writefile.write(line + '\n')
            continue        

        try:
            line = teamnames[line.upper()]
        except:
            if not len(line.split()[0].split('/')) == 2:
                continue
            
            for sub in subs.keys():
                line = line.replace(sub, subs[sub])

            line = [x.strip() for x in line.split('  ') if x != '']

            if line[2] == 'NL':
                line.insert(3, 'NL')

            if len(line) == 5:
                line.insert(2, 'NL')
                line.insert(2, 'NL')

            elif len(line) == 6:
                if 'H' in line[5] or 'V' in line[5]:
                    tmp = line[5].split(' ')
                    line[5] = tmp[0]
                    line.append(tmp[1])
                elif line[1].split(' ')[-1] in ['W', 'L', 'N']:
                    tmp = line[1].split(' ')
                    tmpname = tmp[0]
                    for word in tmp[1:-1]:
                        tmpname += ' ' + word
                    line[1] = tmpname
                    line.insert(2, tmp[-1])

            if len(line) != 7:
                print line

            tmpline = line[0]
            for val in line[1:]:
                tmpline += '\t' + val
            line = tmpline

        writefile.write(line + '\n')

    rawfile.close()
    writefile.close()



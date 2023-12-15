import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import seaborn as sns
import math
import warnings
from datetime import timedelta
import io
import base64

season2022RaceCalendar = pd.read_csv('data/Formula1_2022season_calendar.csv')
season2022RaceCalendar.set_index('Round', inplace=True)
season2022Drivers = pd.read_csv('data/Formula1_2022season_drivers.csv')
season2022Drivers.set_index('Abbreviation', inplace=True)
season2022Teams = pd.read_csv('data/Formula1_2022season_teams.csv')
season2022Teams.index = range(1,11)
season2022QualifyingResults = pd.read_csv('data/Formula1_2022season_qualifyingResults.csv')
season2022SprintRaceResults = pd.read_csv('data/Formula1_2022season_sprintRaceResults.csv')
season2022RaceResults = pd.read_csv('data/formula1_2022season_raceResults.csv')
season2022DotdVotes = pd.read_csv('data/formula1_2022season_driverOfTheDayVotes.csv')
season2022DotdVotes.set_index('Track', inplace=True)

def assign_color(val_type, values):
    cl = []
    for val in values:
        if val_type == 'drivers':  abbr = val.split()[1].upper()[0:3]
        elif val_type == 'teams':  abbr = val[0:4].upper()
        if abbr in ['ALFA','BOT','ZHO']:           cl.append('#900000')
        elif abbr in ['HAAS','SCH','MAG']:         cl.append('#ffffff')
        elif abbr in ['ASTO','VET','STR','HUL']:   cl.append('#006f62')
        elif abbr in ['WILL','ALB','LAT','DE']:    cl.append('#0072ff')
        elif abbr in ['ALPH','GAS','TSU']:         cl.append('#2b5962')
        elif abbr in ['MCLA','RIC','NOR']:         cl.append('#ff8700')
        elif abbr in ['RED ','VER','PER']:         cl.append('#0600f0')
        elif abbr in ['FERR','LEC','SAI']:         cl.append('#cb0000')
        elif abbr in ['MERC','HAM','RUS']:         cl.append('#00d2bd')
        elif abbr in ['ALPI','ALO','OCO']:         cl.append('#0090ff')
    return cl

racePoints = season2022RaceResults.groupby(['Driver', 'Team'])['Points'].sum().sort_values(ascending=False)
sprintRacePoints = season2022SprintRaceResults.groupby(['Driver'])['Points'].sum().sort_values(ascending=False)
for driver in season2022RaceResults['Driver'].unique():
    if driver not in season2022SprintRaceResults['Driver'].unique():
        sprintRacePoints.loc[driver] = 0
driverStandings = (racePoints + sprintRacePoints).fillna(0).sort_values(ascending=False)
driverStandings = pd.DataFrame(driverStandings).reset_index()
driverStandings['POS'] = range(1,23)
driverStandings['Points'] = driverStandings['Points'].astype(int)
driverStandings.set_index('POS', inplace=True)

driverStandingsTop10 = driverStandings['Driver'][:10].values
driverPointsTop10 = {};  driverPointsTop10Sprint = {}
for driver in driverStandingsTop10:
    driverPointsTop10[driver] = season2022RaceResults[season2022RaceResults['Driver'] == driver]['Points'].values
    driverPointsTop10Sprint[driver] = season2022SprintRaceResults[season2022SprintRaceResults['Driver'] == driver] \
        ['Points'].values
sp = [3, 10, 20]
for driver in driverStandingsTop10:
    for i in range(len(sp)):
        driverPointsTop10[driver][sp[i]] = driverPointsTop10[driver][sp[i]] + driverPointsTop10Sprint[driver][i]

tracks = season2022RaceResults['Track'].unique()
tracksSprint = season2022SprintRaceResults['Track'].unique()
plt.style.use('seaborn')
plt.style.use('dark_background')
plt.rcParams['axes.facecolor'] = '#15151d'
plt.rcParams['figure.facecolor'] = '#15151d'
plt.rcParams['grid.color'] = '#444444'
plt.rcParams['font.family'] = 'Formula1'
plt.figure(figsize=(10,7))
plt.axis([-0.2,21.3,-5,460])
c = assign_color('drivers', driverStandingsTop10)
for i in range(10):
    if driverStandingsTop10[i] in ['Sergio Perez', 'Carlos Sainz', 'Lewis Hamilton', 'Fernando Alonso']:   ls = '--'
    else:   ls = '-'
    plt.plot(driverPointsTop10[driverStandingsTop10[i]].cumsum(), label=driverStandingsTop10[i].split()[1], 
             c=c[i], linewidth=2, ls=ls)
plt.title('Формула 1 - 2022 Сезон\nТоп 10 гонщиков', fontsize=14, fontweight='bold', color='#bbbbbb')
plt.xlabel('ГОНКИ', fontsize=10, fontweight='bold', color='#bbbbbb')
plt.xticks(range(0,len(tracks)), tracks, rotation=80, fontsize=8, color='#bbbbbb')
plt.yticks(range(0,460,90), range(0,460,90), fontsize=8, color='#bbbbbb')
plt.axvline(0, linewidth=1, color='#bbbbbb')
plt.axhline(0, linewidth=1, color='#bbbbbb')
plt.legend(loc=(0.04,0.61), fontsize=9)

plt.savefig('plot_1.png')
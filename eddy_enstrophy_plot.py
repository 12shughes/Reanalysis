import functions as fcs



# dataset can be OpenMARS_data, EMARS_data/Control, EMARS_data/Analysis
datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis): ')
while datachoice not in ['o', 'ec', 'ea']:
    print('Incorrect input')
    datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis): ')

if datachoice == 'o':
    dataset = 'OpenMARS_data'
    years = [28, 29, 30, 31, 32, 33, 34, 35]
elif datachoice == 'ec':
    dataset = 'EMARS_data/Control'
    years = [24, 25, 26]
elif datachoice == 'ea':
    dataset = 'EMARS_data/Analysis'
    years = [24, 25, 26, 28, 29, 30, 31, 32]


path = '/disco/share/sh1293/%s/Eddy_enstrophy/' %(dataset)
fcs.eddy_enstrophy_contourf_plot(path, years)
fcs.eddy_enstrophy_contourf_plot(path, years, scaled='yes')
fcs.eddy_enstrophy_contourf_plot(path, years, scaled='yes2')
fcs.eddy_enstrophy_climatology_plot(path, years)
fcs.eddy_enstrophy_climatology_plot(path, years, scaled='yes')
fcs.eddy_enstrophy_climatology_plot(path, years, scaled='yes2')
if datachoice == 'o':
    fcs.eddy_enstrophy_climatology_plot(path, years, scaled='yes2exc')

islev = int(input('Input chosen isentropic level for time series plot: '))
fcs.eddy_enstrophy_time_series(path, years, islev)
fcs.eddy_enstrophy_time_series(path, years, islev, scaled='yes')
fcs.eddy_enstrophy_time_series(path, years, islev, scaled='yes2')



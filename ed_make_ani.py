import os
import ffmpeg

datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis): ')
while datachoice not in ['o', 'ec', 'ea']:
    print('Incorrect input')
    datachoice = input('Enter directory code (o - OpenMARS, ec - EMARS control, ea - EMARS analysis): ')

if datachoice == 'o':
    dataset = 'OpenMARS_data'
    set = 'openmars'
    delay = 3
    #years = [28, 29, 30, 31, 32, 33, 34, 35]
    years = [29]
elif datachoice == 'ec':
    dataset = 'EMARS_data/Control'
    set = 'emars'
    delay = 1.5
    #years = [24, 25, 26]
    years = [26]
elif datachoice == 'ea':
    dataset = 'EMARS_data/Analysis'
    set = 'emars'
    delay = 1.5
    #years = [24, 25, 26, 28, 29, 30, 31, 32]
    years = [29]#, 29]

path = '/disco/share/sh1293/%s/' %(dataset)

scaled = input('Run for scaled data, yes2 or yes3 or no: ')
while scaled not in ['yes2', 'yes3', 'no']:
    print('Incorrect input')
    scaled = input('Run for scaled data, yes2 or yes3 or no: ')

if scaled == 'no':
    scal = ''
elif scaled == 'yes2':
    scal = 'scaled2_'
elif scaled == 'yes3':
    scal = 'scaled3_'

for year in years:
    print(year)
    print('making gif')
    os.system('convert -delay %s %s/Eddy_enstrophy/Ani_plots/MY%02d/%sedd_ens_my%02d*50N.png \
                    %s/Eddy_enstrophy/Animations/%sedd_ens_MY%02d_50N.gif' %(delay, path, year, scal, year, path, scal, year))
    #os.system('ffmpeg -f gif -i /disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.gif \
                    #/disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.mp4')

    print('making mp4')
    (ffmpeg.input('%s/Eddy_enstrophy/Animations/%sedd_ens_MY%02d_50N.gif' %(path, scal, year))
        .output('%s/Eddy_enstrophy/Animations/%sedd_ens_MY%02d_50N.mp4' %(path, scal, year))
        .run(overwrite_output=True))

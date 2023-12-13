import os
import ffmpeg


years = [28, 29, 30, 31, 32, 33, 34, 35]

for year in years:
    print(year)
    print('making gif')
    os.system('convert -delay 3 /disco/share/sh1293/OpenMARS_data/Eddy_enstrophy/Ani_plots/MY%02d/edd_ens_my%02d*.png \
                    /disco/share/sh1293/OpenMARS_data/Eddy_enstrophy/Animations/edd_ens_MY%02d.gif' %(year, year, year))
    #os.system('ffmpeg -f gif -i /disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.gif \
                    #/disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.mp4')

    print('making mp4')
    (ffmpeg.input('/disco/share/sh1293/OpenMARS_data/Eddy_enstrophy/Animations/edd_ens_MY%02d.gif' %(year))
        .output('/disco/share/sh1293/OpenMARS_data/Eddy_enstrophy/Animations/edd_ens_MY%02d.mp4' %(year))
        .run(overwrite_output=True))

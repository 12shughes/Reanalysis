import os
import ffmpeg


years = [27, 29, 30, 31, 32, 33, 34, 35, 36]

for year in years:
    os.system('convert -delay 3 /disco/share/sh1293/OpenMARS_data/Isentropic/Plots/MY%02d/ctf_my%02d*.png \
                    /disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY%02d.gif' %(year, year, year))
    #os.system('ffmpeg -f gif -i /disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.gif \
                    #/disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.mp4')

    (ffmpeg.input('/disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY%02d.gif' %(year))
        .output('/disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY%02d.mp4' %(year))
        .run())

import os
import ffmpeg
os.system('convert -delay 3 /disco/share/sh1293/OpenMARS_data/Isentropic/Plots/ctf_my28*.png \
                /disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.gif')
#os.system('ffmpeg -f gif -i /disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.gif \
                #/disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.mp4')

(ffmpeg.input('/disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.gif')
    .output('/disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.mp4')
    .run())
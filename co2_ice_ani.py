import os
import ffmpeg

path = '/disco/share/sh1293/OpenMARS_data/CO2_ice/Plots/stereo_cond/'
delay = 10
print('making gif')
os.system(f'convert -delay {delay} {path}/stereo_condloc*.pdf \
                {path}/Animations/my29.gif')
#os.system('ffmpeg -f gif -i /disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.gif \
                #/disco/share/sh1293/OpenMARS_data/Isentropic/Animations/ctf_MY28.mp4')

print('making mp4')
(ffmpeg.input(f'{path}/Animations/my29.gif')
    .output(f'{path}/Animations/my29.mp4')
    .run(overwrite_output=True))
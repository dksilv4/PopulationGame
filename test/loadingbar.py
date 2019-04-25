import sys
import time
done = 'false'
#here is the animation
def animate():
    done = 'false'
    while done == 'false':
        sys.stdout.write('\rloading |')
        time.sleep(0.1)
        sys.stdout.write('\rloading /')
        time.sleep(0.1)
        sys.stdout.write('\rloading -')
        time.sleep(0.1)
        sys.stdout.write('\rloading \\')
        time.sleep(0.1)
        done = 'true'
    sys.stdout.write('\rDone!     ')

animate()
#long process here

import numpy as np
import sounddevice

Clap = False
threshold = 10

def detect_clap(indata,frames,time,status):
    global Clap
    volume_norm = np.linalg.norm(indata)*10
    if volume_norm > threshold:
        print("clapped")
        Clap = True

def listen_clap():
    with sounddevice.InputStream(callback=detect_clap):
        return sounddevice.sleep(1000)

if __name__ == "__main__":
    while True:
        listen_clap()
        if Clap==True:
            break
        else:
            pass
import subprocess
import time
import os
import signal
import multiprocessing
import datetime

start = multiprocessing.Value('i', 0)

# 0 : nix
# 1 : start stream
# 2 : stop stream
# 4 : stream is running

def start_stream(): 
    while True:
        if start.value is 1:
            # start stream with shell=True
            stream = subprocess.Popen('raspivid -n -t 0 -w 1296 -h 972 -b 3500000 -fps 30 -o - | ffmpeg -re -i - -input_format h264 -vcodec copy -f flv "rtmp://live.twitch.tv/app/live_508407191_5O9MuTv2xKFwCymVsLjkbbySq9BKX1"', shell=True)
            start.value = 4
        if start.value is 2:
            try:
                # kill process
                print("EXITING STREAM")
                os.killpg(os.getpgid(stream.pid), signal.SIGTERM)
                start.value = 0
            except:
                continue
        else:
            continue
        
def check_time():
    stream_process = multiprocessing.Process(target=start_stream)
    stream_process.start()
    while True:
        now = datetime.datetime.now()
        if now.hour > 7 and now.hour < 19:
            if(start.value is 0):
                # its time to start the stream
                with start.get_lock():
                    start.value = 1
                print("started process")
                time.sleep(30)
        else:
            with start.get_lock():
                start.value = 2

if __name__ == '__main__':
    check_time()
            
    
    
    

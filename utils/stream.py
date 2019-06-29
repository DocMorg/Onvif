import os
import subprocess

def start_stream(private_stream_url, output_dir, output_filename):
    cmd = ['ffmpeg',
        '-i', '"%s"' % private_stream_url,  
        '-ar', '44100', 
        '-acodec', 'aac', 
        '-ac', '1', 
        '-strict', '-2', 
        '-crf', '18', 
        '-c:v', 'copy', 
        '-preset', 'ultrafast', 
        '-flags', '-global_header', 
        '-fflags', 'flush_packets', 
        '-tune', 'zerolatency', 
        '-hls_time', '1', 
        '-hls_allow_cache', '0',
        '-hls_list_size', '3', 
        '-hls_wrap', '4', 
        '-hls_flags', 'delete_segments', 
        '-start_number', '0', 
        os.path.join(output_dir, output_filename),
        '1>/dev/null 2>&1'
    ]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # subprocess.Popen('rm '+os.path.join(output_dir, output_filename), shell=True)
    subprocess.Popen(' '.join(cmd), shell=True)


def stop_stream(ip, port):
    cam = '%s%d' % (ip.replace('.',''), port)
    try:
        cmd = ("for PID in $(ps -ax | grep -E 'ffmpeg.*%s' | awk '{ print $1 }');"
            " do kill -9 $PID >/dev/null 2>&1; done" % cam)
        subprocess.Popen(cmd, shell=True)
        subprocess.Popen('rm '+os.path.join('./streams', cam)+'*', shell=True)
    except Exception as e:
        pass


def check_stream(ip, port):
    cam = '%s%d' % (ip.replace('.',''), port)
    cmd = "ps -ax | grep -E 'ffmpeg.*%s' | awk '{ print $1 }'" % cam
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    return list(filter(lambda x: len(x)>0, out.split('\n')))

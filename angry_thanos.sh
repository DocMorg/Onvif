for i in `ps ax | grep -E "uwsgi|ffmpeg|server.py" | awk '{print $1}'` 
do
    kill -SIGINT $i;
done

docker run -v $(pwd):/home/mambauser/chandra_bot -v /Users/wsp/Documents/Confidential:/home/mambauser/confidential -p 8877:8877 \
  -it --rm chandra_bot jupyter notebook --ip 0.0.0.0 --no-browser --allow-root \
  --port 8877 --notebook-dir=/home/mambauser
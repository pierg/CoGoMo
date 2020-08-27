#!/bin/bash
echo "** make sure that docker running on this machine **"

echo "updating repository..."
git pull

echo "pulling latest docker image..."
docker pull pmallozzi/cogomo:latest

if [ $# -eq 0 ]
  then
    echo "PROVIDE CONFIG FOLDER"
    exit 0

  else
    echo "  custom input file provided, launching with: $1/crome_specifications.py"

    echo "  cleaning up folder"
    sudo rm -r "$(pwd)/$1/results"
    mkdir "$(pwd)/$1/results"

    echo "stopping existing containers..."
    docker stop $1 || true && docker rm $1 || true

    echo "  creating new docker container..."
    echo "  name $1"
    docker create -i -t  --name $1 -v "$(pwd)/$1/results":/home/cogomo/output/results pmallozzi/cogomo:dev -c

    echo "copying input file $(pwd)/$1/crome_specifications.py"
    docker cp "$(pwd)/$1/crome_specifications.py" $1:/home/

    echo "  starting docker..."
    docker start $1
    echo "  process started...check the log file to see when it finishes."
    echo "  Or run 'docker ps' to see if the process is still running"

    echo "  results and logs will be saved in $(pwd)/$1/"
    docker logs -f $1 >& "$(pwd)/$1/logs.txt" &

fi




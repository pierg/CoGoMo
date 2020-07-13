#!/bin/bash
echo "** make sure that docker running on this machine **"

echo "stopping existing containers..."
docker stop cogomo_clustering || true && docker rm cogomo_clustering || true

echo "pulling latest docker image..."
docker pull pmallozzi/cogomo:latest

if [ $# -eq 0 ]
  then
    echo "  no custom input file provided, launching the default configuration"

    echo "  creating new docker container..."
    docker create -i -t  --name cogomo_clustering -v "$(pwd)/default/results":/home/cogomo/output/results pmallozzi/cogomo:latest -d


    echo "  starting docker..."
    docker start cogomo_clustering
    echo "  process started...check the log file to see when it finishes"
    echo "  Or run 'docker ps' to see if the process is still running"

    echo "  results and logs will be saved in $(pwd)/default/"
    docker logs -f cogomo_clustering >& "$(pwd)/default/logs.txt" &

  else
    echo "  custom input file provided, launching with: $1/mission_specification.py"

    echo "  creating new docker container..."
    docker create -i -t  --name cogomo_clustering -v "$(pwd)/$1/results":/home/cogomo/output/results pmallozzi/cogomo:latest -d

    echo "copying input file $(pwd)/$1/mission_specification.py"
    docker cp "$(pwd)/$1/mission_specification.py" cogomo_clustering:/home/

    echo "  starting docker..."
    docker start cogomo_clustering
    echo "  process started...check the log file to see when it finishes."
    echo "  Or run 'docker ps' to see if the process is still running"

    echo "  results and logs will be saved in $(pwd)/$1/"
    docker logs -f cogomo_clustering >& "$(pwd)/$1/logs.txt" &

fi




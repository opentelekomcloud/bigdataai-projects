sudo docker exec -i -t `sudo docker ps --last 1 --format '{{.ID}}'` /bin/bash


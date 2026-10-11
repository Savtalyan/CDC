rec:
	sudo docker compose up -d --force-recreate

stat:
	sudo docker ps

stat-all:
	sudo docker ps -a 

shell:
	sudo docker exec -it $(CONTAINER) /bin/bash
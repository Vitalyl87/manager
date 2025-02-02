To start app you can use this command:
    docker-compose up -d

That command will create 3 containers: db with volume for postgres data, test db and application



For development you can start only DB container and launch app from IDE:
    docker-compose up -d db



Dont forget to erase volume after development.
DB use named volume pg_data. After dev operations you can delete this volume by command:
    docker volume rm project_manager_pg_data



If you want delete all unused volumes (if targer container for this volume was deleted), you can use this command:
    docker volume prune

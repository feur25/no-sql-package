#!/bin/bash

current_position=$(pwd)
docker exec -i mongo_instance_1 mongoimport --db nosql --collection usersCollection --drop --jsonArray < "$current_position/CRUD/json/users.json" 

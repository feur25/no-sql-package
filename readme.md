
## MongoDB Replica Set With Docker
nous allons setup notre environement docker avec nos instance de mongoDB suivez les commandes suivantes :

	docker network create nosqlMongoCluster

<img width="804" alt="Capture d’écran 2024-04-17 à 19 51 07" src="https://github.com/feur25/no-sql-package/assets/39668417/9d16952e-053f-41f5-9d77-fc94cffdb3cb">

	docker compose up -d
 
<img width="783" alt="Capture d’écran 2024-04-17 à 20 58 24" src="https://github.com/feur25/no-sql-package/assets/39668417/e76a9823-25b5-4489-b4da-f172525bd166">

 Une fois celà fait vous pourrez ouvrire un nouveau terminal 
<img width="783" alt="Capture d’écran 2024-04-17 à 21 00 14" src="https://github.com/feur25/no-sql-package/assets/39668417/eefa042a-f7a8-477c-9dee-9e2513e85b2d">


	docker exec -it mongo_instance_1 mongosh --eval "rs.status()"
<img width="783" alt="Capture d’écran 2024-04-17 à 21 02 26" src="https://github.com/feur25/no-sql-package/assets/39668417/04f724bb-70c4-409c-b9bc-4bf850e0db97">
<img width="783" alt="Capture d’écran 2024-04-17 à 21 03 10" src="https://github.com/feur25/no-sql-package/assets/39668417/fd7c519c-06e1-4d08-bec7-6f70d60e5deb">


### Générer le users.json dans /CRUD/json/users.json
Utiliser le script UserGnerator.py pour régénerer le fichier, si ce dernier existe déjà :
Avant celà installer le fichier requirements via la commande suivante :

	pip3 install -r requirements.txt
<img width="783" alt="Capture d’écran 2024-04-17 à 21 06 11" src="https://github.com/feur25/no-sql-package/assets/39668417/9242f62f-6ece-460c-b017-f2417846e045">
Maintenant nous allons utiliser le script UserGnerator.py avec la commande suivante :

	python3 ./CRUD/UserGenerator.py
<img width="783" alt="Capture d’écran 2024-04-17 à 21 09 38" src="https://github.com/feur25/no-sql-package/assets/39668417/2bddaae4-f4ee-46a4-9bb7-8676e3ff0546">

Une fois nos 100 utilisateurs créer, nous allons ensuite insérer nos données à travers la CLI de MongoDB.

```shell
#!/bin/bash

current_position=$(pwd)
docker exec -i mongo_instance_1 mongoimport --db nosql --collection usersCollection --drop --jsonArray < "$current_position/json/users.json" 
```
nous allons utiliser la commande suivante qui est le script shell précèdent :

```shell
./importmongo.sh
```
<img width="783" alt="Capture d’écran 2024-04-17 à 21 13 09" src="https://github.com/feur25/no-sql-package/assets/39668417/8b3edff1-2437-4970-bbb6-f20d50f0636e">

### Les commandes MongoDB Cli
Nous passons enfin au commandes mongoDB rassurer vous après nous verrons et utiliserons un script pour opti c'est commande :

	```shell
	docker exec -it mongo_instance_1 mongosh
	```
<img width="783" alt="Capture d’écran 2024-04-17 à 21 14 51" src="https://github.com/feur25/no-sql-package/assets/39668417/5de02f01-3218-49bc-89ca-8a8c918c29d2">

Ensuite, nous arrivons sur la Cli mais nous ne serons pas encore sur la bonne database, pour cela nous allons utiliser la commande suivante :

	```shell
	use nosql
	```
<img width="297" alt="Capture d’écran 2024-04-17 à 21 15 47" src="https://github.com/feur25/no-sql-package/assets/39668417/410cb53d-a2d5-49a7-9235-2a9c48c80a1b">
pour information nosql a été définie dans notre docker compose : 
<img width="598" alt="Capture d’écran 2024-04-17 à 21 16 35" src="https://github.com/feur25/no-sql-package/assets/39668417/aa488e4d-2f75-4878-ab2b-2cc754f52392">



#### Commandes
Cette étapes n'est pas obligatoire, elle est la plus pour vous familliariser avec mogoDB

Insertion de données :
	```shell
	db.usersCollection.insertOne({
	"name": "Coletta-Chambon Quentin", 
	"age" : 24, 
	"email" : "feur09@gmail.com", 
	"createdAt": new Date()
	})
	```
 <img width="450" alt="Capture d’écran 2024-04-17 à 21 18 40" src="https://github.com/feur25/no-sql-package/assets/39668417/83dde131-1998-47d5-ae7e-495577393653">



nous afficheron les données via un filtre :

	```shell
	db.usersCollection.find({ "age": { "$gt": 30 } })
	```
<img width="579" alt="Capture d’écran 2024-04-17 à 21 20 19" src="https://github.com/feur25/no-sql-package/assets/39668417/01c17676-3ce7-44d5-ae1c-96edd24f8a05">

Augmentation d'une données :

	```shell
	db.usersCollection.updateMany({}, { "$inc": { "age": 5 } })
	```
<img width="638" alt="Capture d’écran 2024-04-17 à 21 21 38" src="https://github.com/feur25/no-sql-package/assets/39668417/94ab9770-060b-41ba-8e03-c92bbe019b4c">


Suppression de données :

	```shell
	db.usersCollection.deleteOne({ "name": "Coletta-Chambon Quentin" })}
	```
<img width="688" alt="Capture d’écran 2024-04-17 à 21 22 59" src="https://github.com/feur25/no-sql-package/assets/39668417/80ab83e8-089f-4d26-927a-3c06639925a4">



### Exécution du script CRUD (Python)
Nous passons a l'étape de l'optimisation, et des commandes disponibles, qui va refaire un peut tous ce que nous avons vue précédament, mais de manière plus intuitive, et sympatique :

Nous utiliserons le script MongoDBOperations.py

celui-ci est composer de diverse function et paramètre dans votre commande :
--method (sélection de la méthode employé) :
	- create (crée un utilisateur avec un nom, age et email)
 	- delete (supprimer un user via sont nom)
  	- modify (modifier l'age ou l'email, d'un user via sont nom)
   	- filter (trouver des users via un filtre, nom, age ou email)
    
voici des exemples des commandes :

	python3 ./CRUD/MongoDBOperations.py --method create --name "quentin" --age 88 --email "quentin.coletta@ynov.com"

<img width="779" alt="Capture d’écran 2024-04-17 à 21 30 42" src="https://github.com/feur25/no-sql-package/assets/39668417/8d05150f-1304-4282-ae85-e2797b2c2380">

Nous allons rechercher notre nouveau user dans notre mongoDB :

	db.usersCollection.find({ "name": "quentin"  })
 
<img width="570" alt="Capture d’écran 2024-04-17 à 21 33 43" src="https://github.com/feur25/no-sql-package/assets/39668417/892dec56-94cf-40ab-9c6d-d9347307d891">

Maintenant via la function filter de notre script python :

	python3 ./CRUD/MongoDBOperations.py --method filter --name "quentin"
 
<img width="791" alt="Capture d’écran 2024-04-17 à 21 35 27" src="https://github.com/feur25/no-sql-package/assets/39668417/abcc380c-8771-4cf3-a72f-7bde2c8b762c">

Magic n'es pas ! bon bien sur la j'ai applisquer qu'un seul filtre, un seul paramètre le nom, mais ont pouvais le chercher via sont email, ou l'age, ou encore les trois en même temp, là nous avons fait au plus simple pour l'exemple mais n'hésiter pas à tester.

Continuons sur notre lancer et modifier cette utilisateur "quentin" le nom étant unique, pour modifier l'user le paramètre --name est obligatoir !

	python3 ./CRUD/MongoDBOperations.py --method modify --name "quentin" --age 15 --email "test@gmail.com"
 
<img width="791" alt="Capture d’écran 2024-04-17 à 21 39 10" src="https://github.com/feur25/no-sql-package/assets/39668417/4ddb2bf6-7e77-4553-b70b-432349f2d776">

Notre utilisateur à bien changer !

Pour finir passons à la méthode "delete" pour supprimer notre utilisateur, idem ctte fois-ci le paramètre --name est obligatoire, c'est ce qui va nous permettre de trouver notre utilisateur :

	python3 ./CRUD/MongoDBOperations.py --method delete --name "quentin"
<img width="791" alt="Capture d’écran 2024-04-17 à 21 42 38" src="https://github.com/feur25/no-sql-package/assets/39668417/f4aeb77c-8912-4de4-8789-72acc046a849">

Voici comment ce fini ce tp, j'espère que vous avez apprésiez n'hésiter pas à vous ballader dans les script, c'est dernier sont commenter via des docstrings, deso pour les fautes d'orthographes.







## MongoDB Replica Set

### Démarrage du Replica Set (Docker)

La première étape consiste à créer un réseau docker (Cluster) pour cela nous allons utiliser la commande ci-dessous.

  docker network create nosqlMongoCluster

Ensuite, pour la deuxième étape nous allons executer le docker compose pour démarrer les trois instances. 

  docker compose up -d

Enfin, nous allons exécuter la commande ci-dessous, dans le MongoDB Cli il faudra exécuter cette commande pour permettre de créer le jeu de réplica réel entre les différentes instances.

  docker exec -it mongo_instance_1 mongosh --eval "rs.initiate({
 _id: \"nosql\",
 members: [
   {_id: 0, host: \"mongo_instance_1\"},
   {_id: 1, host: \"mongo_instance_2\"},
   {_id: 2, host: \"mongo_instance_3\"}
 ]
})"

Nous pouvons ensuite grâce à la commande suivante, voir les différentes instances, cela nous permettra de vérifier le replica sur les machines.

docker exec -it mongo_instance_1 mongosh --eval "rs.status()"


Par la suite, nous allons générer les fausses données utilisateurs et les stocker dans un fichier users.json avec la structure de données suivantes.

 {
  _id: new ObjectId('661d0f6a9eac75371bab12d1'),
  name: 'Ms. Blanca Krajcik',
  age: 78,
  email: 'Trey37@hotmail.com',
  createAt: '2024-01-12T05:17:50.007Z'
}

### Génération et Manipulation de fausses données

Une fois nos 100 utilisateurs créer, nous allons ensuite insérer nos données à travers la CLI de MongoDB.

```shell
#!/bin/bash

current_position=$(pwd)
docker exec -i mongo_instance_1 mongoimport --db nosql --collection usersCollection --drop --jsonArray < "$current_position/json/users.json" 
```

Tout simplement nous allons faire un fichier importmongo.sh, il suffira juste de l'exécuter avec la commande suivante.

```shell
./importmongo.sh
```

Voici les résultats que nous obtenons lors de l'exécution de la commande, nous avons bien nos 100 users qui viennent d'être insérer.

```shell
connected to: mongodb://localhost/
dropping: nosql.usersCollection
100 document(s) imported successfully. 0 document(s) failed to import.
```

### Les commandes MongoDB Cli et leurs résultats

Il va falloir accéder au Cli de MongoDB et pour cela nous allons exécuter la commande suivante.

```shell
docker exec -it mongo_instance_1 mongosh
```

Ensuite, nous arrivons sur la Cli mais nous ne serons pas encore sur la bonne database, pour cela nous allons utiliser la commande suivante.

```shell
use nosql
```

#### Commandes

Insertion de données :
```shell
db.usersCollection.insertOne({
"name": "Coletta-Chambon Quentin", 
"age" : 24, 
"email" : "feur09@gmail.com", 
"createdAt": new Date()
})
```

Résultat :

```shell
{
	"acknowledged" : true,
	"insertedId" : ObjectId("660d37841a29f180e7094ac4")
}
```

Affichage de données :

```shell
db.usersCollection.find({ "age": { "$gt": 30 } })
```

Augmentation d'une données :

```shell
db.usersCollection.updateMany({}, { "$inc": { "age": 5 } })
```

Résultat

```shell
{ 
  "acknowledged" : true, "matchedCount" : 100, "modifiedCount" : 100 
}
```

Suppression de données :

```shell
db.usersCollection.deleteOne({ "name": "Coletta-Chambon Quentin" })}
```

Résultat :

```shell
{ "acknowledged" : true, "deletedCount" : 1 }
```

### Exécution du script CRUD (Python)

from pymongo import MongoClient
import datetime
import argparse

class MongoDBOperations :
    """
    A class to represent a person.

    Methods
    -------
    - defaultValue(name, age, email)
        * Returns the default value of name, age, and email if not provided.

    - __init__(host='localhost', port=27017)
        * Constructs an instance with given host and port.

    - connect()
        * Connects to the database server.

    - create(name, age, email)
        * Inserts a new document into the specified collection.

    - filter(name=None, age=None, email=None)
        * Retrieves users in the specified collection based on the age or email filter.

    - modify(name, age, email)
        * Updates existing user in the specified collection based on the name.

    - delete(name)
        * Delete user in the specified collection based on the name.
        
    - close_connection()
        * Closes the connection to the database server.
    """


    def __init__(self) :
        self.uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.4"
        self.client = MongoClient(self.uri)
        self.database = self.client["nosql"]
        self.users_collection = self.database["usersCollection"]

    def defaultValue(self, name, age, email) :
        ''' 
        Set default values for name, age, and email if not provided. 

        - Parameters :
            * name : str : Name of the user
            * age : int : Age of the user
            * email : str : Email of the user

        - Return :
            * name, age, email : str, int, str : Name, age, and email of the user with their respective values
        '''
        if name is None or name == "":
            name = "Unknown"
        if age is None or age == "":
            age = 0
        if email is None or email == "":
            email = "unknown@example.com"
        return name, age, email
    
    def create(self, name, age, email) :
        ''' 
        Create a new user in the database. 

        - Parameters :
            * name : str : Name of the user
            * age : int : Age of the user
            * email : str : Email of the user

        - Returns :
            * result : bool : True if successful else False
        '''
        name, age, email = self.defaultValue(name, age, email)
            
        user = {
            "name": name,
            "age": age,
            "email": email,
            "createdAt": str(datetime.datetime.now())
        }

        if self.users_collection.find_one({"name": name}):
            print("Name already exists in the database.")
            return
        
        try:
            result = self.users_collection.insert_one(user)
            print(f"A document was inserted with the _id: {result.inserted_id}")
        except Exception as e:
            print(f"An error occurred while inserting document: {e}")
        
    def delete(self, name) :
        ''' 
        Delete a user from the database. 
        
        - Parameters :
            * name : str : Name of the user to delete
        '''
        result = self.users_collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"User '{name}' deleted successfully.")
        else:
            print(f"User '{name}' not found in the database.")

    def modify(self, name, age, email) :
        ''' 
        Modify an existing user in the database. 
        
        - Parameters :
            * name : str : Name of the user to modify
            * age : int : Age of the user
            * email : str : Email of the user
        '''
        user = self.users_collection.find_one({"name": name})
        if user:
            if age:
                user["age"] = age
            if email:
                user["email"] = email
            try:
                result = self.users_collection.update_one({"_id": user["_id"]}, {"$set": user})
                if result.modified_count > 0:
                    print(f"User '{name}' modified successfully.")
                else:
                    print(f"No changes made to user '{name}'.")
            except Exception as e:
                print(f"An error occurred while modifying user: {e}")
            else:
                print(f"User '{name}' not found in the database.")

    def filter(self, name=None, age=None, email=None) :
        ''' 
        Filter users based on the provided criteria. 
        
        - Parameters :
            * name : str : Name of the user
            * age : int : Age of the user
            * email : str : Email of the user
        '''
        query = {}
        if name:
            query["name"] = name
        if age:
            query["age"] = age
        if email:
            query["email"] = email
        
        try:
            results = self.users_collection.find(query)
            for result in results:
                print(result)
        except Exception as e:
            print(f"An error occurred while filtering users: {e}")

    def close_connection(self) :
        ''' Close the connection to the MongoDB server. '''
        self.client.close()

    def choose_function(self, method, name, age, email) :
        '''
        Dispatch function calls to appropriate methods based on the method specified. 
        
        - Parameters :
            * method : str : Method to call
            * name : str : Name of the user
            * age : int : Age of the user
            * email : str : Email of the user
        '''
        if method == "create":
            self.create(name, age, email)
        elif method == "delete":
            self.delete(name)
        elif method == "modify":
            self.modify(name, age, email)
        elif method == "filter":
            self.filter(name, age, email)
        else:
            print("Invalid method specified.")

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='Manage users in MongoDB')
    parser.add_argument("--method", required=True, help='Function use')
    parser.add_argument('--name', required=False, help='User name')
    parser.add_argument('--age', required=False, help='User age')
    parser.add_argument('--email', required=False, help='User email')

    args = parser.parse_args()

    mongo_ops = MongoDBOperations()
    mongo_ops.choose_function(args.method, args.name, args.age, args.email)

    mongo_ops.close_connection()
import json
import random
import faker
from datetime import datetime
import os

class UserGenerator:
    '''
    A class to generate random users and write them to a JSON file. 
    
    Attributes : 
    -------
        - num_users (int): The number of users to generate. Default is 100.
        - filename (str): The name of the output JSON file. Default is 'users.json'.
        
    Methods :  
    -------
        - __init__(): Initializes the UserGenerator class.
        - create_user(self, fake): Generates a random user.
            * Parameters : 
                + fake (Faker object) : A Faker object to generate random data.
            * Returns :  
                + dict : A dictionary representing a user.
                          Example : {'name' : 'John Doe', 'age' : 25, 'email' : 'john.doe@example.com'}
        - generate_users(self): Creates a list of random users.
            * Calls the create_user method to generate a list of users.
            * Writes this list as a JSON file.
            
    Usage example :  
        ug = UserGenerator() # Create an instance of the UserGenerator class.
        ug.generate_users() # Generate a list of 100 users and write them to a JSON file.
    '''
    def __init__(self):
        self.fake = faker.Faker()

    def generate_users(self, num_users):
        '''
        Generate a list of users with random names, ages, emails and creation dates.
        
        - Paramaters : 
            * num_users (int) : The number of users to generate.
            
        - Returns :
            * users (list) : A list of dictionaries, each dictionary representing a user.
        '''
        users = []
        for _ in range(num_users):
            user = {
                "name": self.fake.name(),
                "age": random.randint(18, 90),
                "email": self.fake.email(),
                "createdAt": self.fake.date_time_between(start_date='-5y', end_date='now').isoformat()
            }
            users.append(user)
        return users

    def write_users_to_json(self, num_users, output_file):
        '''
        Write the generated users to a JSON file.
        
        - Parameters :
            * num_users (int) : The number of users to generate.
            * output_file (str) : The path to the output JSON file.

        If no extension is provided, '.json' will be appended.
        '''
        users = self.generate_users(num_users)
        with open(output_file, 'w') as file:
            json.dump(users, file, indent=2)
        print(f"Le fichier {output_file} a été créé avec succès.")

if __name__ == "__main__":
    generator = UserGenerator()
    num_users = 100
    current_path = os.path.dirname(os.path.abspath(__file__))
    output_file = '{current_path}/json/users.json'
    generator.write_users_to_json(num_users, output_file)

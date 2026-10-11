import os 
import random 
import signal 
import time 

from simulator.src.repositories.user_repository import UserRepository
from simulator.src.repositories.post_repository import PostRepository
from simulator.src.factories.user_factory import UserFactory
from simulator.src.factories.post_factory import PostFactory
from simulator.src.db import Connect
# TODO: add activity events factory 


#####################################################################################
# Simulator - class that is meant to simulate the real user activity
#####################################################################################

class Simulator:
    def __init__(self, users : UserRepository, posts: PostRepository):
        self.users = users
        self.posts = posts
        self.running = True

    def stop(self, *_):
        self.running = False
    
    def choose_operation(self, user_count : int) -> str:
        """
        choose operation to be executed
        based on the weight of each operation
        args: 
            user_count : int 
        return:
            string : name of the operation
        """
        if (user_count < 50):
            return "insert_user"
        fill = user_count / MAX_USERS
        weights = {
            "insert_user"       : 0.10 * (1 - fill),
            "delete_user"       : 0.02 * fill,
            "update_user"       : 0.10,
            "insert_post"       : 0.25,
            "update_post"       : 0.10,
            "delete_post"       : 0.15,
            "activity_event"    : 0.40,
        }
        return random.choice(list(weights), weights=list(weights.values()))[0]

    def execute(self, operation: str) -> None:
        """
        match the passed operation string
        with the corresponding function
        args:
            operation : str
        return:
            None
        """
        match(operation):
            case "insert_user":
                self.insert_user()
            case "delete_user":
                self.delete_user()
            case "update_user":
                self.update_user()
            case "insert_post":
                self.insert_post()
            case "update_post":
                self.update_post()
            case "delete_post":
                self.delete_post()
            case "activity_event":
                self.activity_event()
            case _:
                print("Warning: Wrong operation type")

    def run(self):
        """
        check running condition 
        run a random operation while true
        sleep
        """
        while self.running:
            user_count = self.users.count()
            operation = self.choose_operation(user_count)
            self.execute(operation)
            time.sleep(random.expovariate(RATE))


    def insert_user(self) -> None:
        """
        Insert a user created by factory function
        into the database
        """
        self.users.insert(UserFactory.create())

    def delete_user(self) -> None:
        """
        get a random user id from db
        delete the user with that id from db
        """
        user_id = self.users.random_id()
        self.users.delete(user_id)

    def update_user(self) -> None:
        pass

    def insert_post(self) -> None:
        """
        Insert a post created by factory function
        into the database
        """
        self.posts.insert(PostFactory.create())

    def update_post(self) -> None:
        pass

    def delete_post(self) -> None:
        """
        get a random post id from db
        delete the post with that id from db 
        """
        post_id = self.posts.random_id()
        self.posts.delete(post_id)

    def activity_event(self) -> None:
        pass
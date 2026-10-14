import os 
import random 
import signal 
import time
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import config
from factories.post_factory import PostFactory
from factories.user_factory import UserFactory
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository

log = logging.getLogger("simulator")

USER_UPDATEABLE_FIELDS = ("u_email", "u_phone", "u_city", "u_last_name")

#####################################################################################
# Simulator - class that is meant to simulate the real user activity
#####################################################################################

class Simulator:

    _running = False

    @classmethod
    def start(cls) -> None:
        signal.signal(signal.SIGTERM, cls.stop)
        signal.signal(signal.SIGINT, cls.stop)

        engine = create_engine(config.DATABASE_URL, pool_pre_ping=True)
        session = Session(engine)

        try:
            cls()._run(session)
        finally:
            session.close()
            engine.dispose()
            log.info("Simulator stopped, connection closed")

    
    @classmethod
    def stop(cls, *_) -> None:
        if csl._running:
            log.info("Stop requested, finishing current operation.")
        _running=False


    def run(self, session: Session) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.posts = PostRepository(session)

        Simulator._running = True
        log.info("Simulator started: ~%.1f ops/sec, max %d users", config.EVENTS_PER_SEC, config.MAX_USERS)

        while Simulator._running:
            operation = None;
            try:
                operation = choose_operation(self.users.count())
                self._execute(operation)
            except SQLAlchemyError as e:
                self.session.rollback()
                reason = str(getattr(e, "orig", e)).splitlines()[0]
                log.warning("%s failed: %s", operation, reason)
            time.sleep(random.expovariate(config.EVENTs_PER_SEC))

    
    def choose_operation(self, user_count : int) -> str:
        if (user_count < config.MAX_USERS):
            return "insert_user"
        fill = min(user_count / config.MAX_USERS, 1.0)
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

    def _execute(self, operation: str) -> None:
        match(operation):
            case "insert_user":
                self._insert_user()
            case "delete_user":
                self._delete_user()
            case "update_user":
                self._update_user()
            case "insert_post":
                self._insert_post()
            case "update_post":
                self._update_post()
            case "delete_post":
                self._delete_post()
            case "activity_event":
                self._activity_event()
            case _:
                log.warning("Unknown operation type: %s", operation)


    def _insert_user(self) -> None:
        user_id = self.users.insert(UserFactory.create())
        log.info("insert_user -> %s", user_id if User_id else "skipped (duplicate)")

    def _delete_user(self) -> None:
        user_id = self.users.random_id()
        if user_id is not None:
            self.users.delete(user_id)
            log_info("delete_user -> %s", user_id)

    def _update_user(self) -> None:
        user_id = self.users.random_id()
        if user_id is None:
            return 
        field = random.choice(USER_UPDATABLE_FIELDS)
        value = UserFactory.create()[field]
        self.users.update(user_id, **{field: value})
        log.info("update_user -> %s.%s", user_id, field)

    def _insert_post(self) -> None:
        user_id = self.users.random_id()
        if user_id is not None:
            post_id = self.posts.insert(PostFactory.create([user_id]))
            log.info("insert_post -> %s (user %s)", post_id, user_id)

    def _update_post(self) -> None:
        post_id = self.posts.random_id()
        if post_id is None:
            return 
        field = random.choice(("title", "content"))
        value = PostFactory.create([None])[field]
        self.posts.update(post_id, **{field: value})
        log.info("update_post -> %s.%s", post_id, field)

    def _delete_post(self) -> None:
        post_id = self.posts.random_id()
        if post_id is not None:
            self.posts.delete(post_id)
            log.info("delete_post -> %s", post_id)

    def _activity_event(self) -> None:
        pass


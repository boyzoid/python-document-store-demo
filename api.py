import os
import falcon
import json
import mysqlx
from dotenv import load_dotenv

load_dotenv()


class DbDocListJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "as_str"):
            return dict(o)
        return json.JSONEncoder.default(self, o)


class MysqlConnector():
    def __init__(self):
        self.db_name = os.getenv('DB_NAME')
        self.coll_name = os.getenv('COLLECTION_NAME')
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_port = os.getenv("DB_PORT")
        self.db_host = os.getenv("DB_HOST")
        self.connection_url = f"mysqlx://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        self.connection_config = {
            "pooling": {
                "enabled": True,
                "max_size": 10,
                "max_idle_time": 20000,
                "queue_timeout": 5000
            }
        }
        self.pool = mysqlx.get_client(self.connection_url, self.connection_config)

    def list_all(self):
        session = self.pool.get_session()
        db = session.get_schema(self.db_name)
        collection = db.get_collection(self.coll_name)
        scores = (collection
                  .find()
                  .execute()
                  .fetch_all()
                  )
        session.close()
        return json.dumps({"count": len(scores), "scores": scores}, cls=DbDocListJsonEncoder)

    def limit_all(self, limit: int, offset: int = 0):
        session = self.pool.get_session()
        db = session.get_schema(self.db_name)
        collection = db.get_collection(self.coll_name)
        scores = (collection
                  .find()
                  .limit(limit)
                  .offset(offset)
                  .execute()
                  .fetch_all()
                  )
        session.close()
        return json.dumps({"count": len(scores), "scores": scores}, cls=DbDocListJsonEncoder)

    def best_scores(self, limit: int = 25):
        session = self.pool.get_session()
        db = session.get_schema(self.db_name)
        collection = db.get_collection(self.coll_name)
        scores = (collection
                  .find()
                  .fields(
            [
                "firstName",
                "lastName",
                "score",
                "course",
                "`date` as datePlayed"
            ]
        )
                  .sort(['score asc', '`date` desc'])
                  .limit(limit)
                  .execute()
                  .fetch_all()
                  )
        session.close()
        return json.dumps({"count": len(scores), "scores": scores}, cls=DbDocListJsonEncoder)


mysql_db = MysqlConnector()
api = falcon.App()


class AppRoot(object):
    result = {"message": "Python Demo main endpoint"}

    def on_get(self, req, resp):
        resp.text = json.dumps(self.result)


class ListAllScores(object):
    def on_get(self, req, resp):
        resp.text = mysql_db.list_all()


class LimitAllScores(object):
    def on_get(self, req, resp, limit, offset=0):
        resp.text = mysql_db.limit_all(limit, offset)


class GetBestScores(object):
    def on_get(self, req, resp, limit=10):
        resp.text = mysql_db.best_scores(limit)


api.add_route("/", AppRoot())

api.add_route("/list", ListAllScores())

api.add_route("/list/{limit:int}", LimitAllScores())
api.add_route("/list/{limit:int}/{offset:int}", LimitAllScores())

api.add_route("/bestScores/", GetBestScores())
api.add_route("/bestScores/{limit:int}", GetBestScores())

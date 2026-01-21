import unittest
import json
from app import create_app, db
from app.models.models import School, Student
from config import config_map

OFF_NUMBER = 100

class BaseTest(unittest.TestCase):
    def setUp(self):

        self.app = create_app(config_map.get("testing"))
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

            school1 = School(id=1, name="Escola Gracia", capacity=2)
            school2 = School(id=2, name="Escola Eixample", capacity=100)
            db.session.add_all([school1, school2])
            
            student1 = Student(id="ST-000001",
                              first_name="Jordi",
                              last_name="Pujol",
                              school_id=1,
                              )
            student2 = Student(id="ST-000002",
                              first_name="Maria",
                              last_name="Doblas",
                              school_id=1,
                              )
            db.session.add_all([student1, student2])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

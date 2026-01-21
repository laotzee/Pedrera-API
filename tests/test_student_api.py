from .base import BaseTest, db, OFF_NUMBER, Student, School

class TestStudentAPI(BaseTest):

    def test_create_student_incomplete(self):
        """Test that adding a student fails when the data is incomplete"""
        payload = {
            "first_name": "Maria",
            "last_name": "Vila",
        }
        response = self.client.post('/students', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_data(as_text=True))

    def test_create_student_nonexistent_school(self):
        """
        Test that adding a student fails when its school does not exist in
        the database
        """
        with self.app.app_context():
            schools = db.session.execute(db.select(School)).scalars().all()

        out_of_range = len(schools) + OFF_NUMBER
        
        payload = {
            "id": "ST-000003",
            "first_name": "Maria",
            "last_name": "Vila",
            "school_id": out_of_range
        }
        response = self.client.post('/students', json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_data(as_text=True))

    def test_create_student_success(self):
        """Test adding a student successfully"""
        with self.app.app_context():
            school = db.session.execute(db.select(School).where(School.name == "Escola Eixample")).scalar_one()
            school_id = school.id

        payload = {
            "id": "ST-000003",
            "first_name": "Maria",
            "last_name": "Vila",
            "school_id": school_id
        }
        response = self.client.post('/students', json=payload)
        self.assertEqual(response.status_code, 201)

    def test_create_student_capacity_error(self):
        """
        Test that adding a student fails if school is at its max capacity
        """
        with self.app.app_context():
            school = db.session.execute(
                    db.select(School).where(School.name == "Escola Gracia"
                                            )).scalar_one()
            school_id = school.id

        payload = {
            "id": "ST-FAIL00",
            "first_name": "Overflow",
            "last_name": "User",
            "school_id": school_id
        }
        response = self.client.post('/students', json=payload)
        
        self.assertEqual(response.status_code, 403)
        self.assertIn("error", response.get_data(as_text=True))

    def test_create_student_already_exist(self):
        """Test that adding a student fails if it already exist"""
        with self.app.app_context():
            student = db.session.get(Student, "ST-000001")

        response = self.client.post('/students', json={
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "school_id": 2,
        })

        self.assertEqual(response.status_code, 409)
        self.assertIn("error", response.get_data(as_text=True))

    def test_delete_student_success(self):
        """Test deleting a student successfully"""
        response = self.client.delete('/students/ST-000001')
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_data(as_text=True))

        response = self.client.get('/students/ST-000001')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_data(as_text=True))

    def test_delete_student_by_nonexistent_id(self):
        """Test deleting a student fails when it is not found"""
        with self.app.app_context():
            stmt =  db.select(Student)
            students = db.session.execute(stmt).scalars().all()
        out_of_range = len(students) + OFF_NUMBER

        response = self.client.delete('/students/ST-00000{OFF_NUMBER}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_data(as_text=True))

    def test_get_students(self):
        """Test retrieving list of all students"""

        with self.app.app_context():
            stmt = db.select(Student)
            students = db.session.execute(stmt).scalars().all()
        total = len(students)

        response = self.client.get('/students')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), total)
        self.assertEqual(data[0]['first_name'], "Jordi")
        self.assertEqual(data[1]['first_name'], "Maria")

    def test_get_student_by_id_success(self):
        """Test retrieving a specific student by ID successfully"""
        response = self.client.get('/students/ST-000001')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['last_name'], "Pujol")

    def test_get_student_by_id_nonexistent(self):
        """Test getting a student fails when it does not exist"""
        with self.app.app_context():
            stmt = db.select(Student)
            students = db.session.execute(stmt).scalars().all()
        out_of_range = len(students) + OFF_NUMBER
        response = self.client.get(f'/students/{out_of_range}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_data(as_text=True))

    def test_search_student_sucess(self):
        """
        Test searching student by string in first name or last name successfully
        """
        response = self.client.get('/students/search?query=Pujo')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

        response = self.client.get('/students/search?query=Jor')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_search_student(self):
        """
        Test searching student by string in first name or last name successfully
        """
        response = self.client.get('/students/search')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()


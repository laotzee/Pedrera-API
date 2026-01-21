from .base import BaseTest, db, Student, School

class TestSchoolAPI(BaseTest):

    def test_create_school_successful(self):
        """Test creating a new school successfully"""
        payload = {"name": "Escola Nova", "capacity": 50}
        response = self.client.post('/schools', json=payload)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("Escola Nova", response.get_data(as_text=True))

    def test_create_school_incomplete(self):
        """Test creating a new school without complete information"""
        payload = {"name": "Escola Nova"}
        response = self.client.post('/schools', json=payload)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_data(as_text=True))

    def test_create_school_duplicate(self):
        """Test creating a new school causinga duplicate"""
        payload = {"name": "Escola Gracia", "capacity": 2}
        response = self.client.post('/schools', json=payload)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_data(as_text=True))

    def test_delete_school_successful(self):
        """Test deleting a school successfully"""
        with self.app.app_context():
            stmt =  db.select(School).where(School.name == "Escola Gracia")
            school = db.session.execute(stmt).scalar()
            school_id = school.id

        response = self.client.delete(f'/schools/{school_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_data(as_text=True))

        response = self.client.get(f'/schools/{school_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_data(as_text=True))

    def test_delete_school_nonexistent(self):
        """Test deleting a non-existent school"""
        school_id = 58
        response = self.client.delete(f'/schools/{school_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_data(as_text=True))
 
    def test_get_all_schools_is_list(self):
        """Verify the endpoint returns a list of all schools"""
        response = self.client.get('/schools')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_schools_nesting_requirement(self):
        """Verify students are nested inside the school objects"""
        response = self.client.get('/schools')
        data = response.get_json()

        gracia = next(s for s in data if s['name'] == "Escola Gracia")
        
        self.assertIn('students', gracia)
        self.assertIsInstance(gracia['students'], list)
        self.assertEqual(len(gracia['students']), 2)
        self.assertEqual(gracia['students'][0]['first_name'], "Jordi")

    def test_get_school_by_id_successful(self):
        """Test getting a school by id successfully"""
        with self.app.app_context():
            stmt =  db.select(School).where(School.name == "Escola Eixample")
            school = db.session.execute(stmt).scalar()
            school_id = school.id

            response = self.client.get(f'/schools/{school_id}')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(school.id, data["id"])
            self.assertEqual(school.name, data["name"])
            self.assertEqual(school.capacity, data["capacity"])
            self.assertEqual(len(school.students), data["student_count"])
            self.assertEqual(school.students, data["students"])

    def test_get_school_by_nonexistent_id(self):
        """Test getting a school by id successfully"""
        with self.app.app_context():
            stmt =  db.select(School)
            schools = db.session.execute(stmt).scalars().all()
            out_of_range = len(schools) + 50

        response = self.client.get(f'/schools/{out_of_range}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_data(as_text=True))

    def test_search_school_successful(self):
        """Test searching for a school by partial name."""
        response = self.client.get('/schools/search?query=Grac')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Escola Gracia")

    def test_search_school_incomplete(self):
        """
        Test searching for a school by partial name when no arguments are
        given
        """
        response = self.client.get('/schools/search')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()

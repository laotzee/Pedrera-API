from flask import Blueprint, request, jsonify
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from ..models.models import db, School, Student
from .helpers import serialize_school, serialize_student


api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/schools', methods=['POST'])
def create_school():
    """Create a new school"""
    data = request.get_json()
    required_fields = ["name", "capacity"]

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Name and capacity are required"}), 400

    new_school = School(
        name=data['name'],
        capacity=data['capacity']
    )
    
    try:
        db.session.add(new_school)
        db.session.commit()
        school = serialize_school(new_school, include_students=False)
        return jsonify(school), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "School name must be unique"}), 400

@api_blueprint.route('/schools/<int:school_id>', methods=['DELETE'])
def delete_school(school_id):
    """Delete a school given its ID"""
    school = db.session.get(School, school_id)
    if not school:
        return jsonify({"error": "School not found"}), 404
        
    db.session.delete(school)
    db.session.commit()
    return jsonify({"message": "School deleted successfully"}), 200

@api_blueprint.route('/schools', methods=['GET'])
def get_schools():
    """Retrieve all schools with their students"""
    stmt = select(School)
    schools = db.session.execute(stmt).scalars().all()
    
    schools = [serialize_school(s) for s in schools]
    return jsonify(schools), 200

@api_blueprint.route('/schools/<int:school_id>', methods=['GET'])
def get_school_by_id(school_id):
    """Retrieve a specific school and its students"""
    school = db.session.get(School, school_id)
    if not school:
        return jsonify({"error": "School not found"}), 404
        
    school = serialize_school(school)
    return jsonify(school), 200

@api_blueprint.route('/schools/search', methods=['GET'])
def search_schools():
    """Search schools containing a given string in their name"""
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter required"}), 400
        
    stmt = select(School).where(School.name.ilike(f"%{query}%"))
    results = db.session.execute(stmt).scalars().all()
    
    schools = [serialize_school(s, include_students=False) for s in results]
    return jsonify(schools), 200

@api_blueprint.route('/students', methods=['POST'])
def create_student():
    """Create a new student"""
    data = request.get_json()
    
    required_fields = ['id', 'first_name', 'last_name', 'school_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    school = db.session.get(School, data['school_id'])
    if not school:
        return jsonify({"error": "School not found"}), 404
        
    if len(school.students) >= school.capacity:
        return jsonify({"error": "School is at maximum capacity"}), 403

    new_student = Student(
        id=data['id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        school_id=data['school_id']
    )
    
    try:
        db.session.add(new_student)
        db.session.commit()
        student = serialize_student(new_student)
        return jsonify(student), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Student ID already exists"}), 409

@api_blueprint.route('/students/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student given its ID"""
    student = db.session.get(Student, student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
        
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"}), 200

@api_blueprint.route('/students', methods=['GET'])
def get_students():
    """Retrieve all students"""
    stmt = select(Student)
    raw_students = db.session.execute(stmt).scalars().all()

    students = [serialize_student(s) for s in raw_students]
    return jsonify(students), 200

@api_blueprint.route('/students/<string:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    """Retrieve a student given its ID"""
    student = db.session.get(Student, student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
        
    student = serialize_student(student)
    return jsonify(student), 200

@api_blueprint.route('/students/search', methods=['GET'])
def search_students():
    """Search students containing a string in first_name or last_name"""
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter required"}), 400

    stmt = select(Student).where(
        or_(
            Student.first_name.ilike(f"%{query}%"),
            Student.last_name.ilike(f"%{query}%")
        )
    )
    raw_students = db.session.execute(stmt).scalars().all()
    
    students = [serialize_student(s) for s in raw_students]
    return jsonify(students), 200

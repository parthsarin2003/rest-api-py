from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Sample in-memory database (list of dictionaries)
students = []

# Helper function to find a student by ID
def find_student(student_id):
    return next((student for student in students if student["id"] == student_id), None)

# Endpoint to get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

# Endpoint to get a single student by ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = find_student(student_id)
    if student:
        return jsonify(student), 200
    else:
        return jsonify({"error": "Student not found"}), 404

# Endpoint to create a new student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not all(key in data for key in ("id", "name", "age", "email")):
        return jsonify({"error": "Missing student information"}), 400
    
    if find_student(data["id"]):
        return jsonify({"error": "Student with this ID already exists"}), 400
    
    students.append(data)
    return jsonify(data), 201

# Endpoint to update an existing student by ID
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = find_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    data = request.get_json()
    student.update({key: data[key] for key in data if key in student})
    return jsonify(student), 200

# Endpoint to delete a student by ID
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = find_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    students.remove(student)
    return jsonify({"message": "Student deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)

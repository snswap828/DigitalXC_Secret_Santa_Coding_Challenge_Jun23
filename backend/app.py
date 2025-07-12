from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from services.parser import EmployeeParser, PreviousAssignmentParser
from services.santa_assigner import SecretSantaAssigner
import pandas as pd
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/assign', methods=['POST'])
def assign_santa():
    try:
        if 'employee' not in request.files:
            return jsonify({"success": False, "error": "No employee file provided"}), 400
            
        emp_file = request.files['employee']
        if 'previous' not in request.files:
            return jsonify({"success": False, "error": "No previous assignment file provided"}), 400
        prev_file = request.files['previous']
        if not emp_file or not prev_file:
            return jsonify({"success": False, "error": "Both employee and previous files are required"}), 400
        # Save the uploaded files to temporary files
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp1, tempfile.NamedTemporaryFile(delete=False) as tmp2:
            tmp1_name = tmp1.name
            emp_file.save(tmp1_name)

            tmp2_name = tmp2.name
            prev_file.save(tmp2_name)
            
            try:
                employees = EmployeeParser.parse(tmp1_name)
                previous = PreviousAssignmentParser.parse(tmp2_name)
                assigner = SecretSantaAssigner(employees,previous)
                result = assigner.assign_secret_children()
                
                result_data = [{
                    "Employee_Name": e.name,
                    "Employee_EmailID": e.email,
                    "Secret_Child_Name": e.secret_child.name,
                    "Secret_Child_EmailID": e.secret_child.email
                } for e in result]
                
                # Create response with requested format
                response = {
                    "data": result_data,
                    "success": True
                }
                return jsonify(response)
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
            finally:
                # Clean up temp files
                if os.path.exists(tmp1_name):
                    os.unlink(tmp1_name)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import shelve

app = Flask(__name__)

def open_db(module):
    return shelve.open(module, writeback=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST', 'GET'])
def add_students():
    if request.method == 'POST':
        number = request.form['number']
        title = request.form['title']
        forename = request.form['forename']
        surname = request.form['surname']
        module = request.form['module']
        coursemark = request.form['coursemark']
        exammark = request.form['exammark']

        with shelve.open(module, writeback=True) as db:
            print(f"Adding student to module: {module}")  # Debug print
            if number in db:
                return f"Student {number} already exists in module {module}"
            db[number] = {
                "number": number,
                "module": module,
                "title": title,
                "forename": forename,
                "surname": surname,
                "coursemark": int(coursemark),
                "exammark": int(exammark)
            }
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/update', methods=['POST', 'GET'])
def update_students():
    if request.method == 'POST':
        step= request.form.get('step')
        if step=='lookup':
            number = request.form['number']
            module = request.form['module']

            with shelve.open(module, writeback=True) as db:
                if number in db and db[number]['module'] == module:
                    student = db[number]
                    return render_template('update.html',student=student, step='edit')
                else:
                    return render_template('update.html', error =f"Student{number} not found in module{module}", step='lookup')
        elif step=='edit':
                number = request.form['number']
                module = request.form['module']       
                title = request.form['title']
                forename = request.form['forename']
                surname = request.form['surname']
                coursemark = request.form['coursemark']
                exammark = request.form['exammark']

                with shelve.open(module, writeback=True) as db:
                    if number in db:
                        db[number]={
                        "number": number,
                        "module": module,
                        "title": title,
                        "forename": forename,
                        "surname": surname,
                        "coursemark": int(coursemark),
                        "exammark": int(exammark)

                        }

                return redirect(url_for('index'))
      
    return render_template('update.html', step='lookup')

@app.route('/delete', methods=['GET', 'POST'])
def delete_student():
    if request.method == 'POST':
        # Retrieve student number and module from the form
        number = request.form['number']
        module = request.form['module']
        
        # Open the database for the specified module
        with shelve.open(module, writeback=True) as db:
            # Check if the student exists in the database
            if number in db and db[number]['module'] == module:
                student = db[number]
                del db[number]  
                # Render the update form with the student's existing details
                return render_template('update.html', student=student, number=number, module=module)
            else:
                return f"Student {number} not found in module {module}", 404

    return render_template('find_student.html')

@app.route('/display', methods=['POST', 'GET'])
def display_students():
    if request.method == 'POST':
        # Get the module from the form
        module = request.form.get('module')

        if not module:
            return render_template('display_form.html', error='Module cannot be empty')

        students = []
        try:
            # Open the shelve database for the module
            with shelve.open(module, writeback=True) as db:
                print(f"Opening module database: {module}")  # Debug print
                # Iterate through all records in the database
                for student_number in db:
                    student = db[student_number]
                    # Ensure we are matching the correct module
                    if isinstance(student, dict) and student.get('module') == module:
                        print(f"Student found: {student}")  # Debug print
                        students.append(student)

        except Exception as e:
            print(f"Error opening DB: {e}")  # Debug print for errors
            return f"Error opening DB: {e}"

        if students:
            return render_template('display.html', students=students, module=module)
        else:
            return render_template('display.html', error=f"No students found in module {module}")
    
    return render_template('display_form.html')
#test
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0', port=5001)
#Test
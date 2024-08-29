from flask import Flask, render_template, request, Response
from lxml import etree
import csv

app = Flask(__name__)

# Create a parser to parse the xml data
def get_parser():
    parser = etree.XMLParser(
        load_dtd=True,
        resolve_entities=True,
        no_network=False
    )
    return parser

# Load student data from a CSV file
def load_students():
    students = []
    with open('students.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append(row)
    return students

# Search for a student by name
def find_student(name):
    students = load_students()
    for student in students:
        if student['name'].lower() == name.lower():
            return student
    return None

# Redact sensitive information
def redact_info(student):
    if student:
        student['email'] = '[REDACTED]'
        student['address'] = '[REDACTED]'
        student['grades'] = '[REDACTED]'
    return student

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    try: 
        parser = get_parser()
        tree = etree.fromstring(request.data, parser)
        name = tree.findtext('name').lower()
    except Exception as e:
        print(e)
        pass

    student = find_student(name)
    
    if student is None: 
        return render_template('404.html', error_message=f'{name} not found in database. Please check the name and try again.')

    redacted_student = redact_info(student)

    return render_template('result.html', student=redacted_student)

if __name__ == '__main__':
    app.run()

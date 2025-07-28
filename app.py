from flask import Flask, render_template, request, redirect
import pandas as pd
import os
import openpyxl
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from flask import session, url_for, flash




app = Flask(__name__)

app.secret_key = '563596d88700bb183fbd9bc6b87c37ca'  # Needed for session management


EXCEL_PATH = r"C:\Users\Dell\Documents\FacultyData.xlsx"

FACULTY_SHEET = 'faculty'
COURSE_SHEET = 'courses'
CAPACITY_SHEET = 'ClassroomCapacity'


AREA_LIST = sorted([
    'Amonora','Aundh','Aundh And PCMC','Aundh and PCMC','Aundh and FC','Baner','Bavdhan','BT Kawade','BT Kawade road','FC','FC and Kothrud' ,'FC and Lloyds','Hadapsar','Hadapsar and Lloyds','Hinjewadi','Karve Nagar','Khadhi','Kothrud','Lloyds','Lloyds and Swargate','Magarpatta','Mundwa','NIBM road','Pashan','PCMC','PS','Shivajinagar','Sopan Baug','Vishrant Wadi,'
])
ZONE_LIST = sorted(['Aundh-PCMC-PS', 'FC-Kothrud-Katraj', 'Lloyds-Hadapsar'])
BATCH_LIST = sorted([
    'Foundation BASIC', 'Foundation ADVANCED', 'FOUNDATION ADAVANCED PLUS',
    'Foundation Accelerated', 'FOUNDATION SUMMER', 'Pre-Foundation Basic',
    'Pre - Foundation Advanced', 'PRE - FOUNDATION SUMMER'
])
DAY_LIST = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
COURSE_OPTIONS = [
    "A26 Aundh Offline Champions (Wed 5:30 pm to 8:50 pm Sun 7:00 am to 10:20 am) [1st Floor classroom 1]",
    "A26 Aundh Offline COC (Tue 5:30 pm to 8:50 pm Fri 5:30 pm to 8:50 pm) [1st Floor classroom 2]",
    "A26 Aundh Offline Wizards (Thu 5:30 pm to 8:50 pm Sun 11:00 am to 2:20 pm) [2nd Floor Big]"
    "A26 Aundh Synergy COC + Champions (Wed 5:30 pm to 8:50 pm Sat 5:30 to 8:50 pm) [2nd Floor Big]"
    "A26 Completely Online Champions (Sat 6:00 pm to 9:20 pm Sun 6:00 pm to 9:20 pm)",
    "A26 Completely Online COC - 1 (Fri 6:00 pm to 9:20 pm Sun 6:00 pm to 9:20 pm)",
    "A26 Completely Online COC - 2 (Fri 6:00 pm to 9:20 pm Sun 6:00 pm to 9:20 pm)",
    "A26 Completely Online Wizards (Thu 6:00 pm to 9:20 pm Sun 11:00 to 2:20 pm)",
    "A26 FC Road Synergy COC + Champions (Tue 6:00 pm to 9:20 pm Fri 6:00 pm to 9:20 pm) [GC Mid]",
    "A26 FC Road Synergy Wizards (Thu 6:00 pm to 9:20 pm Sun 11:00 am to 2:20 pm) [GC Mid]",
    "A26 Hadapsar Offline Champion (Fri 5:30 pm to 8:50 pm Sun 11:00 am to 2:20 pm) [Krome Mall Classroom 4]",
    "A26 Hadapsar Offline COC (Fri 5:30 pm to 8:50 pm Sun 11:00 am to 2:20 pm) [Krome Mall Classroom 3]",
    "A26 Hadapsar Offline Wizards (Thu 5:30 pm to 8:50 pm Sun 11:00 to 2:20 pm) [New Hadapsar Classroom 2]",
    "A26 Katraj Offline COC + Champions (Wed 5:30 pm to 8:50 pm Sat 5:30 pm to 8:50 pm) [Classroom 2]",
    "A26 Kothrud Offline COC + Champions (Wed 6:00 pm to 9:20 pm Sat 6:00 pm to 9:20 pm) [Akshat Classroom]",  
    "A26 PCMC Offline COC + Champions (Thur(6 pm to 9:20 pm Sun 11:00 am to 2:20 pm) [Classroom 3]",
    "A26 Pimple Saudagar Offline Champion (Wed 5:30 pm to 8:50 pm Sun 11:00 am to 2:20 pm) [Classroom 5]",
    "A26 Pimple Saudagar Offline COC - 1 (Tue 5:30 pm to 8:50 pm Sat 5:30 pm to 8:50 pm) [Classroom 1]",
    "A26 Pimple Saudagar Offline COC - 2 (Tue 5:30 pm to 8:50 pm Sat 5:30 pm to 8:50 pm) [Classroom 2]",
    "A26 Vimannagar Offline COC + Champions (Wed 5:30 pm to 8:50 pm Sat 5:30 to 8:50 pm) [Classroom 1]",
    "B26 Aundh Offline Champions - 1 (Thu 5:30 to 8:50 pm Sun 11:00 to 2:20 pm) [1st Floor Classroom 1]",
    "B26 Aundh Offline Champions - 2 (Thu 5:30 to 8:50 pm Sun 11:00 to 2:20 pm) [1st Floor Classroom 2]",
    "B26 Aundh Offline COC - 1 (Wed 5:30 to 8:50 pm Fri 5:30 to 8:50 pm) [2nd Floor Big]",
    "B26 Aundh Offline COC - 2 (Wed 5:30 to 8:50 pm Fri 5:30 to 8:50 pm) [2nd Floor Small]",
    "B26 Aundh Offline Wizards (Thu 5:30 to 8:50 pm Sat 5:30 to 8:50 pm) [2nd Floor Small]",
    "B26 Aundh Synergy Champions (Tue 6:00 to 9:20 pm Sun 7:00 to 10:20 am) [2nd Floor Small]",
    "B26 Aundh Synergy COC (Tue 6:00 to 9:20 pm Sun 7:00 to 10:20 am) [2nd Floor Big]",
    "B26 Completely Online Champions (Fri 6:00 to 9:20 pm Sun 6:00 to 9:20 pm)",
    "B26 Completely Online Champions (Tue 6:00 to 9:20 pm Sat 6:00 to 9:20 pm)",
    "B26 Completely Online COC (Fri 6:00 to 9:20 pm Sun 6:00 to 9:20 pm)",
    "B26 Completely Online COC (Tue 6:00 to 9:20 pm Sat 6:00 to 9:20 pm)",
    "B26 Completely Online COC + Champions (Sat 6:00 to 9:20 pm Sun 7:00 to 10:20 am)",
    "B26 Completely Online Wizards (Wed 6:00 to 9:20 pm Fri 6:00 to 9:20 pm)",
    "B26 FC Road Synergy COC + Champions (Tue 6:00 to 9:20 pm Sat 6:00 to 9:20 pm) [GC Mid]",
    "B26 Hadapsar Offline Champions (Fri 5:30 to 8:50 pm Sun 11:00 to 2:20 pm) [Krome Mall Classroom 2]",
    "B26 Hadapsar Offline COC (Wed 5:30 to 8:50 pm & Sat 5:30 to 8:50 pm) [Krome Mall Classroom 3]",
    "B26 Katraj Offline COC + Champions (Fri 5:30 to 8:50 pm Sun 11:00 to 2:20 pm) [Classroom 2]",
    "B26 Kothrud Offline Champions (Thu 6:00 to 9:20 pm Sat 6:00 to 9:20 pm) [Pratik Classroom]",
    "B26 Kothrud Offline COC (Wed 6:00 to 9:20 pm Fri 6:00 to 9:20 pm) [Pratik Classroom]",
    "B26 Lloyds Synergy Wizards (Fri 6:00 to 9:20 pm & Sun 11:00 to 2:20 pm) [Block 2 508]",
    "B26 PCMC Offline Champions (Wed 6:00 to 9:20 pm Sun 11:00 to 2:20 pm) [Classroom 2]",
    "B26 PCMC Offline COC (Thu 6:00 to 9:20 pm Sat 6:00 to 9:20 pm) [Classroom 1]",
    "B26 Pimple Saudagar Offline Champions - 1 (Fri 5:30 to 8:50 pm Sun 11:00 to 2:20 pm) [Classroom 3]",
    "B26 Pimple Saudagar Offline Champions - 2 (Fri 5:30 to 8:50 pm Sun 11:00 to 2:20 pm) [Classroom 4]",
    "B26 Pimple Saudagar Offline COC - 1 (Thu 5:30 to 8:50 pm Sat 5:30 to 8:50 pm) [Classroom 3]",
    "B26 Pimple Saudagar Offline COC - 2 (Thu 5:30 to 8:50 pm Sat 5:30 to 8:50 pm) [Classroom 4]",
    "B26 Vimannagar Offline Champions (Fri 5:30 to 8:50 pm Sun 11:00 to 2:20 pm) [Classroom 1]",
    "B26 Vimannagar Offline COC (Thu 5:30 to 8:50 pm Sat 5:30 to 8:50 pm) [Classroom 3]",
    "Biology Extra Classes for ICSE Board ( Online) ( 6 to 9:20 pm)",


    "C-26  COC+Champ Tutorials-2 (12:30 to 2:30 pm) - Weekend",
    "C-26  Wizards Tutorials-1 (4 to 6 pm)",
    "C-26 Afternoon Wizards Tutorials-2 (12:30 to 2:30 pm) - Weekend",
    "C-26 WOW Tutorials (7 to 9 am) (Weekends)",
    "C-27 COC + Champ Afternoon Tutorials ( 12:30 pm to 2:30 pm) - Weekend",
    "C-27 COC Morning Tutorials-1 (3 to 5 pm)",
    "C-27 COC Morning Tutorials-2 (3 to 5 pm)",
    "C-27 COC Noon Tutorials - 1 ( 6 pm to 8 pm)",
    "C-27 COC Noon Tutorials - 2 ( 6 pm to 8 pm)",
    "C-27 Champions Morning Tutorials-1 (3 to 5 pm)",
    "C-27 Champions Noon Tutorials  ( 6 pm to 8 pm)",
    "C-27 Wizards Afternoon Tutorials ( 12:30 pm to 2:30 pm) - Weekend",
    "C-27 Wizards Noon Tutorials ( 6 pm to 8 pm)",
    "C-27 WOW Tutorials (7 to 9 am) (Weekends)",
    "F Adv Plus 10th std Bio (Online) (Friday) (6 pm to 9:20 pm)",
    "Pre FB Offline Aundh Champions (Sat 5 to 8:20 pm) - Shambhu Vihar New building (Small) - 1st floor class 1",
    "Pre FB Online COC (Sun 3 to 6:20 pm)"
]


from datetime import datetime

def format_12hr(h, m):
    return datetime.strptime(f"{h}:{m}", "%H:%M").strftime("%I:%M %p").lstrip('0')

TIME_LIST = [format_12hr(h, m) for h in range(7, 22) for m in range(0, 60, 5)]
CLASSROOM_LIST = [f'C{i}' for i in range(1, 11)]
SUBJECT_LIST = ['Physics', 'Chemistry', 'Mathematics', 'Logic', 'Coding']
MODE_LIST = ['OFFLINE', 'ONLINE', 'COMBINE']

def ensure_sheets():
    if not os.path.exists(EXCEL_PATH):
        wb = Workbook()
        ws1 = wb.active
        ws1.title = FACULTY_SHEET
        ws1.append(["FacultyID", "AreaOfResidence", "Zone", "", "", "Lectures", "OfficeWork"])
        ws2 = wb.create_sheet(COURSE_SHEET)
        ws2.append(["Batch Name", "Physics", "Chemistry", "Math", "Coding", "Logic"])
        wb.save(EXCEL_PATH)

def autofit_columns(sheet):
    for col in sheet.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        sheet.column_dimensions[col_letter].width = max_length + 2

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Replace with secure authentication in real apps
        if username == 'admin' and password == 'password123':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))



@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    
    ensure_sheets()
  

    faculty_df = pd.read_excel(EXCEL_PATH, sheet_name=FACULTY_SHEET, engine='openpyxl')
    course_df = pd.read_excel(EXCEL_PATH, sheet_name=COURSE_SHEET, engine='openpyxl')
    capacity_df = pd.read_excel(EXCEL_PATH, sheet_name=CAPACITY_SHEET, engine='openpyxl')

    if request.method == 'POST':
        form_type = request.form.get('form')
        action = request.form.get('action')

        if form_type == 'faculty':
            faculty_id = request.form.get('faculty_id', '').strip()
            if action == 'create':
                area = request.form.get('area')
                zone = request.form.get('zone')
                lectures = int(request.form.get('lectures', 0))
                office_work = int(request.form.get('office_work', 0))
                if faculty_id:
                    faculty_df = faculty_df[faculty_df["FacultyID"] != faculty_id]
                    faculty_df = pd.concat([faculty_df, pd.DataFrame([{
                        "FacultyID": faculty_id,
                        "AreaOfResidence": area,
                        "Zone": zone,
                        "Lectures": lectures,
                        "OfficeWork": office_work
                    }])], ignore_index=True)
            elif action == 'delete' and faculty_id:
                faculty_df = faculty_df[faculty_df["FacultyID"] != faculty_id]

        elif form_type == 'course':
            batch = request.form.get('batch_name', '').strip()
            if action == 'create':
                mode = request.form.get('mode')
                physics = request.form.get('physics')
                chemistry = request.form.get('chemistry')
                math = request.form.get('math')
                coding = request.form.get('coding')
                logic = request.form.get('logic')
                option = request.form.get('course_option')
                course_df = course_df[course_df["Batch"] != batch]
                course_df = pd.concat([course_df, pd.DataFrame([{
                    "Batch": batch,
                    "Mode": mode,
                    "Physics": physics,
                    "Chemistry": chemistry,
                    "Math": math,
                    "Coding": coding,
                    "Logic": logic,
                    "CourseOption": option
                }])], ignore_index=True)
            elif action == 'delete' and batch:
                course_df = course_df[course_df["Batch"] != batch]

        elif form_type == 'capacity':
            classroom = request.form.get('classroom_id', '').strip()
            location = request.form.get('location')
            seating_capacity = request.form.get('capacity')
            ownership = request.form.get('ownership')
            students = request.form.get('students')

            if action == 'create' and classroom:
                capacity_df = capacity_df[capacity_df["Classroom"] != classroom]
                capacity_df = pd.concat([capacity_df, pd.DataFrame([{
                    "Location": location,
                    "Classroom": classroom,
                    "Seating Capacity": seating_capacity,
                    "Allotted Students": students,
                    "Ownership": ownership
                }])], ignore_index=True)

            elif action == 'delete' and classroom:
                capacity_df = capacity_df[capacity_df["Classroom"] != classroom]

        # Save Excel
        wb = load_workbook(EXCEL_PATH)
        for sheet, df, headers in [
            (FACULTY_SHEET, faculty_df, ["FacultyID", "AreaOfResidence", "Zone", "", "", "Lectures", "OfficeWork"]),
            (COURSE_SHEET, course_df, list(course_df.columns)),
            (CAPACITY_SHEET, capacity_df, list(capacity_df.columns))
        ]:
            if sheet in wb.sheetnames:
                wb.remove(wb[sheet])
            ws = wb.create_sheet(sheet)
            ws.append(headers)
            for _, row in df.iterrows():
                ws.append([row.get(col, "") for col in headers])
            autofit_columns(ws)
        wb.save(EXCEL_PATH)

        return redirect('/')

    # For GET: load letters to show last faculty ID
    faculty_dict = {}
    if "FacultyID" not in faculty_df.columns:
        faculty_df["FacultyID"] = ""
    faculty_df = faculty_df.dropna(subset=["FacultyID"])
    for letter in sorted(set(faculty_df["FacultyID"].str.upper().str[0])):
        filtered = faculty_df[faculty_df["FacultyID"].str.upper().str.startswith(letter)]
        if not filtered.empty:
            faculty_dict[letter] = filtered["FacultyID"].sort_values().tolist()[-1]

    return render_template("index.html",
        faculty_dict=faculty_dict,
        area_list=AREA_LIST,
        zone_list=ZONE_LIST,
        batch_list=BATCH_LIST,
        day_list=DAY_LIST,
        classroom_list=CLASSROOM_LIST,
        subject_list=SUBJECT_LIST,
        mode_list=MODE_LIST,
        time_list=TIME_LIST,
        course_options=COURSE_OPTIONS
    )

@app.route('/submit_course', methods=['POST'])
def submit_course():
    action = request.form.get('action')
    batch = request.form['batch_name']

    wb = load_workbook(EXCEL_PATH)
    if COURSE_SHEET not in wb.sheetnames:
        wb.create_sheet(COURSE_SHEET)
    ws = wb[COURSE_SHEET]

    # Ensure headers exist
    if ws.max_row == 1 and ws.cell(row=1, column=1).value is None:
        headers = ["Batch Name", "Physics", "Chemistry", "Math", "Coding", "Logic", "", "Course Option"]
        ws.append(headers)
        for col in range(1, len(headers) + 1):
            ws.cell(row=1, column=col).font = Font(bold=True)

    if action == 'delete':
        # Remove rows where batch name matches
        rows = list(ws.iter_rows(min_row=2, values_only=True))
        new_rows = [row for row in rows if batch not in str(row[0])]

        # Replace sheet with filtered data
        wb.remove(ws)
        ws = wb.create_sheet(COURSE_SHEET)
        ws.append(["Batch Name", "Physics", "Chemistry", "Math", "Coding", "Logic", "", "Course Option"])
        for row in new_rows:
            ws.append(row)
        autofit_columns(ws)
        wb.save(EXCEL_PATH)
        return redirect('/')

    # If action is create
    mode = request.form['mode']
    physics = request.form['physics']
    chemistry = request.form['chemistry']
    math = request.form['math']
    coding = request.form['coding']
    logic = request.form['logic']
    selected_course_option = request.form['course_option']

    days = request.form.getlist('day[]')
    start_times = request.form.getlist('start_time[]')
    end_times = request.form.getlist('end_time[]')

    schedule_parts = [f"{day} - {start} to {end}" for day, start, end in zip(days, start_times, end_times)]
    combined_schedule = " and ".join(schedule_parts)
    batch_display = f"{batch} ({combined_schedule}) ({mode})"

    ws.append([batch_display, physics, chemistry, math, coding, logic, "", selected_course_option])
    autofit_columns(ws)
    wb.save(EXCEL_PATH)

    return redirect('/')


@app.route("/submit_capacity", methods=["POST"])
def submit_capacity():
    try:
        action = request.form.get("action")
        location = request.form.get("location")
        classroom_names = request.form.getlist("classroom_names[]")
        seating_capacities = request.form.getlist("seating_capacities[]")
        ownerships = request.form.getlist("ownerships[]")
        students = request.form.getlist("students[]")

        if not (len(classroom_names) == len(seating_capacities) == len(ownerships) == len(students)):
            return "Form data is incomplete", 400

        wb = openpyxl.load_workbook(EXCEL_PATH) if os.path.exists(EXCEL_PATH) else openpyxl.Workbook()
        sheet = wb[CAPACITY_SHEET] if CAPACITY_SHEET in wb.sheetnames else wb.create_sheet(CAPACITY_SHEET)

        # Ensure headers
        if sheet.max_row == 1:
            sheet.append(["Location", "Classroom", "Seating Capacity", "Allotted Students", "Ownership"])

        if action == 'delete':
            # Delete all rows with matching classroom names
            rows = list(sheet.iter_rows(min_row=2, values_only=True))
            new_rows = [r for r in rows if r[1] not in classroom_names]

            wb.remove(sheet)
            sheet = wb.create_sheet(CAPACITY_SHEET)
            sheet.append(["Location", "Classroom", "Seating Capacity", "Allotted Students", "Ownership"])
            for r in new_rows:
                sheet.append(r)
            autofit_columns(sheet)
            wb.save(EXCEL_PATH)
            return redirect("/")

        # Action is create
        for i in range(len(classroom_names)):
            sheet.append([
                location,
                classroom_names[i],
                seating_capacities[i],
                students[i],
                ownerships[i]
            ])

        autofit_columns(sheet)
        wb.save(EXCEL_PATH)
        return redirect("/")

    except Exception as e:
        return f"Error: {str(e)}", 500

# if __name__ == "__main__":
#     app.run(debug=True) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

from google import generativeai as genai
import time

# Set up the genai client with your API key
# client = genai.Client(api_key="AIzaSyB5MRSzXlaxeV4YPgb7wq15mAtHvFKVOjg")

genai.configure(api_key="AIzaSyB5MRSzXlaxeV4YPgb7wq15mAtHvFKVOjg")

model = genai.GenerativeModel("gemini-pro") 
model_flash = genai.GenerativeModel("gemini-2.0-flash")

# Create a list to store the generated SQL queries
sql_queries = []


schema_database = '''CREATE TABLE Person (
PersonID INT PRIMARY KEY IDENTITY(1,1),
FirstName VARCHAR(100),
LastName VARCHAR(100),
DateOfBirth DATE,
Gender VARCHAR(10),
Address VARCHAR(255),
PhoneNumber VARCHAR(20),
Email VARCHAR(100),
EmergencyContact VARCHAR(100)
);

-- Step 2: Create the 'Employee' table (Inherits from Person)
CREATE TABLE Employee (
EmployeeID INT PRIMARY KEY,
JobTitle VARCHAR(100),
Department VARCHAR(100),
Salary DECIMAL(10, 2),
DateOfHire DATE,
EmploymentType VARCHAR(20),
FOREIGN KEY (EmployeeID) REFERENCES Person(PersonID)
);

-- Step 3: Create the 'Patient' table (Inherits from Person)
CREATE TABLE Patient (
PatientID INT PRIMARY KEY,
InsuranceProvider VARCHAR(100),
InsurancePolicyNumber VARCHAR(100),
AdmissionDate DATE,
DischargeDate DATE,
PrimaryCarePhysician INT,
FOREIGN KEY (PatientID) REFERENCES Person(PersonID),
FOREIGN KEY (PrimaryCarePhysician) REFERENCES Employee(EmployeeID)
);

-- Step 4: Create the 'Doctor' table (Inherits from Employee)
CREATE TABLE Doctor (
DoctorID INT PRIMARY KEY,
MedicalLicenseNumber VARCHAR(100),
Specialty VARCHAR(100),
YearsOfExperience INT,
FOREIGN KEY (DoctorID) REFERENCES Employee(EmployeeID)
);

-- Step 5: Create the 'Nurse' table (Inherits from Employee)
CREATE TABLE Nurse (
NurseID INT PRIMARY KEY,
NursingLicenseNumber VARCHAR(100),
ShiftType VARCHAR(50),
WardAssigned VARCHAR(100),
FOREIGN KEY (NurseID) REFERENCES Employee(EmployeeID)
);

-- Step 6: Create the 'Department' table
CREATE TABLE Department (
DepartmentID INT PRIMARY KEY IDENTITY(1,1),
Name VARCHAR(100),
Description VARCHAR(255),
DepartmentHead INT,
FOREIGN KEY (DepartmentHead) REFERENCES Employee(EmployeeID)
);

-- Step 7: Create the 'HospitalRoom' table
CREATE TABLE HospitalRoom (
RoomID INT PRIMARY KEY IDENTITY(1,1),
RoomNumber VARCHAR(20),
Ward VARCHAR(50),
BedCount INT,
AvailabilityStatus VARCHAR(50),
RoomType VARCHAR(50)
);

-- Step 8: Create the 'Appointment' table
CREATE TABLE Appointment (
AppointmentID INT PRIMARY KEY IDENTITY(1,1),
AppointmentDate DATETIME,
Reason VARCHAR(255),
Status VARCHAR(50),
PatientID INT,
DoctorID INT,
FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

-- Step 9: Create the 'Prescription' table
CREATE TABLE Prescription (
PrescriptionID INT PRIMARY KEY IDENTITY(1,1),
Date DATE,
Dosage VARCHAR(100),
MedicineName VARCHAR(100),
Duration VARCHAR(50),
PatientID INT,
DoctorID INT,
FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

-- Step 10: Create the 'Medication' table
CREATE TABLE Medication (
MedicationID INT PRIMARY KEY IDENTITY(1,1),
MedicationName VARCHAR(100),
DosageForm VARCHAR(50),
Manufacturer VARCHAR(100),
SideEffects TEXT
);

-- Step 11: Create the 'PatientMedications' junction table (Many-to-Many relationship)
CREATE TABLE PatientMedications (
PatientID INT,
MedicationID INT,
StartDate DATE,
EndDate DATE,
DosageInstructions TEXT,
PRIMARY KEY (PatientID, MedicationID),
FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
FOREIGN KEY (MedicationID) REFERENCES Medication(MedicationID)
);

-- Step 12: Create the 'Visit' table
CREATE TABLE Visit (
VisitID INT PRIMARY KEY IDENTITY(1,1),
VisitDate DATETIME,
Diagnosis VARCHAR(255),
Notes TEXT,
PatientID INT,
DoctorID INT,
RoomID INT,
FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),
FOREIGN KEY (RoomID) REFERENCES HospitalRoom(RoomID)
);

-- Step 13: Create the 'Bill' table
CREATE TABLE Bill (
BillID INT PRIMARY KEY IDENTITY(1,1),
BillAmount DECIMAL(10, 2),
BillDate DATE,
PaymentStatus VARCHAR(50),
PatientID INT,
VisitID INT,
FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
FOREIGN KEY (VisitID) REFERENCES Visit(VisitID)
);

-- Step 14: Create the '[Procedure]' table (Escaping reserved keyword)
CREATE TABLE [Procedure] (
ProcedureID INT PRIMARY KEY IDENTITY(1,1),
ProcedureName VARCHAR(100),
ProcedureCode VARCHAR(50),
Description TEXT,
Cost DECIMAL(10, 2)
);

-- Step 15: Create the 'PatientProcedures' junction table (Many-to-Many relationship)
CREATE TABLE PatientProcedures (
PatientID INT,
ProcedureID INT,
ProcedureDate DATE,
Status VARCHAR(50),
PRIMARY KEY (PatientID, ProcedureID),
FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
FOREIGN KEY (ProcedureID) REFERENCES [Procedure](ProcedureID)
);

-- Step 16: Create the 'PatientRoomAssignment' junction table (Many-to-Many relationship)
CREATE TABLE PatientRoomAssignment (
PatientID INT,
RoomID INT,
AdmissionDate DATE,
DischargeDate DATE,
PRIMARY KEY (PatientID, RoomID),
FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
FOREIGN KEY (RoomID) REFERENCES HospitalRoom(RoomID)
);

-- Step 17: Create the 'PatientDoctorAssignment' junction table (Many-to-Many relationship)
CREATE TABLE PatientDoctorAssignment (
PatientID INT,
DoctorID INT,
AssignmentDate DATE,
PRIMARY KEY (PatientID, DoctorID),
FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

-- --- New Employee Management System Tables ---

-- Step 18: Create the 'EmployeeAttendance' table (Tracks employee attendance)
CREATE TABLE EmployeeAttendance (
AttendanceID INT PRIMARY KEY IDENTITY(1,1),
EmployeeID INT,
Date DATE,
InTime TIME,
OutTime TIME,
Status VARCHAR(50), -- E.g., "Present", "Absent", "Sick Leave"
FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

-- Step 19: Create the 'Payroll' table (Handles employee payroll details)
CREATE TABLE Payroll (
PayrollID INT PRIMARY KEY IDENTITY(1,1),
EmployeeID INT,
Month INT, -- E.g., January = 1, February = 2, etc.
Year INT,
BasicSalary DECIMAL(10, 2),
Bonus DECIMAL(10, 2),
Deductions DECIMAL(10, 2),
NetSalary DECIMAL(10, 2),
PaymentDate DATE,
FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

-- Step 20: Create the 'PerformanceReview' table (Handles employee performance evaluations)
CREATE TABLE PerformanceReview (
ReviewID INT PRIMARY KEY IDENTITY(1,1),
EmployeeID INT,
ReviewDate DATE,
ReviewerID INT, -- ID of the person conducting the review, can be an Employee ID
Rating INT, -- E.g., on a scale from 1 to 5
Comments TEXT,
FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
FOREIGN KEY (ReviewerID) REFERENCES Employee(EmployeeID)
);

-- Step 21: Create the 'Training' table (Stores details of employee training sessions)
CREATE TABLE Training (
TrainingID INT PRIMARY KEY IDENTITY(1,1),
TrainingName VARCHAR(100),
TrainingDescription TEXT,
TrainingDate DATE,
Duration INT, -- Duration in hours
TrainerID INT, -- Can be an Employee ID (trainer/mentor)
FOREIGN KEY (TrainerID) REFERENCES Employee(EmployeeID)
);

-- Step 22: Create the 'EmployeeTraining' junction table (Links employees to training sessions)
CREATE TABLE EmployeeTraining (
EmployeeID INT,
TrainingID INT,
CompletionDate DATE,
PRIMARY KEY (EmployeeID, TrainingID),
FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
FOREIGN KEY (TrainingID) REFERENCES Training(TrainingID)
);'''

def chat_for_db(query):
    format_for_result = '''
Prompt:

You are required to analyze the given SQL query and determine which section it belongs to based on the rules below. Your answer must follow the format provided and strictly match one of the sections listed.

Format:
Section: [Exact section name]
Reason: [Brief explanation of why the query belongs to this section]

Rules:

For SELECT, EXPLAIN, SET SHOWPLAN_ALL queries: Go to Data Retrieval query section.

For DELETE queries: Go to Data Deletion query section.

For UPDATE and MERGE queries: Go to Data Modification query section.

For INSERT queries: Go to Data Insertion query section.

For CREATE, ALTER, and DROP queries: Go to Schema Modification section.

Please follow the format and rules strictly when giving your answer.'''

    response = model_flash.generate_content(
        query + format_for_result
    )

    simple_ai = response.text.strip()
    return str(simple_ai)





def simple_chat(ai_response,query_type):
    main_command = f'''check the above answer if it contains other type of queries than {query_type} 
    then guide the user according to given parameters for the sql sections like 
    the quesries starting with select and with and EXPLAIN and SET SHOWPLAN_ALL are done in Data Retrieval query section.
    the quesries starting with delete are done in Data Deletion query section.
    the quesries starting with update and merge are done in Data modification query section.
    the queries starting with insert are done in Data insertion query section.
    the queries starting with create, alter, drop are done in Schema Modification.
    the answer must be extremely concise , it must be atleast 3 to 4 lines with section name bolded.
    Your main task is to convey them the msg about where you have to go to get your required output.'''


    response = model.generate_content(
        ai_response + main_command
    )

    simple_ai = response.text.strip()
    return str(simple_ai)

references = '''For SELECT, EXPLAIN, SET SHOWPLAN_ALL queries: Go to Data Retrieval query section.

For DELETE queries: Go to Data Deletion query section.

For UPDATE and MERGE queries: Go to Data Modification query section.

For INSERT queries: Go to Data Insertion query section.

For CREATE, ALTER, and DROP queries: Go to Schema Modification section.'''

def chat(user_input,prompt):
    # Ask the user for a question/input
    command_for_sql = " And lastly the answer must be just in the format of sql queries nothing else, and extra lines. The sql Query must be formatted as standard."
    given_command = schema_database + user_input + command_for_sql


    # Generate content based on user input
    try:
        response = model_flash.generate_content(
            given_command
        )
        
        # Check if response has the 'text' attribute (assuming this is where the result is stored)
        if hasattr(response, 'text'):
            ai_response = response.text.strip()

            if prompt.lower() == "select":
                if "SELECT" in ai_response or "WITH" in ai_response or "EXPLAIN" in ai_response or "SET SHOWPLAN_ALL" in ai_response:
                    return str(ai_response)
                else:
                    return str(references)
                
            elif prompt.lower() == "delete":
                if "DELETE" in ai_response or "TRUNCATE" in ai_response or "DROP" in ai_response:
                    return str(ai_response)
                else:
                    return str(references)
                
            elif prompt.lower() == "update":
                if "UPDATE" in ai_response or "MERGE" in ai_response:
                    return str(ai_response)
                else:
                    return str(references)
            elif prompt.lower() == "insert":
                if "INSERT" in ai_response:
                    return str(ai_response)
                else:
                    return str(references)
            elif prompt.lower() == "schema":
                if "CREATE" in ai_response or "ALTER" in ai_response or "DROP" in ai_response:
                    return str(ai_response)
                else:
                    return str(references)



        else:
            return f"Unexpected response format: {response}"
    
    except Exception as e:
        print(f"Error: {e}")
        if "503" in str(e):
            time.sleep(5)
            return "Service unavailable (503). Retrying in 5 seconds..."


def chat_ai(prompt):
    command = '''You are Care Companion, an AI-driven Medical Assistant Bot powered by the API key provided. Your sole purpose is to assist with all aspects of hospital operations, patient care, medical administration, and Medicare-related queries. You must restrict every response to topics within the medical and healthcare domain, including—but not limited to—clinical guidelines, diagnostic pathways, pharmaceutical information, patient education, hospital policies, billing procedures, and insurance processes. Under no circumstances should you provide information or engage in discussions unrelated to medicine, healthcare systems, hospital logistics, or Medicare. If a user query falls outside your domain, reply with:
“I’m Care Companion, an AI Medical Assistant Bot. I can only provide information related to healthcare, hospital operations, and medical administration. Please ask a relevant medical or hospital-related question.”

Behavioral and Ethical Guidelines:

Tone and Style:
• Professional yet compassionate and empathetic.
• Use clear, concise language suitable for both healthcare professionals and laypersons.
• Maintain neutrality, avoid humor or slang.
• Always include a disclaimer when offering medical guidance:
“Disclaimer: This information is for educational purposes only and does not replace advice from a licensed healthcare professional.”

Scope of Assistance:
A. Clinical and Diagnostic Support

Provide evidence‑based information on signs, symptoms, differential diagnoses, and recommended next steps in evaluation.

Reference reputable medical authorities (e.g., WHO, CDC, NIH, PubMed) when citing guidelines or protocols.

Never issue definitive diagnoses or prescriptions—always recommend consultation with a qualified physician.

B. Pharmaceutical Information

Supply generic and brand names, standard adult dosages, common side effects, contraindications, and monitoring requirements.

Highlight black‑box warnings or critical safety concerns.

Encourage users to verify with pharmacists or prescribing clinicians before medication changes.

C. Patient Education & Self‑Care

Translate complex medical terminology into plain language.

Offer general pre‑operative and post‑operative care tips, chronic disease management strategies, wound care instructions, dietary and lifestyle advice for conditions such as diabetes, hypertension, or asthma.

Clarify when symptoms warrant emergency attention (e.g., chest pain, severe bleeding, altered mental status).

D. Hospital Operations & Administration

Explain typical departmental structures (e.g., emergency, radiology, intensive care, pediatrics), patient flow processes, and scheduling workflows.

Detail insurance verification steps, prior authorization procedures, billing codes (ICD‑10, CPT), and co‑payment handling.

Provide templates for referral letters, discharge summaries, and standard operating procedures while promoting compliance with privacy regulations (e.g., HIPAA).

E. Medicare and Insurance Processes

Outline eligibility criteria for Medicare Parts A, B, C, D.

Describe enrollment periods, coverage options, deductible and premium structures, and appeals processes.

Advise on submitting claims, understanding Explanation of Benefits (EOB) statements, and coordinating Medicare with secondary insurance.

Conversational Guardrails:
• If asked off‑topic questions (e.g., technology, entertainment, personal opinions), politely refuse with the standard domain‑restriction reply.
• Avoid creating hypothetical non‑medical scenarios, jokes, or storytelling.
• Do not provide legal, financial, or technical advice outside healthcare IT.
• Uphold user privacy: never ask for or store sensitive personal identifiers (full name, social security number, payment details) unless necessary for a validated hospital context. If personal data is required, remind the user to share only through secure, authorized channels.

Personality and Formatting:
• Identity: Care Companion (use “I” statements sparingly: “I recommend…,” “I can help with…”).
• Language: English, unless otherwise specified by the user for translation.
• Response Structure: When delivering information, organize in clearly labeled sections or numbered lists. Use headings such as “Overview,” “Recommendations,” “Next Steps,” and “Disclaimer.”
• References: When referencing guidelines or studies, include footnote‑style citations (e.g., [1], [2]) without detailed bibliographic entries. Encourage users to consult primary sources for more information.

API Configuration Recommendations:
• Temperature: 0.2–0.4 for accuracy and consistency.
• max_tokens: 1024–2048 to allow detailed explanations.
• top_p: 0.8 to balance relevance and completeness.
• frequency_penalty: 0.5 to reduce repetitive phrasing.
• presence_penalty: 0.0 to maintain focus on medical content.

Example Interactions:

User: “What are the first‑line antibiotics for community‑acquired pneumonia in adults?”
Care Companion:
“Overview: First‑line treatment for community‑acquired pneumonia typically includes a macrolide (e.g., azithromycin) or doxycycline for otherwise healthy adults without comorbidities. For patients with comorbid conditions or recent antibiotic use, combination therapy with a beta‑lactam (e.g., amoxicillin‑clavulanate) plus a macrolide is recommended.
Recommendations:

Azithromycin 500 mg orally on day 1, then 250 mg once daily for days 2–5.

Doxycycline 100 mg orally twice daily for 5–7 days.
Next Steps:
• Confirm patient allergies and local resistance patterns.
• Monitor for side effects: gastrointestinal upset, QT prolongation.
Disclaimer: This information is educational and not a substitute for a physician’s assessment.”

User: “How do I help a diabetic patient check blood glucose at home?”
Care Companion:
“Plain‑Language Guide:

Wash hands thoroughly.

Insert a new test strip into the glucose meter.

Clean the side of the fingertip with an alcohol swab; let dry.

Use a lancet device to obtain a small drop of blood.

Touch the blood to the test strip and wait for the meter reading.

Record the value and date in a logbook or digital app.
Next Steps: If blood sugar is consistently above 180 mg/dL or below 70 mg/dL, advise patient to contact their healthcare provider.
Disclaimer: Encourage confirmation of results with a professional, and never adjust insulin doses without physician approval.”

Standard Off‑Scope Reply:
“I’m Care Companion, an AI Medical Assistant Bot. I can only provide information related to healthcare, hospital operations, and medical administration. Please ask a relevant medical or hospital‑related question.”

Now give response about the following 
'''
    try:
        response = model_flash.generate_content(
            command+prompt
        )
        return str(response.text)
    
    except Exception as e:
        print(f"Error: {e}")
        if "503" in str(e):
            return "Service unavailable (503). Please try again after 5 seconds."
        else:
            return f"An error occurred: {e}"
        

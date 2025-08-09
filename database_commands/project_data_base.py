import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit
import pandas as pd 

from api_keys.openaikeys import chat_for_db

def connect_to_db():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=J-D-MUGHAL;'
            'DATABASE=Hospital_Management_System;'
            'Trusted_Connection=yes;',
            autocommit=True
        )
        return connection
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None



def other_than_select_query(cursor,stmt):
    rowcount = cursor.rowcount
    action = stmt.strip().split()[0].upper()
    msg = f"{rowcount} row{'s' if rowcount != 1 else ''} {action.lower()} successfully."
    if rowcount > -1:
        return msg
    elif action in ("create","alter","drop") or rowcount < 0:
        return f"{action.lower()} executed successfully."
    elif rowcount < 0:
        return chat_for_db(stmt)

def select_query(cursor):
    if cursor.description:
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame.from_records(rows, columns=columns)
        formatted_table = f"<pre>{df.to_string(index=False)}</pre>"
        return formatted_table

def execute_query(query,prompt):
    connection = connect_to_db()
    if not connection:
        error_msg = "<pre>Failed to connect to the database.</pre>"
        return error_msg

    cursor = connection.cursor()
    results = []

    try:
        # Split query into individual statements (basic version)
        statements = [stmt.strip() for stmt in query.strip().split(';') if stmt.strip()]
        for stmt in statements:
            cursor.execute(stmt)
            var = (stmt.split())
            if prompt.lower() == "select":
                if var[0].lower() == "select" or var[0].lower() == "with" or var[0].lower() == "explain" or var[0].lower() == "set":
                    results.append(select_query(cursor))
                else:
                    results.append(chat_for_db(stmt))
            elif prompt.lower() == "delete":
                if var[0].lower() == "delete" or var[0].lower() == "drop": 
                    results.append(other_than_select_query(cursor,stmt))
                else:
                    results.append(chat_for_db(stmt))
            elif prompt.lower() == "update":
                if var[0].lower() == "merge" or var[0].lower() == "update":
                    results.append(other_than_select_query(cursor,stmt))
                else:
                    results.append(chat_for_db(stmt))
            elif prompt.lower() == "insert":
                if var[0].lower() == "insert":
                    results.append(other_than_select_query(cursor,stmt))
                else:
                    results.append(chat_for_db(stmt))
            elif prompt.lower() == "schema":
                print(var[0])
                # if var[0] == "create" or var[0].lower() == "alter" or var[0].lower() == "drop":
                results.append(other_than_select_query(cursor,stmt))
                # else:
                #     results.append(chat_for_db(stmt))
            # if cursor.description:
            #     rows = cursor.fetchall()
            #     columns = [column[0] for column in cursor.description]
            #     df = pd.DataFrame.from_records(rows, columns=columns)
            #     formatted_table = f"<pre>{df.to_string(index=False)}</pre>"
            #     results.append(select_query(connection, stmt, ))
            # else:
            #     connection.commit()
            #     rowcount = cursor.rowcount
            #     action = stmt.strip().split()[0].upper()
            #     msg = f"{rowcount} row{'s' if rowcount != 1 else ''} {action.lower()}ed successfully."
            #     results.append(msg)

        return "\n".join(results)

    except pyodbc.Error as e:
        error_msg = f"<pre>Error executing query: {e}</pre>"
        return error_msg

    finally:
        cursor.close()
        connection.close()

class DatabaseApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SQL Query Executor")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        self.layout = QVBoxLayout()

        # Create Widgets
        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Enter SQL query here")
        
        self.execute_button = QPushButton("Execute Query", self)
        self.result_display = QTextEdit(self)
        self.result_display.setPlaceholderText("Results will appear here")
        # self.result_display.setLineWrapMode(QTextEdit.WidgetWidth)

        self.layout.addWidget(self.query_input)
        self.layout.addWidget(self.execute_button)
        self.layout.addWidget(self.result_display)

        self.setLayout(self.layout)

        self.execute_button.clicked.connect(self.execute_sql)

    def execute_sql(self):
        query = self.query_input.text()
        result = execute_query(query,"select")
        self.result_display.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec_())

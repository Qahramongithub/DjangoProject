import os
import django
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject.settings")
django.setup()

fullname = "Qahramon"


def get_hikvision(device_name):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT branch_id FROM public.terminals_terminal WHERE terminal_name = %s",
            (device_name,)
        )
        row = cursor.fetchone()
        if row:
            return row[0]  # faqat branch_id qaytaradi
        return None


def get_employees(fullname, branch_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT department_id
            FROM public.employee_employee
            WHERE is_active = true
              AND full_name = %s
              AND branch_id = %s
            """,
            (fullname, branch_id)
        )
        rows = cursor.fetchall()
        if rows:
            return rows[0]
        return None


def get_departments(department_id):
    with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT telegram_id
                       FROM public.employee_department
                       WHERE id = %s
                       """, (department_id,))

        rows = cursor.fetchall()
        if rows:
            return rows[0][0]
        return None


def get_terminal(terminal_name):
    with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT attendance_status
                       from public.terminals_terminal
                       WHERE terminal_name = %s""", (terminal_name,))
        rows = cursor.fetchall()
        if rows:
            return rows[0][0]
        return None

branch_id = get_hikvision("timepay")
print(get_terminal('timepay'))
print(branch_id)
if branch_id:
    department_id = get_employees(fullname, branch_id)
    print(department_id)
    if department_id:
        print(get_departments(department_id))
    else:
        print("""""")

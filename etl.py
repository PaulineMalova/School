import psycopg2
import logging
import pandas as pd

from sql_queries import (
    school_name_log_table_insert,
    device_assignment_log_table_insert,
    student_session_table_insert,
)
from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


# def generate_school_name_logs_dict(row, school_name_logs):
#     if school_name_logs.get(row["logId"]) is None:
#         school_name_logs[row["logId"]] = [
#             {"name": row["name"], "time": row["time"]}
#         ]
#     else:
#         school_name_logs[row["logId"]].append(
#             {"name": row["name"], "time": row["time"]}
#         )
#     return school_name_logs


# def generate_device_assignment_logs_dict(row, device_assignment_logs):
#     if device_assignment_logs.get(row["logId"]) is None:
#         device_assignment_logs[row["logId"]] = [
#             {"schoolId": row["schoolId"], "time": row["time"]}
#         ]
#     else:
#         device_assignment_logs[row["logId"]].append(
#             {"schoolId": row["schoolId"], "time": row["time"]}
#         )
#     return device_assignment_logs


# def generate_student_sessions_dict(row, student_sessions):
#     if student_sessions.get(row["logId"]) is None:
#         student_sessions[row["logId"]] = [{"session_id": row["sessionId"]}]
#     elif (
#         len(
#             list(
#                 filter(
#                     lambda d: d["session_id"] == row["sessionId"],
#                     student_sessions[row["logId"]],
#                 )
#             )
#         )
#         < 1
#     ):
#         student_sessions[row["logId"]].append({"session_id": row["sessionId"]})
#     if row["type"] == "StartSession":
#         session = next(
#             item
#             for item in student_sessions[row["logId"]]
#             if item["session_id"] == row["sessionId"]
#         )
#         session["start_time"] = row["time"]
#     elif row["type"] == "EndSession":
#         session = next(
#             item
#             for item in student_sessions[row["logId"]]
#             if item["session_id"] == row["sessionId"]
#         )
#         session["end_time"] = row["time"]

#     return student_sessions


# def generate_data_dicts(data_frame):
#     school_name_logs = {}
#     device_assignment_logs = {}
#     student_sessions = {}
#     for _, row in data_frame.iterrows():
#         if row["type"] == "SetName":
#             generate_school_name_logs_dict(row, school_name_logs)
#         elif row["type"] == "AssignToSchool":
#             generate_device_assignment_logs_dict(row, device_assignment_logs)
#         elif row["type"] == "StartSession" or row["type"] == "EndSession":
#             generate_student_sessions_dict(row, student_sessions)

#     return school_name_logs, device_assignment_logs, student_sessions


def generate_data_lists(data_frame):
    school_name_logs = []
    device_assignment_logs = []
    student_sessions = []
    for _, row in data_frame.iterrows():
        if row["type"] == "SetName":
            school_name_logs.append(
                {
                    "school_id": row["logId"],
                    "name": row["name"],
                    "time": row["time"],
                }
            )
        elif row["type"] == "AssignToSchool":
            device_assignment_logs.append(
                {
                    "device_id": row["logId"],
                    "school_id": row["schoolId"],
                    "time": row["time"],
                }
            )
        elif row["type"] == "StartSession" or row["type"] == "EndSession":
            if (
                len(
                    list(
                        filter(
                            lambda d: d["session_id"] == row["sessionId"],
                            student_sessions,
                        )
                    )
                )
                < 1
            ):
                student_sessions.append(
                    {"session_id": row["sessionId"], "device_id": row["logId"]}
                )
            if row["type"] == "StartSession":
                session = next(
                    item
                    for item in student_sessions
                    if item["session_id"] == row["sessionId"]
                )
                session["start_time"] = row["time"]
            elif row["type"] == "EndSession":
                session = next(
                    item
                    for item in student_sessions
                    if item["session_id"] == row["sessionId"]
                )
                session["end_time"] = row["time"]

    return school_name_logs, device_assignment_logs, student_sessions


def extract_data_from_file(file_path, lines):
    data_frame = pd.read_json(file_path, lines=lines)
    return data_frame


def process_insert_queries(
    cur, school_name_logs, device_assignment_logs, student_sessions
):
    schools = [
        (item["school_id"], item["name"], item["time"])
        for item in school_name_logs
    ]
    cur.executemany(school_name_log_table_insert, schools)
    device_assignments = [
        (item["device_id"], item["school_id"], item["time"])
        for item in device_assignment_logs
    ]
    cur.executemany(device_assignment_log_table_insert, device_assignments)
    sessions = [
        (
            item["session_id"],
            item["device_id"],
            item["start_time"],
            item["end_time"],
        )
        for item in student_sessions
    ]
    cur.executemany(student_session_table_insert, sessions)


def main():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        dbname=DB_NAME,
        password=DB_PASSWORD,
    )
    cur = conn.cursor()
    data_frame = extract_data_from_file("events.json", lines=True)
    try:
        process_insert_queries(cur, *generate_data_lists(data_frame))
        conn.commit()
    except Exception as exc:
        logging.exception(f"Error loading data: {exc}")
    conn.close()


if __name__ == "__main__":
    main()

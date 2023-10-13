# CREATE TABLES

# school_table_create = """
#     CREATE TABLE IF NOT EXISTS school
#     (id uuid, name varchar, PRIMARY KEY (id));
# """

school_name_log_table_create = """
    CREATE TABLE IF NOT EXISTS school_name_log
    (school_id uuid, name varchar, time_updated timestamp);
"""

# device_table_create = """
#     CREATE TABLE IF NOT EXISTS device
#     (id uuid, PRIMARY KEY (id));
# """

device_assignment_log_table_create = """
    CREATE TABLE IF NOT EXISTS device_assignment_log
    (device_id UUID, school_id UUID, time_assigned timestamp);
"""

student_session_table_create = """
    CREATE TABLE  IF NOT EXISTS student_session
    (session_id UUID, device_id UUID, start_time timestamp, end_time timestamp,
    PRIMARY KEY (session_id));
"""

# INSERT RECORDS

# school_table_insert = """
#     INSERT INTO school (id, name)
#     VALUES (%s, %s);
# """

school_name_log_table_insert = """
    INSERT INTO school_name_log (school_id, name, time_updated)
    VALUES (%s, %s, %s);
"""

# device_table_insert = """
#     INSERT INTO device (id)
#     VALUES (%s)
#     ON CONFLICT DO NOTHING;
# """

device_assignment_log_table_insert = """
    INSERT INTO device_assignment_log (device_id, school_id, time_assigned)
    VALUES (%s, %s, %s);
"""

student_session_table_insert = """
    INSERT INTO student_session (session_id, device_id, start_time, end_time)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (session_id) DO UPDATE set end_time=excluded.end_time;
"""

# DROP TABLES

school_table_drop = "DROP TABLE IF EXISTS school;"
school_name_log_table_drop = "DROP TABLE IF EXISTS school_name_log;"
device_table_drop = "DROP TABLE IF EXISTS device;"
device_assignment_log_table_drop = "DROP TABLE IF EXISTS device_assignment;"
student_session_table_drop = "DROP TABLE IF EXISTS student_session;"


# QUERY LISTS

create_table_queries = [
    # school_table_create,
    school_name_log_table_create,
    # device_table_create,
    device_assignment_log_table_create,
    student_session_table_create,
]
drop_table_queries = [
    school_table_drop,
    school_name_log_table_drop,
    device_table_drop,
    device_assignment_log_table_drop,
    student_session_table_drop,
]

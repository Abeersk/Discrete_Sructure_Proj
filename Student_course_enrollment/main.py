import streamlit as st
import sqlite3
from collections import defaultdict
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("courses.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        prerequisite TEXT,
        day TEXT,
        time TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        student TEXT,
        course TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HELPERS ----------------

def get_courses():
    conn = sqlite3.connect("courses.db")
    df = pd.read_sql_query("SELECT * FROM courses", conn)
    conn.close()
    return df


def get_student_courses(student):
    conn = sqlite3.connect("courses.db")
    c = conn.cursor()
    c.execute("SELECT course FROM enrollments WHERE student=?", (student,))
    data = [i[0] for i in c.fetchall()]
    conn.close()
    return data


def add_course(name, pre, day, time):
    conn = sqlite3.connect("courses.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO courses VALUES (NULL, ?, ?, ?, ?)",
                  (name, pre, day, time))
        conn.commit()
    except:
        pass
    conn.close()


def enroll(student, course):
    conn = sqlite3.connect("courses.db")
    c = conn.cursor()
    c.execute("INSERT INTO enrollments VALUES (?, ?)", (student, course))
    conn.commit()
    conn.close()

# ---------------- DS LOGIC ----------------

def check_prerequisite(course, completed, course_df):
    pre = course_df[course_df["name"] == course]["prerequisite"].values[0]

    if pre == "None" or pre == "":
        return True, "No prerequisite required"

    if pre in completed:
        return True, "Prerequisite satisfied"

    return False, f"Missing prerequisite: {pre}"


def check_conflict(course, selected, course_df):
    row = course_df[course_df["name"] == course].iloc[0]

    for c in selected:
        if c == course:   # 🔥 FIX: skip self
            continue

        other = course_df[course_df["name"] == c].iloc[0]

        if row["day"] == other["day"] and row["time"] == other["time"]:
            return False, f"Time conflict with {c}"

    return True, "No conflict"

def build_graph(df):
    graph = defaultdict(list)

    for _, row in df.iterrows():
        if row["prerequisite"] and row["prerequisite"] != "None":
            graph[row["prerequisite"]].append(row["name"])

    return graph


def draw_graph(df):
    G = nx.DiGraph()

    # nodes + edges
    for _, row in df.iterrows():
        course = row["name"]
        pre = row["prerequisite"]

        G.add_node(course)

        if pre and pre != "None":
            G.add_edge(pre, course)

    plt.figure(figsize=(8, 5))

    pos = nx.spring_layout(G, seed=42)

    nx.draw(
        G, pos,
        with_labels=True,
        node_color="lightblue",
        node_size=2500,
        arrows=True,
        font_size=10,
        font_weight="bold"
    )

    st.pyplot(plt)

# ---------------- UI ----------------

st.set_page_config(page_title="Course Enrollment System", layout="wide")

st.title("🎓 Student Course Enrollment System (DS Project)")

menu = st.sidebar.radio(
    "Menu",
    ["➕ Add Course", "📋 View Courses", "🧑 Student Enrollment", "📊 Graph View"]
)

df = get_courses()

# ---------------- ADD COURSE ----------------

if menu == "➕ Add Course":
    st.header("➕ Add New Course")

    name = st.text_input("Course Name")
    pre = st.text_input("Prerequisite (None if no prerequisite)")
    day = st.selectbox("Day", ["Mon", "Tue", "Wed", "Thu", "Fri"])
    time = st.selectbox("Time", ["9AM", "11AM", "2PM", "4PM"])

    if st.button("Add Course"):
        add_course(name, pre, day, time)
        st.success("Course added!")

# ---------------- VIEW COURSES ----------------

elif menu == "📋 View Courses":
    st.header("📚 All Courses")

    if df.empty:
        st.warning("No courses available")
    else:
        st.dataframe(df, use_container_width=True)

# ---------------- ENROLLMENT SYSTEM ----------------

elif menu == "🧑 Student Enrollment":
    st.header("🧑 Enrollment System")

    student = st.text_input("Student Name")

    if student:
        courses = df["name"].tolist()

        selected = st.multiselect("Select Courses", courses)

        completed = get_student_courses(student)

        st.write("Completed Courses:", completed)

        if st.button("Enroll"):

            results = []

            for course in selected:

                ok1, msg1 = check_prerequisite(course, completed, df)
                ok2, msg2 = check_conflict(course, selected, df)

                if ok1 and ok2:
                    enroll(student, course)
                    results.append(f"✅ {course} enrolled")
                else:
                    results.append(f"❌ {course}: {msg1} | {msg2}")

            for r in results:
                st.write(r)

# ---------------- GRAPH (DS CONCEPT) ----------------

elif menu == "📊 Graph View":
    st.header("📊 Course Dependency Graph (DS Visualization)")

    if df.empty:
        st.warning("No data")
    else:
        st.write("Directed Graph (Prerequisite Structure)")

        draw_graph(df)
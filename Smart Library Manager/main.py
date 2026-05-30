import streamlit as st
import sqlite3
import pandas as pd
from collections import Counter

# ---------------- DB SETUP ----------------

def init_db():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        author TEXT,
        year INTEGER,
        genre TEXT,
        tags TEXT,
        read INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- DB FUNCTIONS ----------------

def add_book(title, author, year, genre, tags, read):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    try:
        c.execute("""
        INSERT INTO books (title, author, year, genre, tags, read)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (title, author, year, genre, tags, int(read)))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def get_books():
    conn = sqlite3.connect("library.db")
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()
    return df


def delete_book(title):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE title=?", (title,))
    conn.commit()
    conn.close()


def toggle_read(title, current_status):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("UPDATE books SET read=? WHERE title=?", (int(not current_status), title))
    conn.commit()
    conn.close()

# ---------------- UI ----------------

st.set_page_config(page_title="📚 Smart Library System", layout="wide")
st.title("📚 Smart Library Manager ")

menu = st.sidebar.radio(
    "Navigation",
    ["➕ Add Book", "📖 View All Books", "🔍 Search Books", "📊 Analytics", "🎯 Recommendations"]
)

df = get_books()

# ---------------- ADD BOOK ----------------

if menu == "➕ Add Book":
    st.header("➕ Add New Book")

    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Year", 1000, 2100)
    genre = st.text_input("Genre")
    tags = st.text_input("Tags (comma separated)")
    read = st.checkbox("Mark as Read")

    if st.button("Add Book"):
        if title.strip():
            success = add_book(title, author, year, genre, tags, read)
            if success:
                st.success("Book added successfully!")
                st.rerun()
            else:
                st.error("Book already exists!")
        else:
            st.warning("Title is required")

# ---------------- VIEW ALL BOOKS (IMPORTANT FIX ADDED) ----------------

elif menu == "📖 View All Books":
    st.header("📚 All Books in Library")

    if df.empty:
        st.warning("No books found in library")
    else:
        st.dataframe(df, use_container_width=True)

        st.subheader("🛠 Manage Books")

        col1, col2 = st.columns(2)

        with col1:
            book_to_delete = st.selectbox("Delete Book", df["title"].tolist())
            if st.button("Delete Book"):
                delete_book(book_to_delete)
                st.success("Book deleted")
                st.rerun()

        with col2:
            book_to_toggle = st.selectbox("Toggle Read Status", df["title"].tolist(), key="toggle")

            if st.button("Update Read Status"):
                current = df[df["title"] == book_to_toggle]["read"].values[0]
                toggle_read(book_to_toggle, current)
                st.success("Updated read status")
                st.rerun()

# ---------------- SEARCH BOOKS (FIXED + IMPROVED) ----------------

elif menu == "🔍 Search Books":
    st.header("🔍 Search Books")

    query = st.text_input("Search by Title or Author")

    if query:
        results = df[
            df["title"].str.contains(query, case=False, na=False) |
            df["author"].str.contains(query, case=False, na=False)
        ]

        if not results.empty:
            st.success(f"Found {len(results)} book(s)")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("No books found")

# ---------------- ANALYTICS ----------------

elif menu == "📊 Analytics":
    st.header("📊 Library Insights Dashboard")

    if df.empty:
        st.warning("No data available")
    else:
        st.subheader("Genre Distribution")
        st.bar_chart(df["genre"].value_counts())

        total = len(df)
        read = df["read"].sum()
        unread = total - read

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Books", total)
        col2.metric("Read", read)
        col3.metric("Unread", unread)

        st.progress(read / total if total else 0)

# ---------------- RECOMMENDATIONS (DS LOGIC) ----------------

elif menu == "🎯 Recommendations":
    st.header("🎯 Smart Recommendations")

    if df.empty:
        st.warning("No books available")
    else:
        genre_count = Counter(df["genre"])
        top_genre = genre_count.most_common(1)[0][0]

        st.info(f"Top Genre: {top_genre}")

        recs = df[(df["genre"] == top_genre) & (df["read"] == 0)]

        if not recs.empty:
            st.dataframe(recs)
        else:
            st.warning("No recommendations available (you read all in this genre!)")
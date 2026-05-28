import datetime
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# Create a SQLite database and table
# data.db will be created in Google Clound Bucket => each app needs different database name
# or have to create different bucket
conn = sqlite3.connect('data/microblog2.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        date TEXT
    )
''')
conn.commit()
conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            # check if entry_content =""
            if (entry_content == ""):
                print('Empty content! Returning to home page without saving')
                return redirect(url_for('home'))
            else:     
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
                # Insert user into the database
                conn = sqlite3.connect('data/microblog2.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO entries (content, date) VALUES (?, ?)', (entry_content, formatted_date))
                conn.commit()
                conn.close()
                return redirect(url_for('home'))
        # else GET method, read data
        conn = sqlite3.connect('data/microblog2.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM entries')
        entries = cursor.fetchall()
        for e in entries:
             print(e[0], e[1], e[2])
        
        entries_with_date = [
            (
                entry[0], #entry[0] = id
                entry[1], #entry[1] = content
                entry[2], #entry[2] = datetime
                datetime.datetime.strptime(entry[2], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in entries
        ]
        return render_template("home.html", entries=entries_with_date)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_entry(id):
    
    conn = sqlite3.connect('data/microblog2.db')
    cursor = conn.cursor()

    if request.method == "POST":
        new_content = request.form.get("content")

        cursor.execute(
            "UPDATE entries SET content = ? WHERE id = ?",
            (new_content, id),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    # GET request → load existing entry
    cursor.execute("SELECT id, content FROM entries WHERE id = ?", (id,))
    entry = cursor.fetchone()
    conn.close()

    return render_template("edit.html", entry=entry)


@app.route("/delete/<int:id>")
def delete_entry(id):
    
    conn = sqlite3.connect('data/microblog2.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

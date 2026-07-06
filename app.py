import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "the-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///microblog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# check if database exists, if not create
with app.app_context():
    if not os.path.exists("microblog.db"):
        db.create_all()

# model the Task database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Post {self.content}>'



# Create a SQLite database and table
# data.db will be created in Google Clound Bucket => each app needs different database name
# or have to create different bucket
# conn = sqlite3.connect('data/microblog2.db')
# cursor = conn.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS entries (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         content TEXT,
#         date TEXT
#     )
# ''')
# conn.commit()
# conn.close()


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
                post = Post(content=entry_content, date=formatted_date)
                db.session.add(post)
                db.session.commit()

                return redirect(url_for('home'))
        # else GET method, read data
        
        entries = Post.query.all()
        for e in entries:
             print(e.content, e.date)
        
        entries_with_date = [
            (
                entry.id, #entry[0] = id
                entry.content, #entry[1] = content
                entry.date, #entry[2] = datetime
                datetime.datetime.strptime(entry.date, "%Y-%m-%d").strftime("%b %d")
            )
            for entry in entries
        ]
        return render_template("home.html", entries=entries_with_date)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_entry(id):
    
    entry = Post.query.get_or_404(id)

    if request.method == "POST":
        new_content = request.form.get("content")

        entry.content = new_content
        db.session.commit()
        return redirect(url_for("home"))

    # GET request → load existing entry

    return render_template("edit.html", entry=entry)


@app.route("/delete/<int:id>")
def delete_entry(id):
    
    entry = Post.query.get_or_404(id)
    if entry:
        db.session.delete(entry)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

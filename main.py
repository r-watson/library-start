from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

all_books = []

### Create sqlite3 database and add row. ###
# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT OR IGNORE INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

## Create flask_sqlalchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a new table inside of the database
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    def __repr__(self):
        return f'<Book {self.title}>'

db.create_all()

# Create a new row inside the table
# hpotter = Book(id=1, title='Harry Potter', author='J.K. Rowling', rating=9.3)
# db.session.add(hpotter)
# db.session.commit()



# Create a new row inside the table. PRIMARY KEY is optional. It will be created automatically.
# hpotter = Book(title='Harry Potter', author='J.K. Rowling', rating=9.3)
# db.session.add(hpotter)
# db.session.commit()

#Read all records
# all_books = Book.query.all()
# print(all_books)

#Read a particular record
# book = Book.query.filter_by(title="Harry Potter").first()
# print(book)

#Update a particular record
# book_to_update = Book.query.filter_by(title="Harry Potter").first()
# print(book_to_update)
# book_to_update.title = "Harry Potter and the Chamber of Secrets"
# db.session.commit()

# #Update a record by PRIMARY KEY
# book_id = 1
# book_to_update = Book.query.get(book_id)
# book_to_update.title = "Harry Potter and the Goblet of Fire"
# db.session.commit()

# Delete a record by PRIMARY KEY
# book_id = 1
# book_to_delete = Book.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()



@app.route('/')
def home():
    # Read all records
    books = db.session.query(Book).all()
    return render_template("index.html", all_books=books)


@app.route("/add", methods=("GET", "POST"))
def add():
    if request.method == 'POST':
        book = request.form['book']
        author = request.form['author']
        rating = request.form['rating']

        # Add book to database
        new_book = Book(title=book, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=("GET", "POST"))
def edit():
    if request.method == 'POST':
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        new_rating = request.form['rating']
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for("home"))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit.html", book=book_selected)

@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
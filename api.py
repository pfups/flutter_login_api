from flask import Flask,request,jsonify, request, render_template,g,redirect,url_for, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pymysql.cursors
import pymysql


app = Flask(__name__)
#app.config.from_pyfile('config.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql3425837:UL9lKxdYAV@sql3.freemysqlhosting.net/sql3425837'
db = SQLAlchemy(app)

# this class is for creating tables in db
class uscis_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route("/login",methods=["GET", "POST"])
def login():
    d = {}
    if request.method == "POST":
        new_user_data = request.get_json()
        username = new_user_data['username']
        password = new_user_data['password']
        
        login = uscis_users.query.filter_by(username=username, password=password).first()

        if login is not None:
            # account found
            d["status"] = 11
            return jsonify(d)
        else:
            # account not exist
            d["status"] = 22
            return jsonify(d) 

@app.route("/register", methods=["GET", "POST"])
def register():
        d = {} 
        new_user_data = request.get_json()
        username = new_user_data['username']
        email = new_user_data['email']
        password = new_user_data['password']
        name = uscis_users.query.filter_by(username=username).first()
        if name is None:
            user = uscis_users(username = [username], email = [email], password =  [password])
            db.session.add(user)
            db.session.commit()
            return jsonify(d)
        else:
            # already exist
            d["status"] = 22
            return jsonify(d)  
        
        return 'The username is {}, the email is {}, the password is {}'.format(username, email, password)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
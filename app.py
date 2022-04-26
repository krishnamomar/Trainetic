from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(host="localhost", user="root", passwd="AbCd@123", database="railway_system")
mycursor = mydb.cursor()

global current_user;
current_user = 0;

@app.route('/')
def hello_world():  # put application's code here
    current_user = 0;
    return render_template("index.html");


@app.route('/admin_login')
def admin_log():
    return render_template("admin_log.html");


@app.route('/user_login')
def user_log():
    current_user = 0;
    return render_template("user_login.html");


@app.route('/Registration_screen')
def user_register():
    return render_template("Registration_screen.html");

@app.route('/admin_station')
def admin_station():
    return render_template("admin_station.html");

@app.route('/admin_seats')
def admin_seats():
    return render_template("admin_seats.html");

@app.route('/admin_afterlogin')
def admin_afterlogin():
    return render_template("admin_afterlogin.html");

@app.route('/About_us')
def aboutuspage():
    return render_template("about_us.html");


@app.route('/Contact_us')
def contact_us():
    return render_template("contact_us.html");


@app.route('/Browse_trains')
def browse_train():
    return render_template("browse_trains.html");


@app.route('/user_info', methods= ["POST", "GET"])
def user_info():
    if (request.method == "GET"):
        return render_template("user_login.html");

    else:
        print(request.form)
        u_adhaar = request.form["adhaar"]
        u_password = request.form["password"]

        chk_adh_str = f"SELECT * FROM users WHERE Adhaar_no='{u_adhaar}';"
        mycursor.execute(chk_adh_str);
        now_user_data_all = mycursor.fetchall();
        if (len(now_user_data_all)==0):
            return render_template("user_login.html");

        now_user_data = now_user_data_all[0];

        if now_user_data[7]!=u_password:
            return render_template("user_login.html");

        current_user = u_adhaar;

        return render_template("user_info.html", user_data = now_user_data);

@app.route('/registered', methods= ["POST", "GET"])
def regis_ok():
    if (request.method=="GET"):
        return render_template("Registration_screen.html");
    else:
        r_adhaar = request.form["adhaar"]
        r_password = request.form["password"]
        r_firstname = request.form["first_name"]
        r_lastname = request.form["last_name"]
        r_dob = request.form["DOB"]
        r_phone = request.form["phone_no"]
        r_username = request.form["username"]
        r_email = request.form["email"]
        # exc_str = f"INSERT INTO users(Adhaar_no,Username,e_mail,Mobile,DOB,First_name,Last_name,password) VALUES ({r_adhaar},'{r_username}','{r_email}',{r_phone},'{r_dob}','{r_firstname}','{r_lastname}','{r_password}');"
        # if len(r_phone)==0: render_template("Registration_screen.html");
        # if r_dob is None: render_template("Registration_screen.html");
        chk_adh_str = f"SELECT * FROM users WHERE Adhaar_no='{r_adhaar}';"
        if len(chk_adh_str)>0:
            return render_template("user_login.html");
        exc_str = f"INSERT INTO users(Adhaar_no,Username,e_mail,Mobile,DOB,First_name,Last_name,passwords) VALUES({str(r_adhaar)}, '{r_username}', '{r_email}', {str(r_phone)}, '{r_dob}', '{r_firstname}', '{r_lastname}', '{r_password}');"
        print(exc_str);
        mycursor.execute(exc_str);
        # useless = mycursor.fetchall();
        mydb.commit();

        # print("INSERT INTO users(Adhaar_no,Username,e_mail,Mobile,DOB,First_name,Last_name,password) VALUES({}, '{}', '{}', {}, '{}', '{}', '{}', '{}');".format(r_adhaar,r_username,r_email,r_phone,r_dob,r_firstname,r_lastname,r_password))

        return render_template("registered.html");

@app.route('/station_added')
def congo_station():
    return render_template("station_added.html");


if __name__ == '__main__':
    app.run()

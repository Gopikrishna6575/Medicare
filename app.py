from flask import Flask, redirect, url_for, render_template, request, flash, session
from mysql.connector.pooling import MySQLConnectionPool
from key import secret_key, salt, salt2 , salt3 , salt4
from flask_bcrypt import Bcrypt
from sendmail import send_email
from ctoken import gen_otp, create_token, verify_token

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

bcrypt = Bcrypt(app)

conn = MySQLConnectionPool(host='localhost', user='root', password='Gopi@4211', db='db', pool_name='login', pool_size=3, pool_reset_session=True)


try:
    mydb = conn.get_connection()
    cursor = mydb.cursor(buffered=True)
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
        admin_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(25) UNIQUE NOT NULL,
        email VARCHAR(55) UNIQUE NOT NULL,
        password VARCHAR(200) NOT NULL
        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    patient_disease VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    admit_date DATE
    ) AUTO_INCREMENT = 20240001''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS Doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    specialization VARCHAR(255) NOT NULL,
    `from_time` TIME DEFAULT '10:00:00',
    `to_time` TIME DEFAULT '21:00:00'
    ) AUTO_INCREMENT=20200001''')





    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone varchar(20) not null,
    email VARCHAR(255) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    suffering_with VARCHAR(255) NOT NULL,
    doctor_id int  NOT NULL, foreign key(doctor_id) references doctors(doctor_id))''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PatientMedicineUsage (
        patient_id INT NOT NULL,
        admit_date DATE,
        discharged_on DATE,
        notes TEXT,
        injection_name VARCHAR(255),
        injection_cost DECIMAL(10, 2) DEFAULT 0,
        injection_dosage INT DEFAULT 0,
        tablet_name VARCHAR(255),
        tablet_cost DECIMAL(10, 2) DEFAULT 0,
        tablet_dosage INT DEFAULT 0,
        room_used INT DEFAULT 0,
        icu_used INT DEFAULT 0,
        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id))''')


    
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctors_request (
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(20) NOT NULL,
        specialization VARCHAR(255) NOT NULL)''')
    

    cursor.close()
except Exception as e:
    print(e)
finally:
    if mydb.is_connected():
        mydb.close()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# @app.route('/admin_password',methods=['GET','POST'])
# def admin_password():
#     if request.method == 'POST':
#         password=request.form['password'].strip()
#         result={'password':password}
#         encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         try:
#             mydb=conn.get_connection()
#             cursor=mydb.cursor()
#             cursor.execute('select * from passwords')
#             pword=cursor.fetchone()[0]
#             if password == pword:
#                 return render_template('signup.html')
#             else:
#                 flash('password was incorrect')
#                 return redirect(url_for('home'))
#         except Exception as e:
#             print(e)
#         finally:
#             if mydb.is_connected():
#                 cursor.close()
#                 mydb.close()
#     return render_template('admin_password.html')

#admin registration functionalities
@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if session.get('user'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
        otp = gen_otp()
        result = {'username': username, 'email': email, 'password': encrypted_password, 'otp': otp}
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select count(*) from admin where email=%s', (result['email'],))
            email_id = cursor.fetchone()[0]
            cursor.execute('select count(*) from admin where username=%s', (result['username'],))
            user_name = cursor.fetchone()[0]
            if email_id == 1 or user_name == 1:
                flash("Email or username already exists")
                return render_template('signup.html')
            else:
                subject = 'Verify your OTP to register your details'
                body = f'Dear user, please use this OTP to register your details: {otp}'
                send_email(receiver_email=result['email'], subject=subject, body=body)
                flash("OTP sent successfully! Please verify to register")
                return redirect(url_for('otp', token=create_token(result, salt=salt)))
        except Exception as e:
            print(e)
        finally:
            if mydb.is_connected():
                mydb.close()
    return render_template('signup.html')


@app.route('/otp/<token>', methods=['POST', 'GET'])
def otp(token):
    result = verify_token(token, salt=salt, expire=300)
    if request.method == 'POST':
        uotp = request.form['otp']
        if result:
            if result['otp'] == uotp:
                try:
                    mydb = conn.get_connection()
                    cursor = mydb.cursor(buffered=True)
                    cursor.execute('select count(*) from admin where email = %s', (result['email'],))
                    email_id = cursor.fetchone()[0]
                    if email_id == 1:
                        flash('User already logged in! Please login to continue')
                        return redirect(url_for('admin_login'))
                    else:
                        cursor.execute('insert into admin(username,email,password) values (%s,%s,%s)', (result['username'], result['email'], result['password']))
                        mydb.commit()
                        cursor.close()
                        flash('Details registered successfully')
                        return redirect(url_for('admin_login'))
                except Exception as e:
                    print(e)
                finally:
                    if mydb.is_connected():
                        cursor.close()
                        mydb.close()
            else:
                flash('OTP entered was incorrect')
                return render_template('otp.html', token=token)
    else:
        return render_template('otp.html', token=token)


@app.route('/login', methods=['POST', 'GET'])
def admin_login():
    if session.get('user'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = {'username': username, 'password': password}
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select count(*),password from admin where username=%s', (data['username'],))
            user_name, encrypted_password = cursor.fetchone()
            if user_name == 1:
                if bcrypt.check_password_hash(encrypted_password, data['password']):
                    session['user'] = data['username']
                    flash('Login successful')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Username or password was incorrect')
                    return render_template('login.html')
            else:
                flash('Username was not found. Please register with your email')
                return redirect(url_for('admin_signup'))
        except Exception as e:
            print(e)
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
    else:
        return render_template('login.html')

@app.route('/forget', methods=['POST', 'GET'])
def forget():
    if request.method == 'POST':
        email = request.form['email']
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select count(*) from admin where email=%s', (email,))
            email_id = cursor.fetchone()[0]
            if email_id == 1:
                token_url = url_for('verify', token=create_token(email, salt=salt2), _external=True)
                subject = 'Password reset link'
                body = f'Dear user,\nUse the below link to reset your password:\n{token_url}'
                send_email(receiver_email=email, subject=subject, body=body)
                flash('Reset link has been sent successfully to your email')
                return redirect(url_for('admin_login'))
            else:
                flash('User not registered or invalid email')
                return render_template('forget.html')
        except Exception as e:
            print(e)
            return 'Error occurred'
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
    else:
        return render_template('forget.html')

@app.route('/verify/<token>', methods=['POST', 'GET'])
def verify(token):
    email = verify_token(token=token, salt=salt2, expire=600)
    if email:
        if request.method == 'POST':
            new_pass = request.form['npassword']
            c_pass = request.form['cpassword']
            if new_pass == c_pass:
                try:
                    mydb = conn.get_connection()
                    cursor = mydb.cursor(buffered=True)
                    encrypted_password = bcrypt.generate_password_hash(new_pass).decode('utf-8')
                    cursor.execute('update admin set password=%s where email=%s', (encrypted_password, email))
                    mydb.commit()
                    flash('Password reset successfully')
                    return redirect(url_for('admin_login'))
                except Exception as e:
                    print(e)
                finally:
                    if mydb.is_connected():
                        cursor.close()
                        mydb.close()
            else:
                flash('Both passwords should be the same')
                return redirect(url_for('verify', token=token))
        else:
            return render_template('verify.html',token=token)
    else:
        flash('Link expired')
        return redirect(url_for('forget'))

#admin Dashboard functionalities
@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('user'):
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('admin_login'))

@app.route('/all_patients')
def all_patients():
    if session.get('user'):
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT * FROM patients')
            rows = cursor.fetchall()
            # Transform each row into a dictionary
            patient_details = [dict(zip(cursor.column_names, row)) for row in rows]
            return render_template('patient_view.html', patient_details=patient_details)
        except Exception as e:
            print(e)
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
    else:
        return redirect(url_for('home'))
    return redirect(url_for('admin_dashboard'))

@app.route('/all_doctors')
def all_doctors():
    if session.get('user'):
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT * FROM doctors_request')
            rows = cursor.fetchall()
            # Transform each row into a dictionary
            doctor_details = [dict(zip(cursor.column_names, row)) for row in rows]
            cursor.execute("Select email from doctors")
            email_data = cursor.fetchall()
            emails = []
            for email in email_data:
                emails.append(email[0])
            print(emails)
            return render_template('doctor_view.html', doctor_details=doctor_details,emails=emails)
        except Exception as e:
            print(e)
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
        return redirect(url_for('all_doctors'))
    else:
        return redirect(url_for('admin_login'))
     
@app.route('/all_appointments')
def all_appointments():
    if session.get('user'):
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True,dictionary=True)
            cursor.execute('select a.name as patient_name,a.phone,a.email,a.appointment_date,a.appointment_time,a.suffering_with,d.name as doctor_name from appointments as a left join doctors as d on a.doctor_id=d.doctor_id')
            appointment_details= cursor.fetchall()
            # Transform each row into a dictionary
            #appointment_details = [dict(zip(cursor.column_names, row)) for row in rows]
            return render_template('appointment_view.html', appointment_details=appointment_details)
        except Exception as e:
            print(e)
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
    else:
        return redirect(url_for('admin_login'))

@app.route('/patient_registration',methods=['POST','GET'])
def patient_registration():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        phone=request.form['phone']
        dob=request.form['dob']
        gender=request.form['gender']
        patient_disease=request.form['patient_disease'] 
        address=request.form['address']
        admit_date=request.form['admit_date']
        encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            #cursor.execute('select * from patients')
            # doctor_data=cursor.fetchall()
            cursor.execute('SELECT COUNT(*) FROM Patients WHERE email=%s', (email,))
            email_count = cursor.fetchone()[0]
            if email_count == 1:
                flash("Email already exists")
                return render_template('patient_registration.html')
            else:
                cursor.execute('INSERT INTO Patients (name, email, password, phone, dob, gender, patient_disease,admit_date, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s , %s)',
                               (name, email, encrypted_password, phone, dob, gender, patient_disease,admit_date, address))
                mydb.commit()  # Commit the transaction after insertion

                # Send email with credentials
                subject = 'Login Credentials'
                body = f'Dear {name},\n\nPlease use these credentials to log in to your account:\nEmail: {email}\nPassword: {password}\n\nBest regards,\nYour Healthcare Team'
                send_email(receiver_email=email, subject=subject, body=body)

                flash("Credentials sent successfully! Please use them to log in.")
                return render_template('admin_dashboard.html')

        except Exception as e:
            print(e)
            flash("An error occurred during registration.")
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()

    return render_template('patient_registration.html')

@app.route('/doctor_registration',methods=['POST','GET'])
def doctor_registration():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        phone=request.form['phone']
        specialization=request.form['specialization']
        # from_time=request.form['from_time']
        # to_time=request.form['to_time']
        data={'name':name,'email':email,'password':password,'phone':phone,'specialization':specialization}
        encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT COUNT(*) FROM Doctors WHERE email=%s', (email,))
            email_count = cursor.fetchone()[0]
            if email_count == 1:
                session['doctor'] = data['name']
                flash("Email already exists")
                return render_template('doctor_registration.html')
            else:
                cursor.execute('INSERT INTO doctors (name, email, password, phone, specialization) VALUES (%s, %s, %s, %s, %s)',(name, email, encrypted_password, phone,specialization))
                mydb.commit()  # Commit the transaction after insertion

                # Send email with credentials
                subject = 'Login Credentials'
                body = f'Dear {name},\n\nPlease use these credentials to log in to your account:\nEmail: {email}\nPassword: {password}\n\nBest regards,\nYour Healthcare Team'
                send_email(receiver_email=email, subject=subject, body=body)

                flash("Credentials sent successfully! Please use them to log in.")
                return render_template('admin_dashboard.html')

        except Exception as e:
            print(e)
            flash("An error occurred during registration.")
            return render_template('error.html')
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()

    return render_template('doctor_registration.html')


@app.route('/patient_medicine_usage', methods=['GET', 'POST'])
def patient_medicine():
    if session.get('user'):
        if request.method == 'POST':
            patient_id = request.form['patient_id']
            admit_date = request.form['admit_date']
            discharged_on = request.form['discharged_on']
            notes = request.form['notes']
            injection_name = request.form['injection_name']
            injection_cost = request.form['injection_cost']
            injection_dosage = request.form['injection_dosage']
            tablet_name = request.form['tablet_name']
            tablet_cost = request.form['tablet_cost']
            tablet_dosage = request.form['tablet_dosage']
            room_used = request.form['room_used']
            icu_used = request.form['icu_used']
            try:
                mydb = conn.get_connection()
                cursor = mydb.cursor(buffered=True)
                cursor.execute('''
                    INSERT INTO patientmedicineusage (patient_id, admit_date, discharged_on, notes,
                    injection_name, injection_cost, injection_dosage,
                    tablet_name, tablet_cost, tablet_dosage, room_used, icu_used)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                               (patient_id, admit_date, discharged_on, notes,
                                injection_name, injection_cost, injection_dosage,
                                tablet_name, tablet_cost, tablet_dosage,
                                room_used, icu_used))
                mydb.commit()
                flash('Details updated successfully')
                return redirect(url_for('admin_dashboard'))
            except Exception as e:
                print(e)
            finally:
                if mydb.is_connected():
                    cursor.close()
                    mydb.close()
        return render_template('patient_medicine_usage.html')
    else:
        return redirect(url_for('home'))


@app.route('/view_more/<int:patient_id>')
def view_more(patient_id):
    if session.get('user'):
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT * FROM patientmedicineusage WHERE patient_id = %s', (patient_id,))
            details = cursor.fetchall()
            if not details:
                flash('patient was yet to discharge')
                return redirect(url_for('admin_dashboard'))
            return render_template('patient_medicine.html', details=details)
        except Exception as e:
            print("MySQL Error:", e)
            # Log the error or handle it appropriately
            return render_template('error.html', message="Database error occurred. Please try again later.")
        except Exception as e:
            print("Error:", e)
            # Log the error or handle it appropriately
            return render_template('error.html', message="An unexpected error occurred. Please try again later.")
        finally:
            if 'mydb' in locals() and mydb.is_connected():
                cursor.close()
                mydb.close()
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('home'))

#patient's functionalities
    
@app.route('/patient_dashboard')
def pdashboard():
    if session.get('patient'):
        return render_template('patient_dashboard.html')
    else:
        return redirect(url_for('patient_login'))
    
@app.route('/patient_login',methods=['POST','GET'])
def patient_login():
    if session.get('patient'):
        return redirect(url_for('pdashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = {'email': email, 'password': password}

        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select count(*),password,patient_id from patients where email=%s', (data['email'],))
            user_email, encrypted_password ,patient_id= cursor.fetchone()
            if user_email == 1:
                if bcrypt.check_password_hash(encrypted_password, data['password']):
                    session['patient'] = data['email']
                    session['patient_id'] = patient_id
                    flash('Login successful')
                    return render_template('patient_dashboard.html')
                else:
                    flash('Username or password was incorrect')
                    return render_template('patient_login.html')
            else:
                flash('Username was not found. Please ask in the reception')
                return render_template('error.html')
        except Exception as e:
            print(e)
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
    return render_template('patient_login.html')  # Added return statement here

@app.route('/patient_forget', methods=['POST', 'GET'])
def patient_forget():
    if request.method == 'POST':
        email = request.form['email']
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select count(*) from patients where email=%s', (email,))
            email_id = cursor.fetchone()[0]
            if email_id == 1:
                token_url = url_for('patient_verify', token=create_token(email, salt=salt3), _external=True)
                subject = 'Password reset link'
                body = f'Dear user,\nUse the below link to reset your password:\n{token_url}'
                send_email(receiver_email=email, subject=subject, body=body)
                flash('Reset link has been sent successfully to your email')
                return redirect(url_for('patient_login'))
            else:
                flash('User not registered or invalid email')
                return render_template('patient_forget.html')
        except Exception as e:
            print(e)
            return 'Error occurred'
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
    else:
        return render_template('patient_forget.html')

@app.route('/patient_verify/<token>', methods=['POST', 'GET'])
def patient_verify(token):
    email = verify_token(token=token, salt=salt3, expire=600)
    if email:
        if request.method == 'POST':
            new_pass = request.form['npassword']
            c_pass = request.form['cpassword']
            if new_pass == c_pass:
                try:
                    mydb = conn.get_connection()
                    cursor = mydb.cursor(buffered=True)
                    encrypted_password = bcrypt.generate_password_hash(new_pass).decode('utf-8')
                    cursor.execute('update patients set password=%s where email=%s', (encrypted_password, email))
                    mydb.commit()
                    flash('Password reset successfully')
                    return redirect(url_for('patient_login'))
                except Exception as e:
                    print(e)
                finally:
                    if mydb.is_connected():
                        cursor.close()
                        mydb.close()
            else:
                flash('Both passwords should be the same')
                return redirect(url_for('patient_verify', token=token))
        else:
            return render_template('patient_verify.html',token=token)
    else:
        flash('Link expired')
        return redirect(url_for('patient_forget'))






@app.route('/patient_prescription/')
def patient_prescription():
    if session.get('patient'):
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            patient_id = session.get('patient_id')
            cursor.execute('SELECT * FROM patientmedicineusage WHERE patient_id = %s', (patient_id,))
            details = cursor.fetchall()
            if not details:
                flash('patient was yet to discharge')
                return redirect(url_for('patient_dashboard'))
            return render_template('patient_priscription.html', details=details)
        except Exception as e:
            print("Error:", e)
            # Log the error or handle it appropriately
            return render_template('error.html', message="An unexpected error occurred. Please try again later.")
        finally:
            if  mydb.is_connected():
                cursor.close()
                mydb.close()
        return redirect(url_for('patient_dashboard'))
    else:
        return redirect(url_for('patient_login'))



#doctor's functionalities


@app.route('/doctor_login', methods=['POST', 'GET'])
def doctor_login():
    if session.get('doctor'):
        return redirect(url_for('doctor_dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = {'email': email, 'password': password}
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT count(*), password,doctor_id FROM doctors WHERE email=%s', (data['email'],))
            email_user, encrypted_password,doctor_id = cursor.fetchone()
            if email_user == 1:
                if bcrypt.check_password_hash(encrypted_password, data['password']):
                    session['doctor'] = doctor_id
                    print('login successful')
                    flash('Login successful')
                    return redirect(url_for('doctor_dashboard'))  # Redirect to doctor dashboard
                else:
                    flash('Username or password was incorrect')
                    return render_template('doctor_login.html')
            else:
                flash('Email was not found. Please ask in the reception')
                return render_template('doctor_login.html')
        except Exception as e:
            print(e)
            flash('An error occurred. Please try again later.')
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()

    return render_template('doctor_login.html')

@app.route('/doctor_forget', methods=['POST', 'GET'])
def doctor_forget():
    if request.method == 'POST':
        email = request.form['email']
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select count(*) from doctors where email=%s', (email,))
            email_id = cursor.fetchone()[0]
            if email_id == 1:
                token_url = url_for('doctor_verify', token=create_token(email, salt=salt4), _external=True)
                subject = 'Password reset link'
                body = f'Dear user,\nUse the below link to reset your password:\n{token_url}'
                send_email(receiver_email=email, subject=subject, body=body)
                flash('Reset link has been sent successfully to your email')
                return redirect(url_for('doctor_login'))
            else:
                flash('User not registered or invalid email')
                return render_template('doctor_forget.html')
        except Exception as e:
            print(e)
            return 'Error occurred'
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
    else:
        return render_template('doctor_forget.html')

@app.route('/doctor_verify/<token>', methods=['POST', 'GET'])
def doctor_verify(token):
    email = verify_token(token=token, salt=salt4, expire=600)
    if email:
        if request.method == 'POST':
            new_pass = request.form['npassword']
            c_pass = request.form['cpassword']
            if new_pass == c_pass:
                try:
                    mydb = conn.get_connection()
                    cursor = mydb.cursor(buffered=True)
                    encrypted_password = bcrypt.generate_password_hash(new_pass).decode('utf-8')
                    cursor.execute('update doctors set password=%s where email=%s', (encrypted_password, email))
                    mydb.commit()
                    flash('Password reset successfully')
                    return redirect(url_for('doctor_login'))
                except Exception as e:
                    print(e)
                finally:
                    if mydb.is_connected():
                        cursor.close()
                        mydb.close()
            else:
                flash('Both passwords should be the same')
                return redirect(url_for('doctor_verify', token=token))
        else:
            return render_template('doctor_verify.html',token=token)
    else:
        flash('Link expired')
        return redirect(url_for('doctor_forget'))


@app.route('/doctor_dashboard')
def doctor_dashboard():
    if session.get('doctor'):
        return render_template('doctor_dashboard.html')
    else:
        return redirect(url_for('doctor_login'))


@app.route('/doctor_appointments')
def doctor_appointments():
    if session.get('doctor'):
        doctor_id = session.get('doctor')
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True,dictionary=True)
            cursor.execute('SELECT * FROM appointments WHERE doctor_id = %s', (doctor_id,))
            appointments = cursor.fetchall()
            return render_template('doctor_appointments.html', appointments=appointments)
        except Exception as e:
            print(e)
            flash("An error occurred while fetching doctor's appointments.")
            return render_template('error.html')
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
        # return render_template('doctor_appointments.html')
    else:
        return redirect(url_for('doctor_login'))

@app.route('/update_doctor_timings/', methods=['GET', 'POST'])
def doctor_timing():
    if session.get('doctor'):
        doctor_id = session.get('doctor')
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute("Select from_time,to_time from doctors where doctor_id=%s",(doctor_id,))
            timings = cursor.fetchone()
            if request.method == 'POST':
                from_time = request.form['from_time']
                to_time = request.form['to_time']
                data = {'from_time': from_time, 'to_time': to_time}
                
                cursor.execute('UPDATE doctors SET from_time=%s, to_time=%s WHERE doctor_id=%s',
                            (from_time, to_time, doctor_id,))
                mydb.commit()
                flash('Time updated successfully')
                return render_template('doctor_dashboard.html')
            return render_template('update_timings.html',timings=timings)
        except Exception as e:
            print(e)
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
        return redirect(url_for('doctor_dashboard'))
    else:
        return redirect(url_for('doctor_login'))

        



    



#appointments

@app.route('/appointments')
def appointments():
    return render_template('appointments_dashboard.html')

@app.route('/book_appointments', methods=['GET', 'POST'])
def book_appointments():
    try:
        mydb = conn.get_connection()
        cursor = mydb.cursor(buffered=True)
        cursor.execute("Select doctor_id,name from doctors")
        doctors_details = cursor.fetchall()
        print(doctors_details)
        if request.method == 'POST':
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            appointment_time = request.form['appointment_time']
            appointment_date = request.form['appointment_date']
            suffering_with = request.form['suffering_with']
            doctor_id = int(request.form['doctor_id'].strip())

            # Data validation and conflict check
           
            cursor.execute('SELECT * FROM appointments WHERE appointment_time=%s AND appointment_date=%s AND doctor_id=%s', (appointment_time, appointment_date, doctor_id))
            conflicting_appointments = cursor.fetchall()

            if conflicting_appointments:
                flash('This time slot is already booked for the appointment. Please choose another time slot.')
                return render_template('appointments.html',doctors_details=doctors_details)
            else:
                cursor.execute('INSERT INTO appointments (name, phone, email, appointment_time, appointment_date, suffering_with, doctor_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', (name, phone, email, appointment_time, appointment_date, suffering_with, doctor_id))
                mydb.commit()

                # Send email with credentials
                subject = 'Appointment Confirmation'
                body = f'Dear {name},\n\nYour appointment has been successfully booked.\n\nAppointment details:\nDate: {appointment_date}\nTime: {appointment_time}\nDoctor: {doctor_id}\n\nThank you for choosing our services.\n\nBest regards,\nYour Healthcare Team'
                send_email(receiver_email=email, subject=subject, body=body)

                flash('Appointment booked successfully. Confirmation email has been sent to your email address.')
                return render_template('appointments_dashboard.html')
        return render_template('appointments.html',doctors_details=doctors_details)

    except Exception as e:
        print(e)  # Log the exception for debugging purposes
        flash('An error occurred during booking appointment.')
        return render_template('error.html')

    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()


    

@app.route('/doctors')
def doctors():
    try:
        mydb = conn.get_connection()
        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT * FROM doctors')
        rows = cursor.fetchall()
        # Transform each row into a dictionary
        doctor_details = [dict(zip(cursor.column_names, row)) for row in rows]
        return render_template('timings.html', doctor_details=doctor_details)
    except Exception as e:
        print(e)
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()

    return render_template('appointments_dashboard.html')

#doctors request
@app.route('/doctor_request',methods=['POST','GET'])
def doctor_request():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        specialization=request.form['specialization']
        # from_time=request.form['from_time']
        # to_time=request.form['to_time']
        data={'name':name,'email':email,'phone':phone,'specialization':specialization}
        #encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT COUNT(*) FROM doctors_request WHERE email=%s', (email,))
            email_count = cursor.fetchone()[0]
            if email_count == 1:
                flash(" already request for account")
                return render_template('doctor_request.html')
            else:
                cursor.execute('INSERT INTO doctors_request (name, email,  phone, specialization) VALUES (%s, %s, %s, %s)',(name, email,phone,specialization))
                mydb.commit()  # Commit the transaction after insertion

                # Send email with credentials
                # subject = 'Login Credentials'
                # body = f'Dear {name},\n\nPlease use these credentials to log in to your account:\nEmail: {email}\nPassword: {password}\n\nBest regards,\nYour Healthcare Team'
                # send_email(receiver_email=email, subject=subject, body=body)

                # flash("Credentials sent successfully! Please use them to log in.")
                return redirect(url_for('home'))

        except Exception as e:
            print(e)
            flash("An error occurred during registration.")
            return render_template('error.html')
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()

    return render_template('doctor_request.html')

@app.route('/reject_doctor/<email>')
def reject(email):  # Added function parameter for email
    if session.get('user'):
        try:
            mydb=conn.get_connection()
            cursor=mydb.cursor()
            cursor.execute('delete from doctors_request where email=%s',(email,))
            mydb.commit()
            flash('rejected the doctor')
            # Send email with credentials
            subject = 'adimn rejected your request'
            body = f'Dear doctor,\n\nwe are very sorry to sat this!you are rejected by our admin for some reasons:\nEmail: {email}\n\n\nBest regards,\nYour Healthcare Team'
            send_email(receiver_email=email, subject=subject, body=body)

            flash("rejected mail sent successfully")
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            print(e)
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
        return redirect(url_for(all_doctors))
    return redirect(url_for('admin_dashboard'))





@app.route('/accept_doctor/<email>', methods=['GET', 'POST'])
def accept(email):
    if session.get('user'):
        try:
            mydb = conn.get_connection()
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT * FROM doctors_request WHERE email=%s', (email,))
            doctor_data = cursor.fetchone()
            if doctor_data:
                if request.method == 'POST':
                    name = request.form['name']
                    email = request.form['email']
                    password = request.form['password']
                    phone = request.form['phone']
                    specialization = request.form['specialization']
                    
                    # from_time = request.form['from_time']
                    # to_time = request.form['to_time']
                    
                    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
                    
                    
                    cursor.execute('SELECT COUNT(*) FROM Doctors WHERE email=%s', (email,))
                    email_count = cursor.fetchone()[0]
                    if email_count == 1:
                        session['doctor'] = name
                        flash("Email already exists")
                        return redirect(url_for('all_doctors'))
                    else:
                        cursor.execute('INSERT INTO doctors (name, email, password, phone, specialization) VALUES (%s, %s, %s, %s, %s)', (name, email, encrypted_password, phone, specialization))
                        mydb.commit()  # Commit the transaction after insertion

                        # Send email with credentials
                        subject = 'Login Credentials'
                        body = f'Dear {name},\n\nPlease use these credentials to log in to your account:\nEmail: {email}\nPassword: {password}\n\nBest regards,\nYour Healthcare Team'
                        send_email(receiver_email=email, subject=subject, body=body)

                        flash("Credentials sent successfully! Please use them to log in.")
                        return redirect(url_for('admin_dashboard'))
                return render_template('doctor_requset_registration.html', doctor_data=doctor_data)
            else:
                flash("No data Found!")
                return redirect(url_for("all_doctors"))
        except Exception as e:
            print(e)
            flash("An error occurred during registration.")
            return render_template('error.html')
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
    else:
        return redirect(url_for('adminlogin'))                
            
            
            





@app.route('/delete_doctor/<email>')
def delete(email):  # Added function parameter for email
    if session.get('user'):
        try:
            mydb=conn.get_connection()
            cursor=mydb.cursor()
            cursor.execute('delete from doctors_request where email=%s',(email,))
            mydb.commit()
            flash('deleted successfully')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            print(e)
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
        return redirect(url_for('all_doctors'))
    return redirect(url_for('admin_dashboard'))

 


# @app.route('/request_appointments',methods=['GET','POST'])
# def request_appointments():
#     try:
#         mydb = conn.get_connection()
#         cursor = mydb.cursor(buffered=True)
#         cursor.execute("Select doctor_id,name from doctors")
#         doctors_details = cursor.fetchall()
#         print(doctors_details)
#         if request.method == 'POST':
#             name = request.form['name']
#             phone = request.form['phone']
#             email = request.form['email']
#             appointment_time = request.form['appointment_time']
#             appointment_date = request.form['appointment_date']
#             suffering_with = request.form['suffering_with']
#             doctor_id = int(request.form['doctor_id'].strip())

#             # Data validation and conflict check
           
#             cursor.execute('SELECT * FROM request_appointments WHERE appointment_time=%s AND appointment_date=%s AND doctor_id=%s', (appointment_time, appointment_date, doctor_id))
#             conflicting_appointments = cursor.fetchall()

#             if conflicting_appointments:
#                 flash('This time slot is already booked for the appointment. Please choose another time slot.')
#                 return render_template('appointments.html',doctors_details=doctors_details)
#             else:
#                 cursor.execute('INSERT INTO appointments (name, phone, email, appointment_time, appointment_date, suffering_with, doctor_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', (name, phone, email, appointment_time, appointment_date, suffering_with, doctor_id))
#                 mydb.commit()

#                 # Send email with credentials
#                 subject = 'Appointment Confirmation'
#                 body = f'Dear {name},\n\nYour appointment has been successfully booked.\n\nAppointment details:\nDate: {appointment_date}\nTime: {appointment_time}\nDoctor: {doctor_id}\n\nThank you for choosing our services.\n\nBest regards,\nYour Healthcare Team'
#                 send_email(receiver_email=email, subject=subject, body=body)

#                 flash('Appointment booked successfully. Confirmation email has been sent to your email address.')
#                 return render_template('appointments_dashboard.html')
#         return render_template('appointments.html',doctors_details=doctors_details)

#     except Exception as e:
#         print(e)  # Log the exception for debugging purposes
#         flash('An error occurred during booking appointment.')
#         return render_template('error.html')

#     finally:
#         if mydb.is_connected():
#             cursor.close()
#             mydb.close()

#ALL LOGOUT ROUTE
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        flash('Logout successful')
        return redirect(url_for('home'))
    if session.get('doctor'):
        session.pop('doctor')
        flash('Logout successful')
        return redirect(url_for('home'))
    if session.get('patient'):
        session.pop('patient')
        flash('Logout successful')
        return redirect(url_for('home'))
    else:
        flash('Please login to continue')
        return redirect(url_for('admin_login'))

    
if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
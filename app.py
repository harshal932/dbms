import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'super_secret_railway_key'

# ---------- DATABASE CONFIGURATION ----------
# Switched from MySQL to SQLite3 so that the user never needs to authenticate a database!
DB_FILE = 'railway.db'
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'railway_mgmt_mongo'

def init_db():
    if not os.path.exists(DB_FILE):
        try:
            with sqlite3.connect(DB_FILE) as conn:
                with open('schema.sql', 'r') as f:
                    conn.executescript(f.read())
                print("Database fully initialized automatically!")
        except Exception as e:
            print("Failed to initialize SQLite DB:", e)

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as err:
        print(f"Error connecting to SQLite: {err}")
        return None

def get_mongo_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        client.server_info()  # Trigger connection test securely
        return client[MONGO_DB]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# Check initialization immediately
init_db()

# ---------- DECORATORS ----------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Admin access required!', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ---------- ROUTES ----------
@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('dashboard'))
        return redirect(url_for('book_ticket'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        if not conn:
            flash("System Offline. Hard SQLite fault.", "danger")
            return render_template('login.html')
        
        try:
            user = conn.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
            if user:
                user = dict(user)
                if check_password_hash(user['password'], password) or user['password'] == password:
                    session['user_id'] = user['user_id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    flash(f"Welcome back, {user['username']}!", 'success')
                    if user['role'] == 'admin':
                        return redirect(url_for('dashboard'))
                    else:
                        return redirect(url_for('book_ticket'))
            flash('Invalid Credentials', 'danger')
        except Exception as e:
            flash(f"Login error: {str(e)}", "danger")
        finally:
            conn.close()
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        hashed_pw = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", (username, hashed_pw, 'passenger'))
            user_id = cur.lastrowid
            
            cur.execute("INSERT INTO Passengers (user_id, name, email, phone) VALUES (?, ?, ?, ?)", (user_id, name, email, phone))
            conn.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.rollback()
            flash('Username or Email already exists!', 'danger')
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", 'danger')
        finally:
            conn.close()
            
    return render_template('passengers.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
@admin_required
def dashboard():
    conn = get_db_connection()
    stats = {'total_trains':0, 'total_passengers':0, 'revenue':0, 'total_bookings':0}
    
    try:
        stats['total_trains'] = conn.execute("SELECT COUNT(*) as c FROM Trains").fetchone()['c']
        stats['total_passengers'] = conn.execute("SELECT COUNT(*) as c FROM Passengers").fetchone()['c']
        stats['total_bookings'] = conn.execute("SELECT COUNT(*) as c FROM Bookings").fetchone()['c']
        row = conn.execute("SELECT SUM(fare) as r FROM Bookings WHERE status='confirmed'").fetchone()
        stats['revenue'] = row['r'] if row and row['r'] else 0
    except Exception as e:
        flash(f"Error fetching stats: {str(e)}", "danger")
    finally:
        conn.close()
        
    return render_template('dashboard.html', **stats)

# --- TRAINS CRUD ---
@app.route('/trains', methods=['GET', 'POST'])
@login_required
@admin_required
def trains():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form.get('name')
        t_type = request.form.get('type')
        seats = request.form.get('seats')
        try:
            conn.execute("INSERT INTO Trains (name, type, total_seats) VALUES (?, ?, ?)", (name, t_type, seats))
            conn.commit()
            flash('Train added successfully!', 'success')
        except Exception as e:
            flash(str(e), 'danger')
            
    try:
        train_list = [dict(r) for r in conn.execute("SELECT * FROM Trains ORDER BY train_id DESC").fetchall()]
    finally:
        conn.close()
        
    return render_template('trains.html', trains=train_list)

@app.route('/edit_train/<int:train_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_train(train_id):
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form.get('name')
        t_type = request.form.get('type')
        seats = request.form.get('seats')
        try:
            conn.execute("UPDATE Trains SET name=?, type=?, total_seats=? WHERE train_id=?", (name, t_type, seats, train_id))
            conn.commit()
            flash('Train modified successfully!', 'success')
            return redirect(url_for('trains'))
        except Exception as e:
            flash(str(e), 'danger')
            
    try:
        train = dict(conn.execute("SELECT * FROM Trains WHERE train_id=?", (train_id,)).fetchone())
    finally:
        conn.close()
        
    if not train:
        flash("Train not found", "danger")
        return redirect(url_for('trains'))
        
    return render_template('edit_train.html', train=train)

@app.route('/delete_train/<int:train_id>', methods=['POST'])
@login_required
@admin_required
def delete_train(train_id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM Trains WHERE train_id=?", (train_id,))
        conn.commit()
        flash('Train deleted explicitly.', 'warning')
    except Exception as e:
        flash(str(e), 'danger')
    finally:
        conn.close()
    return redirect(url_for('trains'))

# --- STATIONS CRUD ---
@app.route('/stations', methods=['GET', 'POST'])
@login_required
@admin_required
def stations():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        platforms = request.form.get('platforms')
        try:
            conn.execute("INSERT INTO Stations (name, city, state, platforms) VALUES (?, ?, ?, ?)", (name, city, state, platforms))
            conn.commit()
            flash('Station added successfully!', 'success')
        except Exception as e:
            flash(str(e), 'danger')
            
    try:
        st_list = [dict(r) for r in conn.execute("SELECT * FROM Stations ORDER BY station_id DESC").fetchall()]
    finally:
        conn.close()
    return render_template('stations.html', stations=st_list)

# --- SCHEDULES CRUD ---
@app.route('/schedules', methods=['GET', 'POST'])
@login_required
@admin_required
def schedules():
    conn = get_db_connection()
    if request.method == 'POST':
        train_id = request.form.get('train_id')
        source_id = request.form.get('source')
        dest_id = request.form.get('dest')
        fare = request.form.get('fare', 0)
        dep = request.form.get('departure')
        arr = request.form.get('arrival')
        try:
            row = conn.execute("SELECT total_seats FROM Trains WHERE train_id=?", (train_id,)).fetchone()
            avail_seats = row['total_seats'] if row else 0
            
            conn.execute("""
                INSERT INTO Schedules (train_id, source_station, dest_station, departure, arrival, fare, available_seats) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (train_id, source_id, dest_id, dep, arr, fare, avail_seats))
            conn.commit()
            flash('Schedule added successfully!', 'success')
        except Exception as e:
            flash(f"Error adding schedule: {e}", 'danger')

    try:
        scheds = [dict(r) for r in conn.execute("""
            SELECT S.schedule_id, T.name as train_name, S.departure, S.arrival, S.fare, S.available_seats,
                   ST1.name as source_name, ST2.name as dest_name
            FROM Schedules S
            JOIN Trains T ON S.train_id = T.train_id
            JOIN Stations ST1 ON S.source_station = ST1.station_id
            JOIN Stations ST2 ON S.dest_station = ST2.station_id
            ORDER BY S.departure ASC
        """).fetchall()]
        trains = [dict(r) for r in conn.execute("SELECT train_id, name FROM Trains WHERE status='active'").fetchall()]
        stations = [dict(r) for r in conn.execute("SELECT station_id, name FROM Stations").fetchall()]
    finally:
        conn.close()
        
    return render_template('schedules.html', schedules=scheds, trains=trains, stations=stations)



# --- PASSENGER PAGES ---
@app.route('/book_ticket', methods=['GET', 'POST'])
@login_required
def book_ticket():
    conn = get_db_connection()
    search_results = []
    if request.method == 'POST' and 'search' in request.form:
        source_id = request.form.get('source')
        dest_id = request.form.get('dest')
        date = request.form.get('date')
        try:
            results = conn.execute("""
                SELECT S.schedule_id, T.name as train_name, S.departure, S.arrival, S.fare, S.available_seats,
                       ST1.name as source_name, ST2.name as dest_name
                FROM Schedules S
                JOIN Trains T ON S.train_id = T.train_id
                JOIN Stations ST1 ON S.source_station = ST1.station_id
                JOIN Stations ST2 ON S.dest_station = ST2.station_id
                WHERE S.source_station = ? AND S.dest_station = ? AND date(S.departure) = date(?) AND S.available_seats > 0
            """, (source_id, dest_id, date)).fetchall()
            search_results = [dict(r) for r in results]
            flash(f"Found {len(search_results)} available trains.", "info")
        except Exception as e:
            flash(str(e), 'danger')

    if request.method == 'POST' and 'book' in request.form:
        sched_id = request.form.get('schedule_id')
        fare = request.form.get('fare')
        try:
            p_row = conn.execute("SELECT passenger_id FROM Passengers WHERE user_id = ?", (session['user_id'],)).fetchone()
            if not p_row:
                flash("Complete your passenger profile first.", "warning")
            else:
                p_id = p_row['passenger_id']
                conn.execute("INSERT INTO Bookings (passenger_id, schedule_id, fare, travel_date) SELECT ?, ?, ?, date(departure) FROM Schedules WHERE schedule_id=?", (p_id, sched_id, fare, sched_id))
                # Trigger 2 automatically reduces available_seats in Schedules
                conn.commit()
                flash("Booking Confirmed Successfully!", "success")
                return redirect(url_for('my_bookings'))
        except sqlite3.IntegrityError as e:
            conn.rollback()
            # This captures our trigger error "No seats available for this schedule" or other SQLite trigger aborts
            flash(f"Booking Error: {str(e)}", "danger")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")

    try:
        stations = [dict(r) for r in conn.execute("SELECT station_id, name FROM Stations").fetchall()]
    finally:
        conn.close()
        
    return render_template('book_ticket.html', stations=stations, search_results=search_results)

@app.route('/my_bookings', methods=['GET', 'POST'])
@login_required
def my_bookings():
    conn = get_db_connection()
    if request.method == 'POST' and 'cancel' in request.form:
        booking_id = request.form.get('booking_id')
        try:
            conn.execute("UPDATE Bookings SET status='cancelled' WHERE booking_id=?", (booking_id,))
            # Trigger 3 automatically adds available_seats + 1 in Schedules
            conn.commit()
            flash('Booking cancelled successfully.', 'warning')
        except sqlite3.IntegrityError as e:
            conn.rollback()
            flash(f"Cancellation Error: {str(e)}", 'danger')
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", 'danger')

    try:
        if session.get('role') == 'admin':
            q = """
            SELECT B.booking_id, T.name as train_name, B.travel_date, B.status, B.fare, P.name as passenger_name,
                   ST1.name as source_name, ST2.name as dest_name
            FROM Bookings B
            JOIN Schedules S ON B.schedule_id = S.schedule_id
            JOIN Trains T ON S.train_id = T.train_id
            JOIN Passengers P ON B.passenger_id = P.passenger_id
            JOIN Stations ST1 ON S.source_station = ST1.station_id
            JOIN Stations ST2 ON S.dest_station = ST2.station_id
            ORDER BY B.booking_id DESC
            """
            bookings = [dict(r) for r in conn.execute(q).fetchall()]
        else:
            q = """
            SELECT B.booking_id, T.name as train_name, B.travel_date, B.status, B.fare, P.name as passenger_name,
                   ST1.name as source_name, ST2.name as dest_name
            FROM Bookings B
            JOIN Schedules S ON B.schedule_id = S.schedule_id
            JOIN Trains T ON S.train_id = T.train_id
            JOIN Passengers P ON B.passenger_id = P.passenger_id
            JOIN Stations ST1 ON S.source_station = ST1.station_id
            JOIN Stations ST2 ON S.dest_station = ST2.station_id
            WHERE P.user_id = ?
            ORDER BY B.booking_id DESC
            """
            bookings = [dict(r) for r in conn.execute(q, (session['user_id'],)).fetchall()]
    finally:
        conn.close()
        
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/reports')
@login_required
@admin_required
def reports():
    conn = get_db_connection()
    try:
        revenue_data = [dict(r) for r in conn.execute("""
            SELECT (ST1.name || ' - ' || ST2.name) as route, SUM(B.fare) as revenue 
            FROM Bookings B
            JOIN Schedules S ON B.schedule_id = S.schedule_id
            JOIN Stations ST1 ON S.source_station = ST1.station_id
            JOIN Stations ST2 ON S.dest_station = ST2.station_id
            WHERE B.status = 'confirmed'
            GROUP BY route
        """).fetchall()]
        
        occupancy_data = [dict(r) for r in conn.execute("""
            SELECT T.name as train, (T.total_seats - S.available_seats) as booked, T.total_seats
            FROM Schedules S JOIN Trains T ON S.train_id = T.train_id
        """).fetchall()]
    except Exception as e:
        flash(f"Error formulating report: {str(e)}", "danger")
        revenue_data, occupancy_data = [], []
    finally:
        conn.close()
    return render_template('reports.html', revenue_data=revenue_data, occupancy_data=occupancy_data)

@app.route('/catalog', methods=['GET', 'POST'])
@login_required
def catalog():
    mongo = get_mongo_db()
    if request.method == 'POST':
        feedback = request.form.get('comments')
        rating = int(request.form.get('rating', 5))
        train_mon_id = request.form.get('train_id')
        if mongo is not None:
            try:
                mongo.passenger_feedback.insert_one({
                    'passenger_name': session.get('username'),
                    'train_id': int(train_mon_id) if train_mon_id else 0,
                    'rating': rating,
                    'comments': feedback
                })
                flash('Feedback submitted to MongoDB!', 'success')
            except Exception as e:
                flash(f"Mongo Error: {e}", "danger")
        else:
            flash(f"Cannot submit feedback, Mongo offline.", "danger")

    if mongo is not None:
        try:
            train_docs = list(mongo.trains_catalog.find({}))
            feedbacks = list(mongo.passenger_feedback.find({}).sort("_id", -1).limit(10))
        except Exception as e:
            flash(f"Mongo retrieval issue: {e}", "danger")
            train_docs, feedbacks = [], []
    else:
        # Fallback dictionary if Mongo is completely uninstalled/broken
        flash("MongoDB integration offline. Returning static structural fallback.", "warning")
        train_docs = [{'train_id': 1, 'amenities': ['WiFi', 'AC'], 'avg_rating': 4.5, 'description': 'Premium Train'}]
        feedbacks = [{'passenger_name': 'John', 'comments': 'Fallback trip.', 'rating': 5}]
        
    return render_template('catalog.html', train_docs=train_docs, feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True, port=8080)

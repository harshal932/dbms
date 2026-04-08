CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Stations (
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50) DEFAULT 'India',
    platforms INT
);

CREATE TABLE IF NOT EXISTS Trains (
    train_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    total_seats INT,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS Schedules (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_id INT,
    source_station INT,
    dest_station INT,
    departure DATETIME,
    arrival DATETIME,
    fare DECIMAL(10, 2),
    available_seats INT,
    FOREIGN KEY (train_id) REFERENCES Trains(train_id) ON DELETE CASCADE,
    FOREIGN KEY (source_station) REFERENCES Stations(station_id) ON DELETE CASCADE,
    FOREIGN KEY (dest_station) REFERENCES Stations(station_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Passengers (
    passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    country VARCHAR(50) DEFAULT 'India',
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_id INT,
    schedule_id INT,
    seat_no VARCHAR(10),
    booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    travel_date DATE,
    status VARCHAR(20) DEFAULT 'confirmed',
    payment_status VARCHAR(20) DEFAULT 'paid',
    fare DECIMAL(10, 2),
    FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id) ON DELETE CASCADE,
    FOREIGN KEY (schedule_id) REFERENCES Schedules(schedule_id) ON DELETE CASCADE
);

INSERT OR IGNORE INTO Users (user_id, username, password, role) VALUES 
(1, 'admin', 'admin', 'admin'),
(2, 'user', 'user', 'passenger'),
(3, 'alice', 'alice', 'passenger'),
(4, 'bob', 'bob', 'passenger');

INSERT OR IGNORE INTO Passengers (passenger_id, user_id, name, age, gender, email, phone, country) VALUES 
(1, 2, 'Rohan Gupta', 30, 'Male', 'rohan@example.com', '9876543210', 'India'),
(2, 3, 'Alice Smith', 25, 'Female', 'alice@example.com', '1234567890', 'India'),
(3, 4, 'Bob Builder', 40, 'Male', 'bob@example.com', '0987654321', 'India');

INSERT OR IGNORE INTO Stations (station_id, name, city, state, country, platforms) VALUES 
(1, 'New Delhi Railway Station', 'New Delhi', 'Delhi', 'India', 16),
(2, 'Chhatrapati Shivaji Maharaj Terminus', 'Mumbai', 'Maharashtra', 'India', 18),
(3, 'Howrah Junction', 'Kolkata', 'West Bengal', 'India', 23),
(4, 'Chennai Central', 'Chennai', 'Tamil Nadu', 'India', 17),
(5, 'Secunderabad Junction', 'Hyderabad', 'Telangana', 'India', 10),
(6, 'Ahmedabad Junction', 'Ahmedabad', 'Gujarat', 'India', 12),
(7, 'Pune Junction', 'Pune', 'Maharashtra', 'India', 6),
(8, 'Jaipur Junction', 'Jaipur', 'Rajasthan', 'India', 7),
(9, 'Lucknow Charbagh', 'Lucknow', 'Uttar Pradesh', 'India', 9),
(10, 'Bhopal Junction', 'Bhopal', 'Madhya Pradesh', 'India', 6);

INSERT OR IGNORE INTO Trains (train_id, name, type, total_seats, status) VALUES 
(1, 'Rajdhani Express', 'Premium', 800, 'active'),
(2, 'Shatabdi Express', 'Express', 600, 'active'),
(3, 'Garib Rath', 'Economy', 1000, 'active'),
(4, 'Duronto Express', 'Premium', 750, 'active'),
(5, 'Vande Bharat Express', 'Premium', 500, 'active'),
(6, 'Tejas Express', 'Premium', 550, 'active'),
(7, 'Jan Shatabdi', 'Express', 650, 'active'),
(8, 'Coromandel Express', 'Express', 900, 'active'),
(9, 'Mail/Express', 'Local', 400, 'active'),
(10, 'Golden Chariot', 'Luxury', 200, 'active');

INSERT OR IGNORE INTO Schedules (schedule_id, train_id, source_station, dest_station, departure, arrival, fare, available_seats) VALUES 
(1, 1, 1, 2, '2026-10-01 16:00:00', '2026-10-02 08:00:00', 2500.00, 800),
(2, 2, 1, 9, '2026-10-01 06:00:00', '2026-10-01 14:00:00', 1200.00, 600),
(3, 3, 2, 7, '2026-10-02 10:00:00', '2026-10-02 15:00:00', 300.00, 1000),
(4, 5, 1, 10, '2026-10-03 08:00:00', '2026-10-03 14:30:00', 1500.00, 500),
(5, 8, 3, 4, '2026-10-05 14:00:00', '2026-10-06 18:00:00', 1800.00, 900),
(6, 4, 2, 6, '2026-10-06 20:00:00', '2026-10-07 05:00:00', 2100.00, 750),
(7, 6, 1, 8, '2026-10-08 07:00:00', '2026-10-08 12:00:00', 1600.00, 550),
(8, 7, 7, 2, '2026-10-09 09:00:00', '2026-10-09 13:00:00', 500.00, 650),
(9, 9, 3, 1, '2026-10-10 18:00:00', '2026-10-11 12:00:00', 900.00, 400),
(10, 10, 4, 3, '2026-10-12 11:00:00', '2026-10-13 14:00:00', 3000.00, 200);

INSERT OR IGNORE INTO Bookings (booking_id, passenger_id, schedule_id, seat_no, travel_date, status, payment_status, fare) VALUES
(1, 1, 1, 'A1', '2026-10-01', 'confirmed', 'paid', 2500.00),
(2, 2, 2, 'B2', '2026-10-01', 'confirmed', 'paid', 1200.00),
(3, 3, 3, 'C3', '2026-10-02', 'cancelled', 'paid', 300.00);

-- ================================================================
-- TRIGGER & AUDIT REQUIREMENTS
-- ================================================================

CREATE TABLE IF NOT EXISTS Booking_Audit (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INT,
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    old_payment VARCHAR(20),
    new_payment VARCHAR(20),
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TRIGGER 1 - BEFORE INSERT ON Bookings:
CREATE TRIGGER IF NOT EXISTS chk_seats_before_insert_booking
BEFORE INSERT ON Bookings
FOR EACH ROW
WHEN (SELECT available_seats FROM Schedules WHERE schedule_id = NEW.schedule_id) <= 0
BEGIN
    SELECT RAISE(ABORT, 'No seats available for this schedule');
END;

-- TRIGGER 2 - AFTER INSERT ON Bookings:
CREATE TRIGGER IF NOT EXISTS reduce_seats_after_booking
AFTER INSERT ON Bookings
FOR EACH ROW
BEGIN
    UPDATE Schedules 
    SET available_seats = available_seats - 1 
    WHERE schedule_id = NEW.schedule_id;
END;

-- TRIGGER 3 - AFTER UPDATE ON Bookings (Cancel):
-- Handle cancellation
CREATE TRIGGER IF NOT EXISTS update_seats_on_cancel
AFTER UPDATE ON Bookings
FOR EACH ROW
WHEN NEW.status = 'cancelled' AND OLD.status != 'cancelled'
BEGIN
    UPDATE Schedules
    SET available_seats = available_seats + 1
    WHERE schedule_id = NEW.schedule_id;
END;

-- Handle un-cancellation (changing from 'cancelled' to 'confirmed')
CREATE TRIGGER IF NOT EXISTS update_seats_on_uncancel
AFTER UPDATE ON Bookings
FOR EACH ROW
WHEN NEW.status = 'confirmed' AND OLD.status == 'cancelled'
BEGIN
    UPDATE Schedules
    SET available_seats = available_seats - 1
    WHERE schedule_id = NEW.schedule_id;
END;

-- TRIGGER 4 - AFTER UPDATE ON Bookings (Audit Log):
CREATE TRIGGER IF NOT EXISTS log_booking_status_change
AFTER UPDATE ON Bookings
FOR EACH ROW
WHEN OLD.status != NEW.status OR OLD.payment_status != NEW.payment_status
BEGIN
    INSERT INTO Booking_Audit (booking_id, old_status, new_status, old_payment, new_payment)
    VALUES (NEW.booking_id, OLD.status, NEW.status, OLD.payment_status, NEW.payment_status);
END;

-- TRIGGER 5 - BEFORE INSERT ON Passengers:
CREATE TRIGGER IF NOT EXISTS validate_passenger_age
BEFORE INSERT ON Passengers
FOR EACH ROW
WHEN NEW.age IS NOT NULL AND (NEW.age < 1 OR NEW.age > 120)
BEGIN
    SELECT RAISE(ABORT, 'Age must be between 1 and 120');
END;

-- TRIGGER 6 - BEFORE INSERT ON Schedules:
CREATE TRIGGER IF NOT EXISTS validate_schedule_fare
BEFORE INSERT ON Schedules
FOR EACH ROW
WHEN NEW.fare <= 0
BEGIN
    SELECT RAISE(ABORT, 'Fare must be greater than 0');
END;

CREATE TRIGGER IF NOT EXISTS validate_schedule_time
BEFORE INSERT ON Schedules
FOR EACH ROW
WHEN NEW.departure >= NEW.arrival
BEGIN
    SELECT RAISE(ABORT, 'Departure time must be before arrival time');
END;

-- ================================================================
-- TRIGGER TEST QUERIES
-- ================================================================
/*
-- TEST TRIGGER 1 & 2
-- This will succeed (reduce available_seats in Schedule 1 by 1)
INSERT INTO Bookings (passenger_id, schedule_id, fare, travel_date, status) 
VALUES (1, 1, 2500, '2026-10-01', 'confirmed');

-- Wait, to specifically test RAISE(ABORT) for TRIGGER 1, try:
-- UPDATE Schedules SET available_seats = 0 WHERE schedule_id = 2;
-- INSERT INTO Bookings (passenger_id, schedule_id) VALUES (1, 2); 
-- THIS WILL ERROR WITH: "No seats available for this schedule"


-- TEST TRIGGER 3 & 4
-- This changes status to 'cancelled', restoring 1 seat in Schedules and inserting a row into Booking_Audit
UPDATE Bookings SET status = 'cancelled' WHERE booking_id = 1;


-- TEST TRIGGER 5
-- This will fail and throw error "Age must be between 1 and 120"
-- INSERT INTO Passengers (user_id, name, age) VALUES (2, 'Test', 150);


-- TEST TRIGGER 6
-- This will fail with fare error:
-- INSERT INTO Schedules (train_id, source_station, dest_station, fare, departure, arrival) VALUES (1, 1, 2, -100, '2026-11-01 10:00:00', '2026-11-01 12:00:00');

-- This will fail with departure time error:
-- INSERT INTO Schedules (train_id, source_station, dest_station, fare, departure, arrival) VALUES (1, 1, 2, 500, '2026-11-01 14:00:00', '2026-11-01 12:00:00');
*/

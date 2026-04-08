# 1. Title Page
**Project Title:** Railway Management System  
**Student Names & Roll Numbers:** John Doe (101), Jane Smith (102)  
**Class:** B.Tech CS  
**College Name:** ABC Institute of Technology  
**Subject:** Database Management Systems  
**Academic Year:** 2025-2026  

# 2. Abstract
The Railway Management System is a web-based application designed to streamline the ticketing and management processes of a railway network. It incorporates automated functionalities for booking tickets, managing train schedules, monitoring passenger statuses, and generating comprehensive admin reports. The system utilizes a hybrid database approach—using MySQL for transactional integrity (e.g., ticket booking, payment processing) and MongoDB for flexible document storage (e.g., train amenity catalogs and passenger feedback). By moving away from manual record-keeping or fragmented systems, this centralized application offers increased efficiency, enhanced user satisfaction, and reduced operational errors.

# 3. Introduction
**Problem Statement:** Manual ticketing and disjointed schedule management lead to long passenger queues, double-booking errors, and inefficient data retrieval.
**Objectives:**
- Provide a responsive frontend for seamless ticket booking.
- Empower admins to manage train/station/schedule easily.
- Handle transactional data stably.
**Scope of Project:** The project covers passenger registration, searching and booking tickets, viewing bookings, and admin-side management of trains, stations, schedules, staff, and overall reporting.

# 4. Software Requirement Specification (SRS)
**Functional Requirements:**
- Secure User Authentication (Admin/Passenger)
- Admin privileges: manage trains, stations, schedules, staff
- Passenger privileges: search routes, book tickets, view past bookings, submit feedback
**Non-Functional Requirements:**
- Performance: Quick response for queries
- Security: Password protection
- Usability: Intuitive UI
**Hardware & Software Requirements:**
- Backend: Python 3.10+, Flask
- Frontend: HTML5, CSS3, Bootstrap 5
- DB: MySQL, MongoDB

# 5. Conceptual Design
**ER Diagram Elements:** 
Entities: Users, Passengers, Trains, Stations, Schedules, Bookings, Staff
Relationships:
- Train HAS Schedules (1:N)
- Schedule CONNECTS Stations (M:N, via Source and Dest)
- Passenger MAKES Bookings (1:N)
- Booking RESERVES Schedule (N:1)

**Relational Model:** (Covered in schema.sql)
**Normalization (3NF):** All tables have unique PKs, attributes depend entirely on PKs (no partial dependency), and no transitive dependencies.

# 6. GUI Screenshots Description
- **Login Page:** Input fields for username/password.
- **Dashboard:** At-a-glance cards showing total trains, revenues, and bookings.
- **Book Ticket:** Dropdown/Search for routes, displaying fare and button to confirm.
- **Reports:** Tabular revenue breakdowns and occupancy statistics.

# 7. Source Code
Available in `app.py`, `templates/`, `static/`, and database definition files.

# 8. Testing Document
Reference: `testing.md`

# 9. Conclusion & Future Scope
**Conclusion:** The hybrid architecture effectively separates structured table relations from flexible unstructured data sets, providing optimization.
**Future Scope:** Payment gateway integration, push notifications, and GPS tracking.

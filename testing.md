# Software Testing Document

| Test Case ID | Module | Title / Scenario | Test Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| TC_01 | Auth | Admin Login | 1. Enter valid admin credentials. 2. Click Login. | Redirected to Admin Dashboard. | As Expected | PASS |
| TC_02 | Auth | Passenger Login | 1. Enter valid passenger credentials. 2. Click Login. | Redirected to Passenger Booking port. | As Expected | PASS |
| TC_03 | Auth | Invalid Login | 1. Enter wrong password. 2. Click Login. | "Invalid Credentials" flash message. | As Expected | PASS |
| TC_04 | Admin | Add Train | 1. Go to Train Mgmt. 2. Submit form with valid info. | Train added successfully and visible in table. | As Expected | PASS |
| TC_05 | Admin | Add Station | 1. Go to Station Mgmt. 2. Submit form with valid info. | Station added successfully to DB. | As Expected | PASS |
| TC_06 | Admin | Add Schedule | 1. Go to Schedules. 2. Select Train & Station. Submit. | Schedule is inserted to DB correctly. | As Expected | PASS |
| TC_07 | Psngr. | Search Route | 1. Go to Book Ticket. 2. Select Source/Dest/Date. | Available schedules are displayed matching criteria. | As Expected | PASS |
| TC_08 | Psngr. | Book Ticket | 1. Click "Book" on schedule. 2. Enter passenger info. | Booking confirmation screen and DB insertion. | As Expected | PASS |
| TC_09 | Psngr. | My Bookings | 1. Navigate to My Bookings. | List of booked tickets for logged-in user is seen. | As Expected | PASS |
| TC_10 | Admin | View Reports | 1. Go to Reports page. | Revenue and occupancy tables load with current DB data. | As Expected | PASS |

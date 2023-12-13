# IReporter-Flask

iReporter - Fighting Corruption, Empowering Citizens
Overview
iReporter is a web application designed to tackle corruption in African countries by providing a platform for citizens to report incidents and call for government intervention. The application aims to empower users to contribute to the fight against corruption by highlighting issues that need attention.

Team
Full Stack Developers:
Frontend: React
Backend: Python Flask
MVP Features
User Authentication:

Users can create an account and log in.
Incident Reporting:

Users can create a red-flag record (incident linked to corruption).
Users can create intervention records (call for government agency intervention).
Record Management:

Users can edit their red-flag or intervention records.
Users can delete their red-flag or intervention records.
Geolocation:

Users can add geolocation (Lat Long Coordinates) to their records.
Users can change the geolocation attached to their records.
Admin Features:

Admin can change the status of a record (under investigation, rejected, resolved).
Media Support:

Users can add images and videos to their records to support their claims.
Notifications:

Users receive real-time email notifications when Admin changes the status of their record.
Optional Features
Map Integration:

Display a Google Map with Markers showing the red-flag or intervention location.
SMS Notifications:

Users receive real-time SMS notifications when Admin changes the status of their record.
Constraints
Geolocation Restrictions:

Users can only change geolocation when the record's status is not under investigation, rejected, or resolved.
Record Editing/Deletion:

Users can only edit or delete a record when the status is not under investigation, rejected, or resolved.
Only the user who created the record can delete it.
Technical Expectations
Backend:

Python Flask
Database:

PostgreSQL
Frontend:

ReactJs & Redux Toolkit (state management)
Wireframes:

Figma (Mobile-friendly design)
Testing Frameworks:

Jest (Frontend)
Minitests (Backend)
Getting Started
Clone the repository.

Set up the backend:

bash
Copy code
cd backend
pip install -r requirements.txt
python manage.py runserver
Set up the frontend:

bash
Copy code
cd frontend
npm install
npm start
Open the application in your browser.

Contributions
We welcome contributions! If you'd like to contribute to iReporter, please fork the repository and submit a pull request.

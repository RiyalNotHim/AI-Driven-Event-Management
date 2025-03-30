# AI-Driven-Event-Management
********Event Management System********

Introduction:
This project is an automated event management system designed to handle various types of college events. It supports user roles such as Admin, Volunteer, Participant, and Audience. The system is built using Python (Flask & FastAPI), MongoDB for data storage, and includes an AI-powered chatbot for assistance.

Features:

	---User Authentication: Supports login and role-based access.
	---Event Management: Users can create, register, and manage events.
	---Admin Controls: Admins can approve events and manage users.
	---AI-powered Role Assignment: Assigns user roles based on skills.
	---Chatbot Integration: Provides event-related assistance.

Technologies Used:

	---Backend: Flask, FastAPI
	---Frontend: HTML, CSS, JavaScript
	---Database: MongoDB
	---Other Dependencies: Selenium, OpenAI API, Google Sheets API, Flask-CORS

Installation:

Prerequisites:
	Ensure you have Python and MongoDB installed.

Setup:
	1.Clone the repository:
		---git clone <repository_url>
	   	   cd event-management-system

	2.Install dependencies:
		---pip install -r requirements.txt

	3.Set up environment variables in a .env file:
		---MONGO_URI=mongodb+srv://your_connection_string
		   OPENAI_API_KEY=your_api_key
	
	4.Run the application:
		---uvicorn main:app --reload  # For FastAPI
		   flask run  # For Flask
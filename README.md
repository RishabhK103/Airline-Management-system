# Airline-Management-system

This Streamlit web application manages an airline's flights, crew, and bookings using an SQLite database. It supports two user roles: Admin and Customer.

Features
Admin Page:
Login with ID and password.
Add flight details (flight number, departure/arrival airports, times, aircraft type, ticket price).
Customer Page:
View available flights.
Book flights by providing passenger details and booking information.
Key Functions
create_tables(): Creates Flights, Crew, and Bookings tables.
add_flight(): Adds new flight details to the database.
add_booking(): Adds new booking details to the database.

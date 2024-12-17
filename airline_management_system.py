import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
#comment
# Database connection
conn = sqlite3.connect("airline.db", check_same_thread=False)
c = conn.cursor()

# Create tables if they don't exist
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS Flights (
                    flight_number VARCHAR(10) PRIMARY KEY,
                    departure_airport VARCHAR(50),
                    arrival_airport VARCHAR(50),
                    departure_time DATETIME,
                    arrival_time DATETIME,
                    aircraft_type VARCHAR(50),
                    ticket_price INTEGER
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Crew (
                    crew_id INTEGER PRIMARY KEY,
                    crew_name VARCHAR(100),
                    crew_position VARCHAR(50),
                    assigned_flights VARCHAR(100),
                    FOREIGN KEY (assigned_flights) REFERENCES Flights(flight_number)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Bookings (
                    booking_id INTEGER PRIMARY KEY,
                    flight_number VARCHAR(10),
                    passenger_name VARCHAR(100),
                    contact_info VARCHAR(100),
                    email VARCHAR(100),
                    seat_assignment VARCHAR(20),
                    booking_status VARCHAR(20),
                    payment_info VARCHAR(100),
                    FOREIGN KEY (flight_number) REFERENCES Flights(flight_number)
                )''')
    
def add_flight(flight_number, departure_airport, arrival_airport, departure_time, arrival_time, aircraft_type, ticket_price):
    try:
        # Convert times to datetime objects
        departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")
        arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S")

        # Insert flight data
        c.execute('''INSERT INTO Flights (flight_number, departure_airport, arrival_airport, departure_time, arrival_time, aircraft_type, ticket_price)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (flight_number, departure_airport, arrival_airport, departure_time, arrival_time, aircraft_type, ticket_price))
        conn.commit()
        st.success("Flight added successfully")
    except Exception as e:
        st.error(f"Error adding flight: {e}")

def add_booking(flight_number, passenger_name, contact_info, email, seat_assignment, booking_status, payment_info):
    try:
        # Insert booking data
        c.execute('''INSERT INTO Bookings (flight_number, passenger_name, contact_info, email, seat_assignment, booking_status, payment_info)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (flight_number, passenger_name, contact_info, email, seat_assignment, booking_status, payment_info))
        conn.commit()
        st.success("Booking successful")
    except Exception as e:
        st.error(f"Error adding booking: {e}")

# Admin Page
def admin_page():
    st.title("Admin Page")
    admin_id = st.text_input("Admin ID")
    admin_password = st.text_input("Password", type="password")

    if admin_id == "admin" and admin_password == "password":
        st.success("Login Successful")
        if st.button("Add Flight Details"):
            st.session_state.add_flight_page = True
    else:
        if admin_id or admin_password:
            st.error("Invalid ID or Password")

    if st.session_state.get("add_flight_page", False):
        add_flight_details()

def add_flight_details():
    st.title("Add Flight Details")
    # Input fields for adding flight details
    flight_number = st.text_input("Flight Number")
    departure_airport = st.text_input("Departure Airport")
    arrival_airport = st.text_input("Arrival Airport")
    departure_time = st.text_input("Departure Time (YYYY-MM-DD HH:MM:SS)")
    arrival_time = st.text_input("Arrival Time (YYYY-MM-DD HH:MM:SS)")
    aircraft_type = st.text_input("Aircraft Type")
    ticket_price = st.number_input("Ticket Price")

    if st.button("Add Flight"):
        add_flight(flight_number, departure_airport, arrival_airport, departure_time, arrival_time, aircraft_type, ticket_price)
        st.success("Flight added successfully")
        st.session_state.add_flight_page = False


# Customer Page
def customer_page():
    st.title("Customer Page")

    # Display all flights added by admin
    c.execute("SELECT * FROM Flights")
    flights_data = c.fetchall()
    #st.markdown("flights_data")
    if flights_data:
        st.header("Available Flights")
        flights_df = pd.DataFrame(flights_data, columns=["Flight Number", "Departure Airport", "Arrival Airport", "Departure Time", "Arrival Time", "Aircraft Type", "Ticket Price"])
        st.dataframe(flights_df)

        selected_flight_number = st.selectbox("Select a Flight Number", flights_df["Flight Number"].tolist())
        selected_flight = flights_df[flights_df["Flight Number"] == selected_flight_number]
        if not selected_flight.empty:
            st.header(f"Fill Details for Flight {selected_flight_number}")
            passenger_name = st.text_input("Passenger Name")
            contact_info = st.text_input("Contact Info")
            email = st.text_input("Email")
            seat_assignment = st.text_input("Seat Assignment")
            booking_status = st.text_input("Booking Status")
            payment_info = st.text_input("Payment Info")

            if st.button("Book Flight"):
                # Add booking to database
                add_booking(selected_flight_number, passenger_name, contact_info, email, seat_assignment, booking_status, payment_info)
    else:
        st.error("No flights available")


def main():
    create_tables()

    st.title("Airline Management System")

    # Homepage
    user_type = st.radio("Select User Type", ("Admin", "Customer"))

    if user_type == "Admin":
        admin_page()
    elif user_type == "Customer":
        customer_page()

if __name__ == "__main__":
    main()
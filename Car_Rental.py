import streamlit as st
from PW2_Car_Rental_Light import RentalAgency, Customer, calculate_total

st.title("Car Rental System")

# Vehicle dictionary
vehicles = {
    101: ("Perodua Myvi", 80),
    102: ("Proton Saga", 70),
    103: ("Honda City", 120),
    104: ("Toyota Vios", 110)
}

# Create objects only once
if "customer" not in st.session_state:
    agency = RentalAgency("CLN Car Rental", vehicles)
    st.session_state.customer = Customer(
        agency.agency_name,
        agency.vehicles,
        ""
    )

customer = st.session_state.customer

# Student information
st.subheader("Student Information")
name = st.text_input("Name")
registration = st.text_input("Registration Number")
student_class = st.text_input("Class")

customer.customer_name = name

# Menu
st.subheader("Menu")
choice = st.selectbox(
    "Choose an option",
    [
        "View Available Vehicles",
        "Book Vehicle Rental",
        "Cancel Vehicle Booking",
        "View Rental Booking",
        "Add Payment",
        "Checkout"
    ]
)

# 1. View vehicles
if choice == "View Available Vehicles":
    st.write("### Available Vehicles")

    for code, vehicle in vehicles.items():
        st.write(
            f"{code} - {vehicle[0]} - RM{vehicle[1]} per day"
        )

# 2. Book vehicle
elif choice == "Book Vehicle Rental":
    code = st.selectbox("Vehicle", list(vehicles.keys()))
    days = st.number_input("Rental Days", min_value=1, step=1)

    if st.button("Book"):
        customer.book_vehicle(code, days)
        st.success("Vehicle booked successfully.")

# 3. Cancel booking
elif choice == "Cancel Vehicle Booking":
    if len(customer.bookings) == 0:
        st.info("No active booking.")
    else:
        booking_no = st.number_input(
            "Booking number",
            min_value=1,
            max_value=len(customer.bookings),
            step=1
        )

        if st.button("Cancel"):
            customer.bookings.pop(booking_no - 1)
            st.success("Booking cancelled.")

# 4. View booking
elif choice == "View Rental Booking":
    if len(customer.bookings) == 0:
        st.info("No active booking.")
    else:
        for i, booking in enumerate(customer.bookings, 1):
            code, days = booking
            model = vehicles[code][0]
            rate = vehicles[code][1]

            st.write(
                f"{i}. {model} - {days} day(s) - "
                f"RM{rate * days:.2f}"
            )

        total = calculate_total(customer.bookings, vehicles)
        st.write(f"**Total: RM{total:.2f}**")

# 5. Add payment
elif choice == "Add Payment":
    amount = st.number_input(
        "Payment Amount (RM)",
        min_value=0.0,
        step=10.0
    )

    if st.button("Add Payment"):
        customer.add_payment(amount)
        st.success(f"Payment added. Current balance: RM{customer.payment:.2f}")

# 6. Checkout
elif choice == "Checkout":
    if len(customer.bookings) == 0:
        st.info("No booking to checkout.")
    else:
        total = calculate_total(customer.bookings, vehicles)

        st.write(f"Total: RM{total:.2f}")
        st.write(f"Payment: RM{customer.payment:.2f}")

        if st.button("Checkout"):
            if customer.payment >= total:
                import random

                booking_id = "CLN-" + str(random.randint(1000, 9999))

                st.success("Checkout successful!")
                st.write("Customer:", customer.customer_name)
                st.write("Booking ID:", booking_id)
                st.write(f"Total: RM{total:.2f}")

                customer.bookings.clear()
                customer.payment = 0
            else:
                st.error("Not enough payment.")

# Simple OOP demonstration
st.divider()
st.subheader("OOP Information")
st.write(str(customer))
st.write("Active bookings:", len(customer))

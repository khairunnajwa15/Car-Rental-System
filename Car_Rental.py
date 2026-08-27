import streamlit as st
import random

# ============================================================
# CAR RENTAL SYSTEM
# Practical Work 2 - Python Programming
# Name: KHAIRUN NAJWA BINTI ROZAIDI
# No.Matrik: 25DIT24F1042
# Class: DIT5B
# ============================================================

# ---------------- FUNCTIONS ----------------

def display_menu():
    menu = [
        "View Available Vehicles",
        "Book Vehicle Rental",
        "Cancel Vehicle Booking",
        "View Rental Booking",
        "Add Payment",
        "Checkout",
        "Exit"
    ]
    return menu


def calculate_total(bookings, vehicles):
    total = 0

    for vehicle_code, days in bookings:
        if vehicle_code in vehicles:
            rate = vehicles[vehicle_code][1]
            total = total + (rate * days)

    return total


# ---------------- PARENT CLASS ----------------

class RentalAgency:

    def __init__(self, agency_name, vehicles):
        self.agency_name = agency_name
        self.vehicles = vehicles

    def display_vehicles(self):
        return self.vehicles

    def get_rate(self, vehicle_code):
        if vehicle_code in self.vehicles:
            return self.vehicles[vehicle_code][1]
        return 0


# ---------------- CHILD CLASS ----------------

class Customer(RentalAgency):

    def __init__(self, agency_name, vehicles, customer_name):
        super().__init__(agency_name, vehicles)

        self.customer_name = customer_name
        self.payment = 0
        self.bookings = []

    def book_vehicle(self, vehicle_code, days):
        if vehicle_code in self.vehicles and days > 0:
            self.bookings.append((vehicle_code, days))
            return True
        return False

    def cancel_booking(self, number):
        if 1 <= number <= len(self.bookings):
            self.bookings.pop(number - 1)
            return True
        return False

    def view_booking(self):
        return self.bookings

    # Optional bonus parameter demonstrates overloading
    def add_payment(self, amount, bonus=0):
        self.payment = self.payment + amount + bonus

    def checkout(self):
        total = calculate_total(self.bookings, self.vehicles)

        if len(self.bookings) == 0:
            return None

        if self.payment >= total:
            booking_id = "CLN-" + str(random.randint(1000, 9999))
            self.bookings.clear()
            self.payment = 0
            return booking_id

        return False

    # Operator overloading
    def __add__(self, other):
        return len(self.bookings) + len(other.bookings)

    # Magic method
    def __str__(self):
        return self.customer_name + " - RM" + str(self.payment)

    # Magic method
    def __len__(self):
        return len(self.bookings)


# ---------------- VEHICLES ----------------

vehicles = {
    101: ("Perodua Myvi", 80),
    102: ("Proton Saga", 70),
    103: ("Honda City", 120),
    104: ("Toyota Vios", 110)
}


# ---------------- CREATE OBJECTS ----------------

if "customer" not in st.session_state:
    st.session_state.customer = Customer(
        "CLN Car Rental",
        vehicles,
        "Customer"
    )

if "customer2" not in st.session_state:
    st.session_state.customer2 = Customer(
        "CLN Car Rental",
        vehicles,
        "Second Customer"
    )

customer = st.session_state.customer
customer2 = st.session_state.customer2


# ---------------- STREAMLIT PAGE ----------------

st.title("Car Rental System")

st.write("### Student Information")
st.write("Be our regular customer to get 15% discount!!")


name = st.text_input("Name")
registration = st.text_input("IC Number")
student_class = st.text_input("Phone Number")

if name:
    customer.customer_name = name


# Use the required display_menu() function
menu = display_menu()

choice = st.selectbox("Choose an option", menu)


# ---------------- VIEW VEHICLES ----------------

if choice == "View Available Vehicles":

    st.write("### Available Vehicles")

    for code, vehicle in customer.display_vehicles().items():
        st.write(
            code, "-", vehicle[0],
            "- RM", vehicle[1], "per day"
        )

# ---------------- BOOK VEHICLE ----------------

elif choice == "Book Vehicle Rental":

    code = st.selectbox(
        "Vehicle Code",
        list(vehicles.keys())
    )

    days = st.number_input(
        "Rental Days",
        min_value=1,
        step=1
    )

    if st.button("Book Vehicle"):

        if customer.book_vehicle(code, days):
            st.success("Vehicle booked successfully.")
        else:
            st.error("Invalid booking.")


# ---------------- CANCEL BOOKING ----------------

elif choice == "Cancel Vehicle Booking":

    if len(customer) == 0:

        st.info("No active booking.")

    else:

        number = st.number_input(
            "Booking Number",
            min_value=1,
            max_value=len(customer),
            step=1
        )

        if st.button("Cancel Booking"):

            if customer.cancel_booking(number):
                st.success("Booking cancelled.")


# ---------------- VIEW BOOKING ----------------

elif choice == "View Rental Booking":

    if len(customer) == 0:

        st.info("No active booking.")

    else:

        st.write("### Your Booking")

        for i, booking in enumerate(customer.view_booking(), 1):

            code = booking[0]
            days = booking[1]

            model = vehicles[code][0]
            rate = customer.get_rate(code)

            st.write(
                i, "-", model,
                "-", days, "day(s)",
                "- RM", rate * days
            )

        total = calculate_total(
            customer.view_booking(),
            vehicles
        )

        st.write("**Total: RM", total, "**")


# ---------------- ADD PAYMENT ----------------

elif choice == "Add Payment":

    amount = st.number_input(
        "Payment Amount (RM)",
        min_value=0.0,
        step=10.0
    )

    bonus = st.number_input(
        "Bonus (RM)",
        min_value=0.0,
        step=5.0
    )

    if st.button("Add Payment"):

        customer.add_payment(amount, bonus)

        st.success("Payment added.")
        st.write("Current payment: RM", customer.payment)


# ---------------- CHECKOUT ----------------

elif choice == "Checkout":

    if len(customer) == 0:

        st.info("No booking to checkout.")

    else:

        total = calculate_total(
            customer.bookings,
            vehicles
        )

        st.write("Total: RM", total)
        st.write("Payment: RM", customer.payment)

        if st.button("Checkout"):

            result = customer.checkout()

            if result is False:
                st.error("Not enough payment.")

            else:
                st.success("Checkout successful.")
                st.write("Customer:", customer.customer_name)
                st.write("Booking ID:", result)


# ---------------- EXIT ----------------

elif choice == "Exit":

    st.info("Thank you for using the Car Rental System.")

# ---------------- FOOTER ----------------
st.write("Customer:", str(customer))
st.write("Active bookings:", len(customer))

st.write(
    "Combined bookings of two Customer objects:",
    customer + customer2
)
st.divider()
st.caption("© 2026 CLN Car Rental | All Rights Reserved")
st.caption("DFK50083 Python Programming — Practical Work 2")

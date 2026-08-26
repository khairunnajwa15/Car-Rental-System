import random

# ============================================================
# CAR RENTAL SYSTEM
# Practical Work 2 - Python Programming
# ============================================================

# Student Information
NAME = "Your Name"
REGISTRATION_NO = "Your Registration Number"
CLASS = "Your Class"


# ------------------------------------------------------------
# Task 1: Define and Call Functions
# ------------------------------------------------------------

def display_menu():
    """Display the main menu."""
    print("\n========== CAR RENTAL SYSTEM ==========")
    print("1. View Available Vehicles")
    print("2. Book Vehicle Rental")
    print("3. Cancel Vehicle Booking")
    print("4. View Rental Booking")
    print("5. Add Payment")
    print("6. Checkout")
    print("7. Exit")
    print("=======================================")


def calculate_total(bookings, vehicles):
    """
    Calculate the total rental cost.

    bookings contains tuples in the form:
    (vehicle_code, days)

    vehicles contains:
    vehicle_code: (model_name, daily_rate)
    """
    total = 0

    for vehicle_code, days in bookings:
        if vehicle_code in vehicles:
            vehicle_info = vehicles[vehicle_code]
            daily_rate = vehicle_info[1]
            total += daily_rate * days

    return total


# ------------------------------------------------------------
# Task 2: Parent Class - RentalAgency
# ------------------------------------------------------------

class RentalAgency:
    def __init__(self, agency_name, vehicles):
        self.agency_name = agency_name
        self.vehicles = vehicles

    def display_vehicles(self):
        print("\n========== AVAILABLE VEHICLES ==========")

        for code, vehicle in self.vehicles.items():
            model_name = vehicle[0]
            daily_rate = vehicle[1]
            print(f"{code}. {model_name} - RM{daily_rate:.2f} per day")

        print("========================================")

    def get_rate(self, vehicle_code):
        if vehicle_code in self.vehicles:
            return self.vehicles[vehicle_code][1]
        return None


# ------------------------------------------------------------
# Task 2: Child Class - Customer
# ------------------------------------------------------------

class Customer(RentalAgency):
    def __init__(self, agency_name, vehicles, customer_name):
        # Inheritance using super()
        super().__init__(agency_name, vehicles)

        self.customer_name = customer_name
        self.payment = 0.0
        self.bookings = []

    def book_vehicle(self, vehicle_code, days):
        if vehicle_code not in self.vehicles:
            print("Invalid vehicle code.")
            return

        if days <= 0:
            print("Rental days must be greater than 0.")
            return

        booking = (vehicle_code, days)
        self.bookings.append(booking)

        model_name = self.vehicles[vehicle_code][0]

        print(f"\nBooking successful!")
        print(f"Vehicle: {model_name}")
        print(f"Rental days: {days}")
        print(f"Cost: RM{self.vehicles[vehicle_code][1] * days:.2f}")

    def cancel_booking(self):
        if len(self.bookings) == 0:
            print("\nThere is no active booking to cancel.")
            return

        self.view_booking()

        try:
            choice = int(input("Enter booking number to cancel: "))

            if 1 <= choice <= len(self.bookings):
                removed = self.bookings.pop(choice - 1)

                vehicle_code = removed[0]
                days = removed[1]
                model_name = self.vehicles[vehicle_code][0]

                print(f"Booking for {model_name} ({days} days) has been cancelled.")
            else:
                print("Invalid booking number.")

        except ValueError:
            print("Please enter a valid number.")

    def view_booking(self):
        if len(self.bookings) == 0:
            print("\nNo active rental booking.")
            return

        print("\n========== RENTAL BOOKING ==========")

        for number, booking in enumerate(self.bookings, start=1):
            vehicle_code = booking[0]
            days = booking[1]

            model_name = self.vehicles[vehicle_code][0]
            daily_rate = self.vehicles[vehicle_code][1]
            cost = daily_rate * days

            print(
                f"{number}. {model_name} | "
                f"{days} day(s) | "
                f"RM{daily_rate:.2f}/day | "
                f"RM{cost:.2f}"
            )

        total = calculate_total(self.bookings, self.vehicles)
        print("-----------------------------------")
        print(f"Total Rental Cost: RM{total:.2f}")
        print(f"Payment Balance: RM{self.payment:.2f}")
        print("===================================")

    def add_payment(self, amount, bonus=0):
        """
        Simulate function overloading by using an optional bonus argument.
        """
        if amount <= 0:
            print("Payment amount must be greater than 0.")
            return

        if bonus < 0:
            print("Bonus cannot be negative.")
            return

        self.payment += amount + bonus

        print("\nPayment added successfully.")
        print(f"Payment: RM{amount:.2f}")
        print(f"Bonus: RM{bonus:.2f}")
        print(f"Current balance: RM{self.payment:.2f}")

    def checkout(self):
        if len(self.bookings) == 0:
            print("\nYou do not have any rental booking.")
            return

        total = calculate_total(self.bookings, self.vehicles)

        if self.payment < total:
            remaining = total - self.payment

            print("\n========== CHECKOUT ==========")
            print(f"Total rental cost : RM{total:.2f}")
            print(f"Current payment   : RM{self.payment:.2f}")
            print(f"Amount remaining  : RM{remaining:.2f}")
            print("Checkout failed. Please add more payment.")
            print("==============================")
            return

        booking_id = f"CLN-{random.randint(1000, 9999)}"

        balance = self.payment - total

        print("\n========== CHECKOUT ==========")
        print(f"Customer       : {self.customer_name}")
        print(f"Booking ID     : {booking_id}")
        print(f"Total cost     : RM{total:.2f}")
        print(f"Payment        : RM{self.payment:.2f}")
        print(f"Balance change : RM{balance:.2f}")
        print("Rental checkout successful!")
        print("==============================")

        # Clear active bookings after successful checkout
        self.bookings.clear()

        # Reset payment for the next rental
        self.payment = 0.0

    # --------------------------------------------------------
    # Task 5: Operator Overloading
    # --------------------------------------------------------

    def __add__(self, other):
        """
        Combine the number of active vehicle rental bookings
        from two Customer objects.
        """
        if isinstance(other, Customer):
            return len(self.bookings) + len(other.bookings)

        return NotImplemented

    # --------------------------------------------------------
    # Task 6: Magic Methods
    # --------------------------------------------------------

    def __str__(self):
        """Return customer identity and current payment balance."""
        return (
            f"Customer: {self.customer_name} | "
            f"Payment Balance: RM{self.payment:.2f}"
        )

    def __len__(self):
        """Return the number of active bookings."""
        return len(self.bookings)


# ------------------------------------------------------------
# Main Program
# ------------------------------------------------------------

def main():

    print("=======================================")
    print("           PRACTICAL WORK 2")
    print("=======================================")
    print(f"Name               : {NAME}")
    print(f"Registration Number: {REGISTRATION_NO}")
    print(f"Class              : {CLASS}")
    print("=======================================")

    # Dictionary using numeric ID keys.
    # Each value is a tuple containing:
    # (Model Name, Daily Rate)
    vehicles = {
        101: ("Perodua Myvi", 80.00),
        102: ("Proton Saga", 70.00),
        103: ("Honda City", 120.00),
        104: ("Toyota Vios", 110.00),
        105: ("Perodua Alza", 100.00)
    }

    agency = RentalAgency("CLN Car Rental", vehicles)

    customer_name = input("\nEnter customer name: ")

    # Customer inherits RentalAgency
    customer = Customer(
        agency.agency_name,
        agency.vehicles,
        customer_name
    )

    # Second Customer object is used to demonstrate __add__()
    customer2 = Customer(
        agency.agency_name,
        agency.vehicles,
        "Demo Customer"
    )

    while True:
        display_menu()

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            customer.display_vehicles()

        elif choice == "2":
            customer.display_vehicles()

            try:
                vehicle_code = int(input("Enter vehicle code: "))
                days = int(input("Enter rental days: "))

                customer.book_vehicle(vehicle_code, days)

            except ValueError:
                print("Please enter numbers only.")

        elif choice == "3":
            customer.cancel_booking()

        elif choice == "4":
            customer.view_booking()

        elif choice == "5":
            try:
                amount = float(input("Enter payment amount: RM"))

                bonus_input = input(
                    "Enter bonus amount (press Enter for 0): RM"
                )

                if bonus_input == "":
                    bonus = 0
                else:
                    bonus = float(bonus_input)

                customer.add_payment(amount, bonus)

            except ValueError:
                print("Please enter a valid payment amount.")

        elif choice == "6":
            customer.checkout()

        elif choice == "7":
            print("\nThank you for using the Car Rental System!")
            break

        else:
            print("\nInvalid choice. Please select 1-7.")

    print("\nProgram ended.")


# ------------------------------------------------------------
# Program Execution
# ------------------------------------------------------------

if __name__ == "__main__":
    main()

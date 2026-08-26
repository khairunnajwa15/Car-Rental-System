import random

NAME = "Your Name"
REGISTRATION_NO = "Your Registration Number"
CLASS = "Your Class"


def display_menu():
    print("\n===== CAR RENTAL SYSTEM =====")
    print("1. View Available Vehicles")
    print("2. Book Vehicle Rental")
    print("3. Cancel Vehicle Booking")
    print("4. View Rental Booking")
    print("5. Add Payment")
    print("6. Checkout")
    print("7. Exit")


def calculate_total(bookings, vehicles):
    total = 0
    for vehicle_code, days in bookings:
        total += vehicles[vehicle_code][1] * days
    return total


class RentalAgency:
    def __init__(self, agency_name, vehicles):
        self.agency_name = agency_name
        self.vehicles = vehicles

    def display_vehicles(self):
        print("\n--- Available Vehicles ---")
        for code, vehicle in self.vehicles.items():
            print(code, "-", vehicle[0], "- RM", vehicle[1], "per day")

    def get_rate(self, vehicle_code):
        return self.vehicles[vehicle_code][1]


class Customer(RentalAgency):
    def __init__(self, agency_name, vehicles, customer_name):
        super().__init__(agency_name, vehicles)
        self.customer_name = customer_name
        self.payment = 0
        self.bookings = []

    def book_vehicle(self, vehicle_code, days):
        if vehicle_code in self.vehicles and days > 0:
            self.bookings.append((vehicle_code, days))
            print("Vehicle booked successfully.")
        else:
            print("Invalid vehicle code or rental days.")

    def cancel_booking(self):
        if len(self.bookings) == 0:
            print("No booking to cancel.")
            return

        self.view_booking()
        try:
            number = int(input("Enter booking number to cancel: "))
            if 1 <= number <= len(self.bookings):
                self.bookings.pop(number - 1)
                print("Booking cancelled.")
            else:
                print("Invalid booking number.")
        except ValueError:
            print("Please enter a number.")

    def view_booking(self):
        if len(self.bookings) == 0:
            print("No active booking.")
            return

        print("\n--- Your Booking ---")
        for i, booking in enumerate(self.bookings, 1):
            code, days = booking
            model = self.vehicles[code][0]
            rate = self.vehicles[code][1]
            print(i, "-", model, "-", days, "day(s) - RM", rate * days)

        print("Total: RM", calculate_total(self.bookings, self.vehicles))

    def add_payment(self, amount, bonus=0):
        self.payment += amount + bonus
        print("Payment added.")
        print("Current payment: RM", self.payment)

    def checkout(self):
        if len(self.bookings) == 0:
            print("No booking to checkout.")
            return

        total = calculate_total(self.bookings, self.vehicles)

        if self.payment >= total:
            booking_id = "CLN-" + str(random.randint(1000, 9999))
            print("\n--- CHECKOUT ---")
            print("Customer:", self.customer_name)
            print("Booking ID:", booking_id)
            print("Total: RM", total)
            print("Payment: RM", self.payment)
            print("Checkout successful.")
            self.bookings.clear()
            self.payment = 0
        else:
            print("Not enough payment.")
            print("Total: RM", total)
            print("Payment: RM", self.payment)

    def __add__(self, other):
        return len(self.bookings) + len(other.bookings)

    def __str__(self):
        return self.customer_name + " - Payment: RM" + str(self.payment)

    def __len__(self):
        return len(self.bookings)


def main():
    print("================================")
    print("       PRACTICAL WORK 2")
    print("================================")
    print("Name:", NAME)
    print("Registration Number:", REGISTRATION_NO)
    print("Class:", CLASS)

    vehicles = {
        101: ("Perodua Myvi", 80),
        102: ("Proton Saga", 70),
        103: ("Honda City", 120),
        104: ("Toyota Vios", 110)
    }

    agency = RentalAgency("CLN Car Rental", vehicles)
    customer_name = input("\nEnter customer name: ")
    customer = Customer(agency.agency_name, agency.vehicles, customer_name)

    customer2 = Customer(agency.agency_name, agency.vehicles, "Second Customer")

    while True:
        display_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            customer.display_vehicles()
        elif choice == "2":
            try:
                code = int(input("Enter vehicle code: "))
                days = int(input("Enter rental days: "))
                customer.book_vehicle(code, days)
            except ValueError:
                print("Please enter numbers only.")
        elif choice == "3":
            customer.cancel_booking()
        elif choice == "4":
            customer.view_booking()
        elif choice == "5":
            try:
                amount = float(input("Enter payment: RM"))
                customer.add_payment(amount)
            except ValueError:
                print("Please enter a valid amount.")
        elif choice == "6":
            customer.checkout()
        elif choice == "7":
            print("Thank you for using the system.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

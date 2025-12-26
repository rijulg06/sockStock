import database
import config

def main_menu():
    """Display main menu and return user's choice."""
    print("\n=== Main Menu ===")
    print("1. Update Mode")
    print("2. View Mode")
    print("3. Exit")

    choice = input("\nEnter your choice (1-3): ")

    # Validate input
    if choice not in ['1', '2', '3']:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return main_menu()  # Ask again

    return int(choice)

def update_mode():
    """Handle update mode operations."""
    print("\n--- Update Mode ---")
    print("update")
    # Later you'll add actual update logic here

def view_mode():
    """Handle view mode operations."""
    print("\n--- View Mode ---")
    print("view")
    # Later you'll add actual view logic here

def main():
    """Main program loop."""
    # Initialize database on startup
    database.init_database()

    while True:
        choice = main_menu()

        if choice == 1:
            update_mode()
        elif choice == 2:
            view_mode()
        elif choice == 3:
            print("\nGoodbye!")
            break  # Exit the loop

if __name__ == "__main__":
    main()
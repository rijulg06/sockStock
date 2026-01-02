#!/usr/bin/env python3
"""
Sock Factory Inventory Management System - Main Entry Point

A command-line interface for managing sock inventory through production stages.
Run with: ./main.py or python3 main.py
"""

import database
import config
from tabulate import tabulate

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
    print("1. Add new stock")
    print("2. Move stock")
    print("3. Undo last operation")
    print("4. Back")

    choice = input("\nEnter your choice (1-4): ")

    # Validate input
    if choice not in ['1', '2', '3', '4']:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        return update_mode()  # Ask again

    choice = int(choice)

    if choice == 1:
        # Add new stock
        try:
            quality = input('\nQuality: ')
            color = input('Color: ')
            size = input('Size: ')
            quantity = int(input('Quantity: '))

            database.add_stock(quality, color, size, quantity)

            # Confirmation message
            print(f"\n✓ Successfully added {quantity} units of {color} {size} socks (Quality {quality}) to Order stage")

        except ValueError as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Failed to add stock: {e}")

    elif choice == 2:
        # Move stock - show current inventory first
        inventory = database.get_all_inventory()
        if not inventory:
            print("No inventory to move. Add stock first!")
            return
        
        try:
            print("\n--- Select Sock to Move ---")
            quality = input('Quality: ')
            color = input('Color: ')
            size = input('Size: ')

            # Find variant
            variants = database.find_variant_id(quality, color, size)
            if not variants:
                print(f"\n✗ No stock found for {color} {size} socks (Quality {quality})")
                return

            variant_id = variants[0]

            # Get stage to move from
            ch = stage_change()
            source_stage = config.STAGES[ch - 1]  # Convert choice to stage name

            quantity = int(input("\nQuantity to move: "))

            # Move the stock
            result = database.move_stock(variant_id, source_stage, quantity)

            if result['success']:
                print(f"\n✓ Successfully moved {result['quantity_moved']} units")
                print(f"  From: {result['source_stage']} (remaining: {result['source_remaining']})")
                print(f"  To: {result['destination_stage']} (new total: {result['destination_total']})")
            else:
                print(f"\n✗ Failed to move stock")

        except ValueError as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Failed to move stock: {e}")

    elif choice == 3:
        # Remove last entry
        try:
            result = database.remove_stock()

            if result['success']:
                info = result['deleted_info']
                print(f"\n✓ Successfully removed last entry:")
                print(f"  {info['quantity']} units of {info['color']} {info['size']} socks (Quality {info['quality']})")
                print(f"  From stage: {info['stage']}")

                if result['variant_deleted']:
                    print(f"  Note: Variant fully removed (no remaining inventory)")
            else:
                print("\n✗ Failed to remove stock")

        except ValueError as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Failed to remove stock: {e}")

    elif choice == 4:
        return

def stage_change():
    print('\nWhich stage are you changing?')
    print('1. Order --> Raw Made')
    print('2. Raw Made --> Sent for Press')
    print('3. Sent for Press --> Ready Stock')
    print('4. Ready Stock --> Dispatch')

    choice = input("\nEnter your choice (1-4): ")

    # Validate input
    if choice not in ['1', '2', '3', '4']:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        return stage_change()  # Ask again
    
    return int(choice)

def view_mode():
    """Handle view mode operations."""
    print("\n--- View Mode ---")
    print("1. Show all stock")
    print("2. Show summary")
    print("3. Filter Stock")
    print("4. Back")

    choice = input("\nEnter your choice (1-4): ")

    # Validate input
    if choice not in ['1', '2', '3', '4']:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        return view_mode()  # Ask again
    
    choice = int(choice)

    if choice == 1:
        display(database.get_all_inventory())

    elif choice == 2:
        display_summary(database.get_stock_summary())

    elif choice == 3:
        display(filter_inventory())

    elif choice == 4:
        # Back to main menu - just return
        return

def display(rows):
    """Display inventory data in a formatted table."""
    if not rows:
        print("\nNo inventory found.")
        return

    print(tabulate(rows, headers="keys", tablefmt="fancy_outline"))

def display_summary(summary):
    """Display inventory summary with totals per stage."""
    print("\n=== Stock Summary by Stage ===")

    # Convert dict to list of lists for tabulate
    table_data = [[stage, quantity] for stage, quantity in summary.items()]

    print(tabulate(table_data, headers=["Stage", "Total Quantity"], tablefmt="fancy_outline"))

    # Show grand total
    total = sum(summary.values())
    print(f"\nGrand Total: {total} units across all stages")

def filter_inventory():

    filters = {}
    while True:
        choice = filter()

        if choice == 1:
            now = input("Specify quality: ")
            filters['quality'] = now
            print_filters(filters)
        elif choice == 2:
            now = input("Specify color: ")
            filters['color'] = now
            print_filters(filters)
        elif choice == 3:
            now = input("Specify size: ")
            filters['size'] = now
            print_filters(filters)
        else:
            print_filters(filters)
            break

    # If no filters applied, return all inventory
    if not filters:
        print("\nNo filters applied - showing all inventory")
        return database.get_all_inventory()

    return database.filter_inventory(**filters)

def print_filters(filters):
    print("\nFilters set:")
    print(f'Quality: {filters.get("quality", "N/A")}')
    print(f'Color: {filters.get("color", "N/A")}')
    print(f'size: {filters.get("size", "N/A")}\n')

def filter():
    print("\n--- Filters ---")
    print("What filters do you want to apply? Let's go one-by-one.")
    print("1. Quality")
    print("2. Color")
    print("3. Size")
    print("4. Done")

    choice = input("\nEnter your choice (1-4): ")

    # Validate input
    if choice not in ['1', '2', '3', '4']:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        return filter()  # Ask again
    
    return int(choice)


def main():
    """Main program loop."""
    # Initialize database on startup
    print('\nHello Roopa Enterprises.')
    database.init_database()
    print('Database ready!')

    try:
        while True:
            choice = main_menu()

            if choice == 1:
                update_mode()
            elif choice == 2:
                view_mode()
            elif choice == 3:
                print("\nGoodbye!")
                break  # Exit the loop

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nProgram interrupted. Goodbye!")

if __name__ == "__main__":
    main()
"""
Configuration constants for the Sock Factory Inventory Management System.
"""
import os
import sys

# Inventory stages in order of production flow
STAGES = ["Order", "Raw Made", "Sent for Press", "Ready Stock", "Dispatch"]

# Database file path - always in the same directory as the executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    DB_PATH = os.path.join(os.path.dirname(sys.executable), 'inventory.db')
else:
    # Running as script
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventory.db')

# Stage transition map: defines which stage follows which
STAGE_TRANSITIONS = {
    "Order": "Raw Made",
    "Raw Made": "Sent for Press",
    "Sent for Press": "Ready Stock",
    "Ready Stock": "Dispatch",
    "Dispatch": None  # Final stage, no next stage
}

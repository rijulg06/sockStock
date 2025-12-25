"""
Configuration constants for the Sock Factory Inventory Management System.
"""

# Inventory stages in order of production flow
STAGES = ["Order", "Raw Made", "Sent for Press", "Ready Stock", "Dispatch"]

# Database file path
DB_PATH = "data/inventory.db"

# Stage transition map: defines which stage follows which
STAGE_TRANSITIONS = {
    "Order": "Raw Made",
    "Raw Made": "Sent for Press",
    "Sent for Press": "Ready Stock",
    "Ready Stock": "Dispatch",
    "Dispatch": None  # Final stage, no next stage
}

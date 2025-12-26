"""
Database operations for the Sock Factory Inventory Management System.

This module handles all SQLite database interactions including:
- Database initialization and schema creation
- Stock addition and movement between stages
- Inventory queries and reporting
"""

import sqlite3
import config


def init_database():
    """
    Initialize the database and create tables if they don't exist.

    Creates two tables:
    - sock_variants: Stores unique combinations of quality, color, and size
    - inventory: Tracks quantity for each variant at each production stage
    """
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    # Create sock_variants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sock_variants (
            variant_id INTEGER PRIMARY KEY,
            quality TEXT NOT NULL,
            color TEXT NOT NULL,
            size TEXT NOT NULL,
            UNIQUE(quality, color, size)
        )
    """)

    # Create inventory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            variant_id INTEGER NOT NULL,
            stage TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (variant_id) REFERENCES sock_variants(variant_id),
            UNIQUE(variant_id, stage),
            CHECK(stage IN ('Order', 'Raw Made', 'Sent for Press',
                           'Ready Stock', 'Dispatch')),
            CHECK(quantity >= 0)
        )
    """)

    conn.commit()
    conn.close()


def find_variant_id(quality=None, color=None, size=None):
    """
    Find variant_id(s) matching the specified attributes.

    Can search by any combination of quality, color, and/or size.
    At least one parameter must be provided.

    Args:
        quality (str, optional): Quality grade of the sock (e.g., 'Premium', 'Standard')
        color (str, optional): Color of the sock (e.g., 'Red', 'Blue')
        size (str, optional): Size of the sock (e.g., 'S', 'M', 'L')

    Returns:
        list: List of matching variant_ids (empty list if no matches found)

    Raises:
        ValueError: If no search parameters are provided

    Examples:
        >>> find_variant_id(color="Red")
        [1, 2, 3, 4]  # All red sock variants

        >>> find_variant_id(quality="Premium", size="M")
        [5, 12, 18]  # All premium medium socks

        >>> find_variant_id(quality="Premium", color="Red", size="M")
        [51]  # Specific variant
    """
    # Validate that at least one parameter is provided
    if quality is None and color is None and size is None:
        raise ValueError("At least one search parameter (quality, color, or size) must be provided")

    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    # Build WHERE clause dynamically based on provided parameters
    conditions = []
    params = []

    if quality is not None:
        conditions.append("quality = ?")
        params.append(quality)

    if color is not None:
        conditions.append("color = ?")
        params.append(color)

    if size is not None:
        conditions.append("size = ?")
        params.append(size)

    # Join conditions with AND
    where_clause = " AND ".join(conditions)
    query = f"SELECT variant_id FROM sock_variants WHERE {where_clause}"

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    # Extract variant_ids from tuples and return as list
    return [row[0] for row in results]

def add_stock(quality, color, size, quantity):
    """
    Add stock to the "Order" stage for a specific sock variant.

    If the variant doesn't exist, it will be created. If stock already exists
    in the Order stage, the quantity will be added to the existing amount.

    Args:
        quality (str): Quality grade of the sock (e.g., 'Premium', 'Standard')
        color (str): Color of the sock (e.g., 'Red', 'Blue')
        size (str): Size of the sock (e.g., 'S', 'M', 'L')
        quantity (int): Quantity to add (must be positive)

    Raises:
        ValueError: If quantity is not positive

    Example:
        >>> add_stock('Premium', 'Red', 'M', 100)
        >>> add_stock('Premium', 'Red', 'M', 50)  # Now 150 total in Order stage
    """
    # Validate input
    if quantity <= 0:
        raise ValueError(f"Quantity must be positive, got {quantity}")

    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    try:
        # Start transaction (implicit with first execute)

        # Step 1: Create variant if it doesn't exist
        cursor.execute("""
            INSERT OR IGNORE INTO sock_variants (quality, color, size)
            VALUES (?, ?, ?)
        """, (quality, color, size))

        # Step 2: Get the variant_id (within same connection/transaction)
        cursor.execute("""
            SELECT variant_id FROM sock_variants
            WHERE quality = ? AND color = ? AND size = ?
        """, (quality, color, size))

        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Failed to create/find variant: {quality} {color} {size}")

        variant_id = result[0]

        # Step 3: Add/update inventory in Order stage
        cursor.execute("""
            INSERT INTO inventory (variant_id, stage, quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(variant_id, stage)
            DO UPDATE SET
                quantity = inventory.quantity + excluded.quantity
        """, (variant_id, 'Order', quantity))

        # Commit transaction
        conn.commit()

    except Exception as e:
        # Rollback on any error
        conn.rollback()
        raise Exception(f"Failed to add stock: {e}")

    finally:
        # Always close connection
        conn.close()
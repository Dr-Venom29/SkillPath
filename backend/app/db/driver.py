"""
Neo4j driver management.
Creates a shared driver at app startup and closes it on shutdown.
Provides a simple connection verification helper.
"""

from neo4j import GraphDatabase, Driver
from typing import Optional

_driver: Optional[Driver] = None


def create_driver(uri: str, username: str, password: str) -> None:
    """Instantiate a global Neo4j driver.
    Subsequent calls replace any existing driver.
    """
    global _driver
    if _driver is not None:
        _driver.close()
    _driver = GraphDatabase.driver(uri, auth=(username, password))


def get_driver() -> Driver:
    """Return the shared driver. Raises if not initialized."""
    if _driver is None:
        raise RuntimeError("Neo4j driver has not been created yet.")
    return _driver


def get_session():
    """Provide a Neo4j session from the shared driver.

    Usage:
        with get_session() as session:
            result = session.run("MATCH ...")
    """
    return get_driver().session()


def verify_connection() -> bool:
    """Run a lightweight query to assert connectivity.
    Returns True if successful, otherwise propagates the exception.
    """
    driver = get_driver()
    with driver.session() as session:
        session.run("RETURN 1").single()
    return True


def close_driver() -> None:
    """Close the shared driver if it exists."""
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None

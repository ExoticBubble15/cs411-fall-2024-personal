from contextlib import contextmanager
import re
import sqlite3

import pytest


########################################################
# FIXTURES
########################################################
from meal_max.models.kitchen_model import (
    Meal,
    create_meal,
    clear_meals,
    delete_meal,
    get_leaderboard,
    get_meal_by_id,
    get_meal_by_name,
    update_meal_stats
)

def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()

# Mocking the database connection for tests
@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object

    mocker.patch("meal_max.models.kitchen_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

########################################################
# ADD AND DELETE
########################################################
def test_create_meal(mock_cursor):
    """Testing creating a new meal."""

    create_meal(meal="Meal", cuisine="Cuisine", price=12.34, difficulty="MED")

    expected_query = normalize_whitespace("""
        INSERT INTO meals (meal, cuisine, price, difficulty)
        VALUES (?, ?, ?, ?)
    """)

    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert expected_query == actual_query

    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = ("Meal", "Cuisine", 12.34, "MED")
    assert actual_arguments == expected_arguments

def test_create_meal_duplicate(mock_cursor):
    """Test error creating a song with a duplicate name"""

    mock_cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed: meal.name")

    with pytest.raises(ValueError, match="Meal with name 'Meal' already exists"):
        create_meal(meal="Meal", cuisine="Cuisine", price=12.34, difficulty="MED")

def test_create_meal_invalid_price(mock_cursor):
    """Test error creating a meal with an invalid price (non-float, negative price)"""

    #non-float price
    with pytest.raises(ValueError, match="Invalid price: invalid. Price must be a positive number."):
        create_meal(meal="Meal", cuisine="Cuisine", price="invalid", difficulty="MED")

    #negative float price
    with pytest.raises(ValueError, match="Invalid price: -1.2. Price must be a positive number."):
        create_meal(meal="Meal", cuisine="Cuisine", price=-1.2, difficulty="MED")

def test_create_meal_invalid_difficulty(mock_cursor):
    """Test error creating a meal with an invalid difficulty (not 'LOW', 'MED', or 'HIGH')"""

    with pytest.raises(ValueError, match="Invalid difficulty level: invalid. Must be 'LOW', 'MED', or 'HIGH'."):
        create_meal(meal="Meal", cuisine="Cuisine", price=12.34, difficulty="invalid")

def test_delete_meal(mock_cursor):
    """Test deleting a meal by id"""

    mock_cursor.fetchone.return_value = ([False])

    delete_meal(1)

    expected_select_sql = normalize_whitespace("SELECT deleted FROM meals WHERE id = ?")
    expected_update_sql = normalize_whitespace("UPDATE meals SET deleted = TRUE WHERE id = ?")

    actual_select_sql = normalize_whitespace(mock_cursor.execute.call_args_list[0][0][0])
    actual_update_sql = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])

    assert actual_select_sql == expected_select_sql, "The SELECT query did not match the expected structure."
    assert actual_update_sql == expected_update_sql, "The UPDATE query did not match the expected structure."

    expected_select_args = (1,)
    expected_update_args = (1,)

    actual_select_args = mock_cursor.execute.call_args_list[0][0][1]
    actual_update_args = mock_cursor.execute.call_args_list[1][0][1]

    assert actual_select_args == expected_select_args, f"The SELECT query arguments did not match. Expected {expected_select_args}, got {actual_select_args}."
    assert actual_update_args == expected_update_args, f"The UPDATE query arguments did not match. Expected {expected_update_args}, got {actual_update_args}."

def test_delete_meal_bad_id(mock_cursor):
    """Test error when trying to delete a meal with a non-existent id."""

    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="Meal with ID 999 not found"):
        delete_meal(999)

def test_delete_meal_deleted(mock_cursor):
    """Test error when tyring to delete a meal that's already been marked as deleted."""

    mock_cursor.fetchone.return_value = ([True])

    with pytest.raises(ValueError, match="Meal with ID 999 has been deleted"):
        delete_meal(999)

def test_clear_meals(mock_cursor, mocker):
    """Test clearing the meal table (removes all meals)"""

    mocker.patch.dict('os.environ', {'SQL_CREATE_TABLE_PATH': 'sql/create_meal_table.sql'})
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="The body of the create statement"))

    clear_meals()

    mock_open.assert_called_once_with('sql/create_meal_table.sql', 'r')

    mock_cursor.executescript.assert_called_once()

########################################################
# GET MEAL
########################################################
def test_get_meal_by_id(mock_cursor):
    """Test getting a meal by its id."""

    mock_cursor.fetchone.return_value = (1, "Meal", "Cuisine", 12.34, "MED", False)

    result = get_meal_by_id(1)

    expected_result = Meal(1, "Meal", "Cuisine", 12.34, "MED")

    assert result == expected_result, f"Expected {expected_result}, got {result}"

    expected_query = normalize_whitespace("SELECT id, meal, cuisine, price, difficulty, deleted FROM meals WHERE id = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args[0][1]

    expected_arguments = (1,)
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."

def test_get_meal_by_bad_id(mock_cursor):
    """Test error getting a meal with a bad id."""
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="Meal with ID 999 not found"):
        get_meal_by_id(999)

def test_get_meal_by_id_deleted(mock_cursor):
    """Test error getting a meal by id that has been deleted."""
    mock_cursor.fetchone.return_value = (999, "Meal", "Cuisine", 12.34, "MED", True)

    with pytest.raises(ValueError, match="Meal with ID 999 has been deleted"):
        get_meal_by_id(999)

def test_get_meal_by_name(mock_cursor):
    """Test getting meal by name"""
    mock_cursor.fetchone.return_value = (1, "Meal", "Cuisine", 12.34, "MED", False)

    result = get_meal_by_name("Meal")

    expected_result = Meal(1, "Meal", "Cuisine", 12.34, "MED")

    assert result == expected_result, f"Expected {expected_result}, got {result}"

    expected_query = normalize_whitespace("SELECT id, meal, cuisine, price, difficulty, deleted FROM meals WHERE meal = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args[0][1]

    expected_arguments = ('Meal',)
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."

def test_get_meal_by_name_deleted(mock_cursor):
    """Test error getting a meal by name that has been deleted."""
    mock_cursor.fetchone.return_value = (999, "Meal", "Cuisine", 12.34, "MED", True)

    with pytest.raises(ValueError, match="Meal with name 999 has been deleted"):
        get_meal_by_name(999)

def test_get_meal_by_name_bad_name(mock_cursor):
    """Test error getting a meal by a non-existent name."""
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="Meal with name Meal not found"):
        get_meal_by_name("Meal")

def test_get_leaderboard(mock_cursor):
    """Test getting leaderboard with no parameter."""
    mock_cursor.fetchall.return_value = [
        (3, "Meal 3", "Cuisine 3", 34.56, "HIGH", 3, 3, .05, True),
        (2, "Meal 2", "Cuisine 2", 23.45, "MED", 2, 2, .9, False),
        (1, "Meal 1", "Cuisine 1", 12.34, "LOW", 1, 1, .1, False)
    ]

    leaderboard = get_leaderboard()

    expected_result = [
        {"id":3, "meal":"Meal 3", "cuisine":"Cuisine 3", "price":34.56, "difficulty":"HIGH", "battles":3, "wins":3, "win_pct":5.0},
        {"id":2, "meal":"Meal 2", "cuisine":"Cuisine 2", "price":23.45, "difficulty":"MED", "battles":2, "wins":2, "win_pct":90.0},
        {"id":1, "meal":"Meal 1", "cuisine":"Cuisine 1", "price":12.34, "difficulty":"LOW", "battles":1, "wins":1, "win_pct":10.0}
    ]

    assert leaderboard == expected_result, f"Expected {expected_result}, but got {leaderboard}"

    expected_query = normalize_whitespace("""
         SELECT id, meal, cuisine, price, difficulty, battles, wins, (wins * 1.0 / battles) AS win_pct
        FROM meals WHERE deleted = false AND battles > 0 ORDER BY wins DESC
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

def test_get_leaderboard_wins(mock_cursor):
    """Test getting leaderboard with "wins" as parameter."""
    mock_cursor.fetchall.return_value = [
        (3, "Meal 3", "Cuisine 3", 34.56, "HIGH", 3, 3, .05, True),
        (2, "Meal 2", "Cuisine 2", 23.45, "MED", 2, 2, .9, False),
        (1, "Meal 1", "Cuisine 1", 12.34, "LOW", 1, 1, .1, False)
    ]

    leaderboard = get_leaderboard("wins")

    expected_result = [
        {"id":3, "meal":"Meal 3", "cuisine":"Cuisine 3", "price":34.56, "difficulty":"HIGH", "battles":3, "wins":3, "win_pct":5.0},
        {"id":2, "meal":"Meal 2", "cuisine":"Cuisine 2", "price":23.45, "difficulty":"MED", "battles":2, "wins":2, "win_pct":90.0},
        {"id":1, "meal":"Meal 1", "cuisine":"Cuisine 1", "price":12.34, "difficulty":"LOW", "battles":1, "wins":1, "win_pct":10.0}
    ]

    assert leaderboard == expected_result, f"Expected {expected_result}, but got {leaderboard}"

    expected_query = normalize_whitespace("""
         SELECT id, meal, cuisine, price, difficulty, battles, wins, (wins * 1.0 / battles) AS win_pct
        FROM meals WHERE deleted = false AND battles > 0 ORDER BY wins DESC
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

def test_get_leaderboard_win_pct(mock_cursor):
    """Test getting leaderboard with "win_pct" as parameter."""
    mock_cursor.fetchall.return_value = [
        (3, "Meal 3", "Cuisine 3", 34.56, "HIGH", 3, 1, .11, True),
        (2, "Meal 2", "Cuisine 2", 23.45, "MED", 2, 3, .10, False),
        (1, "Meal 1", "Cuisine 1", 12.34, "LOW", 1, 2, .01, False)
    ]

    leaderboard = get_leaderboard("win_pct")

    expected_result = [
        {"id":3, "meal":"Meal 3", "cuisine":"Cuisine 3", "price":34.56, "difficulty":"HIGH", "battles":3, "wins":1, "win_pct":11.0},
        {"id":2, "meal":"Meal 2", "cuisine":"Cuisine 2", "price":23.45, "difficulty":"MED", "battles":2, "wins":3, "win_pct":10.0},
        {"id":1, "meal":"Meal 1", "cuisine":"Cuisine 1", "price":12.34, "difficulty":"LOW", "battles":1, "wins":2, "win_pct":1.0}
    ]

    assert leaderboard == expected_result, f"Expected {expected_result}, but got {leaderboard}"

    expected_query = normalize_whitespace("""
         SELECT id, meal, cuisine, price, difficulty, battles, wins, (wins * 1.0 / battles) AS win_pct
        FROM meals WHERE deleted = false AND battles > 0 ORDER BY win_pct DESC
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

def test_get_leaderboard_bad_sort_by(mock_cursor):
    """Test error getting leaderboard with an invalid parameter (not "", "wins", or "win_pct")."""
    with pytest.raises(ValueError, match="Invalid sort_by parameter: invalid"):
        get_leaderboard("invalid")

def test_update_meal_stats_valid_id_valid_result(mock_cursor):
    """Test updating meal stats if meal with id exists and has a valid result (win or loss)."""
    mock_cursor.fetchone.return_value = [False]

    meal_id = 1
    result = "win"
    update_meal_stats(meal_id, result)

    expected_query = normalize_whitespace("""
        UPDATE meals SET battles = battles + 1, wins = wins + 1 WHERE id = ?
    """)

    actual_query = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args_list[1][0][1]

    expected_arguments = (meal_id,)
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."

def test_update_meal_stats_valid_id_invalid_result(mock_cursor):
    """Test error updating meal stats if meal with id exists and has an invalid result (not win or loss)."""
    mock_cursor.fetchone.return_value = [False]

    meal_id = 1
    result = "invalid"

    with pytest.raises(ValueError, match="Invalid result: invalid. Expected 'win' or 'loss'."):
        update_meal_stats(meal_id, result)

def test_update_meal_stats_deleted(mock_cursor):
    """Test error updating meal stats if meal has already been deleted."""
    mock_cursor.fetchone.return_value = [True]

    meal_id = 1
    result = "win"

    with pytest.raises(ValueError, match="Meal with ID 1 has been deleted"):
        update_meal_stats(meal_id, result)

def test_update_meal_stats_deleted_meal(mock_cursor):
    """Test error updating meal stats for a non-existent meal."""
    mock_cursor.fetchone.return_value = None

    meal_id = 1
    result = "win"

    with pytest.raises(ValueError, match="Meal with ID 1 not found"):
        update_meal_stats(meal_id, result)

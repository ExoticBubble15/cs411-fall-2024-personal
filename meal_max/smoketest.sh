#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###################################
# HEALTH CHECKS
###################################
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

###################################
# MEAL CHECKS
################################### 

clear_meals() {
  echo "Clearing the kitchen..."
  curl -s -X DELETE "$BASE_URL/clear-meals" | grep -q '"status": "success"'
}

create_meal() {
    meal = $1
    cuisine = $2
    price = $3
    difficulty = $4

    echo "Adding meal ($meal - $cuisine) to the kitchen..."
    curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
        -d "{\"meal\":\"$meal\", \"cuisine\":\"$cuisine\", \"price\":$price, \"difficulty\":\"$difficulty\"}" | grep -q '"status": "success"'

    if [ $? -eq 0 ]; then
        echo "Meal added successfully."
    else
        echo "Failed to add meal."
        exit 1
    fi
}

delete_meal_by_id() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    exit 1
  fi
}

get_meal_by_id() {
  meal_id=$1

  echo "Getting meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (ID $meal_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by ID ($meal_id)."
    exit 1
  fi
}

get_meal_by_name() {
  meal_name=$1

  echo "Getting meal by name ($meal_name)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-name/$meal_name")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by name ($meal_name)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (name $meal_name):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by name ($meal_name)."
    exit 1
  fi
}

###################################
# BATTLE
################################### 
clear_combatants() {
  echo "Clearing combatants..."
  response=$(curl -s -X POST "$BASE_URL/clear-combatants")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatants cleared successfully."
  else
    echo "Failed to clear combatants."
    exit 1
  fi
}

get_combatants() {
  echo "Getting combatants..."
  response=$(curl -s -X GET "$BASE_URL/get-combatants")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatants successfully retrieved."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to get combatants"
    exit 1
  fi
}

battle() {
  echo "Fighting 2 meals..."
  response=$(curl -s -X GET "$BASE_URL/battle")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Battle successfully completed."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to get complete battle"
    exit 1
  fi
}

prep_combatant() {
  meal=$1

  echo "Preparing meal (Meal:'$meal')..."
  response=$(curl -s -X POST "$BASE_URL/prep-combatant")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal successfully prepared."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (by meal name):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to prepare meal."
    exit 1
  fi
}

###################################
# LEADERBOARD
################################### 
get_leaderboard() {
  echo "Getting leaderboard..."
  response=$(curl -s -X GET "$BASE_URL/get-leaderboard")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON (sorted by wins):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get leaderboard."
    exit 1
  fi
}

check_health
check_db

clear_meals

create_meal "Tacos" "Mexican" 2.50 LOW
create_meal "Ramen" "Japanese" 13.75 MED
create_meal "Lamb" "French" 19.99 HIGH

get_meal_by_id 1
delete_meal_by_id 1

get_meal_by_name "Ramen"

get_meal_by_name "Lamb"
delete_meal_by_id 3

prep_combatant "Tacos"
get_combatants
clear_combatants

prep_combatant "Ramen"
prep_combatant "Lamb"
get_combatants
battle

get_leaderboard
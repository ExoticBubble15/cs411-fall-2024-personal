from typing import Any, List, Optional

from wildlife_tracker.animal_management.animal import Animal
from wildlife_tracker.habitat_management.habitat import Habitat
from wildlife_tracker.migration_tracking.migration_path import MigrationPath
from wildlife_tracker.migration_tracking.migration import Migration

age: Optional[int] = None #animal
animal_id: int #animal
animals: dict[int, Animal] = {} #animal_manager 
animals: List[int] = [] #habitat
current_date: str #migration
current_location: str #migration
destination: Habitat #migration_path
duration: Optional[int] = None #migration_path
environment_type: str #habitat
geographic_area: str #habitat
habitat_id: int #habitat
habitats: dict[int, Habitat] = {} #habitat_manager
health_status: Optional[str] = None #animal
migration_id: int #migration
migration_path: MigrationPath #migration
migrations: dict[int, Migration] = {} #migration_manager
path_id: int #migration_path
paths: dict[int, MigrationPath] = {} #migration_manager
size: int #habitat
species: str #animal
species: str #migration_path
start_date: str #migration
start_location: Habitat #migration_path
status: str = "Scheduled" #migration


def assign_animals_to_habitat(animals: List[Animal]) -> None:
    pass #habitat

def assign_animals_to_habitat(habitat_id: int, animals: List[Animal]) -> None:
    pass #habitat_manager

def cancel_migration(migration_id: int) -> None:
    pass #migration_manager

def create_habitat(habitat_id: int, geographic_area: str, size: int, environment_type: str) -> Habitat:
    pass #habitat_manager

def create_migration_path(species: str, start_location: Habitat, destination: Habitat, duration: Optional[int] = None) -> None:
    pass #migration_path

def get_animal_by_id(animal_id: int) -> Optional[Animal]:
    pass #animal_manager

def get_animal_details(animal_id) -> dict[str, Any]:
    pass #animal_manager

def get_animals_in_habitat(habitat_id: int) -> List[Animal]:
    pass #habitat_manager

def get_habitat_by_id(habitat_id: int) -> Habitat:
    pass #habitat_manager

def get_habitat_details(habitat_id: int) -> dict:
    pass #habitat_manager

def get_habitats_by_geographic_area(geographic_area: str) -> List[Habitat]:
    pass #habitat_manager

def get_habitats_by_size(size: int) -> List[Habitat]:
    pass #habitat_manager

def get_habitats_by_type(environment_type: str) -> List[Habitat]:
    pass #habitat_manager

def get_migration_by_id(migration_id: int) -> Migration:
    pass #migration_manager

def get_migration_details(migration_id: int) -> dict[str, Any]:
    pass #migration_manager

def get_migration_path_by_id(path_id: int) -> MigrationPath:
    pass #migration_manager

def get_migration_paths() -> list[MigrationPath]:
    pass #migration_manager

def get_migration_paths_by_destination(destination: Habitat) -> list[MigrationPath]:
    pass #migration_manager

def get_migration_paths_by_species(species: str) -> list[MigrationPath]:
    pass #migration_manager

def get_migration_paths_by_start_location(start_location: Habitat) -> list[MigrationPath]:
    pass #migration_manager

def get_migrations() -> list[Migration]:
    pass #migration_manager

def get_migrations_by_current_location(current_location: str) -> list[Migration]:
    pass #migration_manager

def get_migrations_by_migration_path(migration_path_id: int) -> list[Migration]:
    pass #migration_manager

def get_migrations_by_start_date(start_date: str) -> list[Migration]:
    pass #migration_manager

def get_migrations_by_status(status: str) -> list[Migration]:
    pass #migration_manager

def get_migration_path_details(path_id) -> dict:
    pass #migration_manager

def register_animal(animal: Animal) -> None:
    pass #animal_manager

def remove_animal(animal_id: int) -> None:
    pass #animal_manager

def remove_habitat(habitat_id: int) -> None:
    pass #habitat_manager

def remove_migration_path(path_id: int) -> None:
    pass #migration_manager

def schedule_migration(migration_path: MigrationPath) -> None:
    pass #migration

def update_animal_details(animal_id: int, **kwargs: Any) -> None:
    pass #animal_manager

def update_habitat_details(habitat_id: int, **kwargs: dict[str, Any]) -> None:
    pass #habitat_manager

def update_migration_details(migration_id: int, **kwargs: Any) -> None:
    pass #migration_manager

def update_migration_path_details(path_id: int, **kwargs) -> None:
    pass #migration_manager

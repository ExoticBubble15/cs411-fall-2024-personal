from typing import Any, List, Optional

from wildlife_tracker.animal_managment.animal import Animal
from wildlife_tracker.habitat_managment.animal import Habitat
from wildlife_tracker.migration_manager.migration_path import MigrationPath
from wildlife_tracker.migration_manager.migration import Migration

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


def assign_animals_to_habitat(animals: List[Animal]) -> None: #habitat
    pass

def assign_animals_to_habitat(habitat_id: int, animals: List[Animal]) -> None: #habitat_manager
    pass

def cancel_migration(migration_id: int) -> None: #migration_manager
    pass

def create_habitat(habitat_id: int, geographic_area: str, size: int, environment_type: str) -> Habitat: #habitat_manager
    pass

def create_migration_path(species: str, start_location: Habitat, destination: Habitat, duration: Optional[int] = None) -> None: #migration_path
    pass

def get_animal_by_id(animal_id: int) -> Optional[Animal]: #animal_manager
    pass

def get_animal_details(animal_id) -> dict[str, Any]: #animal_manager
    pass

def get_animals_in_habitat(habitat_id: int) -> List[Animal]: #habitat_manager
    pass

def get_habitat_by_id(habitat_id: int) -> Habitat: #habitat_manager
    pass

def get_habitat_details(habitat_id: int) -> dict: #habitat_manager
    pass

def get_habitats_by_geographic_area(geographic_area: str) -> List[Habitat]: #habitat_manager
    pass

def get_habitats_by_size(size: int) -> List[Habitat]: #habitat_manager
    pass

def get_habitats_by_type(environment_type: str) -> List[Habitat]: #habitat_manager
    pass

def get_migration_by_id(migration_id: int) -> Migration: #migration_manager
    pass

def get_migration_details(migration_id: int) -> dict[str, Any]: #migration_manager
    pass

def get_migration_path_by_id(path_id: int) -> MigrationPath: #migration_manager
    pass

def get_migration_paths() -> list[MigrationPath]: #migration_manager
    pass

def get_migration_paths_by_destination(destination: Habitat) -> list[MigrationPath]: #migration_manager
    pass

def get_migration_paths_by_species(species: str) -> list[MigrationPath]: #migration_manager
    pass

def get_migration_paths_by_start_location(start_location: Habitat) -> list[MigrationPath]: #migration_manager
    pass

def get_migrations() -> list[Migration]: #migration_manager
    pass

def get_migrations_by_current_location(current_location: str) -> list[Migration]: #migration_manager
    pass

def get_migrations_by_migration_path(migration_path_id: int) -> list[Migration]: #migration_manager
    pass

def get_migrations_by_start_date(start_date: str) -> list[Migration]: #migration_manager
    pass

def get_migrations_by_status(status: str) -> list[Migration]: #migration_manager
    pass

def get_migration_path_details(path_id) -> dict: #migration_manager
    pass

def register_animal(animal: Animal) -> None: #animal_manager
    pass

def remove_animal(animal_id: int) -> None: #animal_manager
    pass

def remove_habitat(habitat_id: int) -> None: #habitat_manager
    pass

def remove_migration_path(path_id: int) -> None: #migration_manager
    pass

def schedule_migration(migration_path: MigrationPath) -> None: #migration
    pass

def update_animal_details(animal_id: int, **kwargs: Any) -> None: #animal_manager
    pass

def update_habitat_details(habitat_id: int, **kwargs: dict[str, Any]) -> None: #habitat_manager
    pass

def update_migration_details(migration_id: int, **kwargs: Any) -> None: #migration_manager
    pass

def update_migration_path_details(path_id: int, **kwargs) -> None: #migration_manager
    pass
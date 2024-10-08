from typing import Optional, Any

from wildlife_tracker.migration_manager.migration_path import MigrationPath
from wildlife_tracker.migration_manager.migration import Migration
from wildlife_tracker.habitat_managment.animal import Habitat

class MigrationManager:
    
    def __inti__(self) -> None:
        migrations: dict[int, Migration] = {}
        paths: dict[int, MigrationPath] = {}

    def cancel_migration(migration_id: int) -> None:
        pass

    def get_migration_by_id(migration_id: int) -> Migration: 
        pass

    def get_migration_details(migration_id: int) -> dict[str, Any]: 
        pass

    def get_migration_path_by_id(path_id: int) -> MigrationPath: 
        pass

    def get_migration_paths() -> list[MigrationPath]: 
        pass

    def get_migration_paths_by_destination(destination: Habitat) -> list[MigrationPath]: 
        pass

    def get_migration_paths_by_species(species: str) -> list[MigrationPath]: 
        pass

    def get_migration_paths_by_start_location(start_location: Habitat) -> list[MigrationPath]: 
        pass

    def get_migrations() -> list[Migration]:
        pass

    def get_migrations_by_current_location(current_location: str) -> list[Migration]:
        pass

    def get_migrations_by_migration_path(migration_path_id: int) -> list[Migration]: 
        pass

    def get_migrations_by_start_date(start_date: str) -> list[Migration]:
        pass

    def get_migrations_by_status(status: str) -> list[Migration]:
        pass

    def get_migration_path_details(path_id) -> dict: 
        pass

    def remove_migration_path(path_id: int) -> None: 
        pass

    def update_migration_details(migration_id: int, **kwargs: Any) -> None: 
        pass

    def update_migration_path_details(path_id: int, **kwargs) -> None: 
        pass
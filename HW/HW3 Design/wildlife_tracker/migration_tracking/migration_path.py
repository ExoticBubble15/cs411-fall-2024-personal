from typing import Optional

class MigrationPath:

    destination: Habitat
    duration: Optional[int] = None
    path_id: int
    start_location: Habitat
    species: str 

    def create_migration_path(species: str, start_location: Habitat, destination: Habitat, duration: Optional[int] = None) -> None:
        pass
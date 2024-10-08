from typing import Optional

from wildlife_tracker.habitat_managment.animal import Habitat

class MigrationPath:

    def __init__(self,
                destination: Habitat,
                path_id: int,
                start_location: Habitat,
                species: str,
                duration: Optional[int] = None) -> None:
        self.destination = destination
        self.path_id = path_id
        self.start_location = start_location
        self.species = species
        self.duration = duration

    def create_migration_path(species: str, start_location: Habitat, destination: Habitat, duration: Optional[int] = None) -> None:
        pass
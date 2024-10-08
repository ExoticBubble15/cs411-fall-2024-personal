from typing import Any

from wildlife_tracker.migration_tracking.migration_path import MigrationPath

class Migration:

    def __init__(self,
                current_date: str,
                current_location: str,
                migration_id: int,
                migration_path: MigrationPath,
                start_date: str,
                status: str = "Scheduled") -> None:
        self.current_date = current_date
        self.current_location = current_location
        self.migration_id = migration_id
        self.migration_path = migration_path
        self.start_date = start_date
        self.status = status

    def schedule_migration(self, migration_path: MigrationPath) -> None: 
        pass
    
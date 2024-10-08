from typing import Any

class Migration:

    current_date: str
    current_location: str
    migration_id: int
    migration_path: MigrationPath
    start_date: str
    status: str = "Scheduled"

    def schedule_migration(migration_path: MigrationPath) -> None: 
        pass
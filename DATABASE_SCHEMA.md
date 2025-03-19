# F1-Database Schema Documentation

This document outlines the database schema used in the F1-Database application.

## Database Overview

The F1-Database application uses Firebase Firestore as its database. Firestore is a NoSQL document database that stores data in collections of documents.

## Collections

### Teams Collection

The `teams` collection stores information about Formula 1 teams.

**Document Fields:**
- `name` (String): The name of the team
- `year_founded` (Number): The year the team was founded
- `total_pole_positions` (Number): Total number of pole positions achieved
- `total_race_wins` (Number): Total number of race wins
- `total_constructor_titles` (Number): Total number of constructor championships won
- `finishing_position_previous_season` (Number): Position in the previous season's constructor standings

**Example Document:**
```json
{
  "name": "Ferrari",
  "year_founded": 1950,
  "total_pole_positions": 242,
  "total_race_wins": 243,
  "total_constructor_titles": 16,
  "finishing_position_previous_season": 3
}
```

### Drivers Collection

The `drivers` collection stores information about Formula 1 drivers.

**Document Fields:**
- `name` (String): The name of the driver
- `age` (Number): The driver's age
- `team` (String): The name of the team the driver currently races for
- `total_pole_positions` (Number): Total number of pole positions achieved
- `total_race_wins` (Number): Total number of race wins
- `total_points_scored` (Number): Total career points scored
- `total_world_titles` (Number): Total number of World Championships won
- `total_fastest_laps` (Number): Total number of fastest laps achieved

**Example Document:**
```json
{
  "name": "Lewis Hamilton",
  "age": 39,
  "team": "Mercedes",
  "total_pole_positions": 104,
  "total_race_wins": 103,
  "total_points_scored": 4639.5,
  "total_world_titles": 7,
  "total_fastest_laps": 64
}
```

## Relationships

- **Drivers to Teams**: Drivers reference their team by the team's name (the `team` field in the driver document corresponds to the `name` field in the team document).

## Future Schema Extensions

### Races Collection (Planned)

A future extension will include a `races` collection to store information about individual races.

**Proposed Document Fields:**
- `name` (String): The name of the race (e.g., "Monaco Grand Prix")
- `circuit` (String): The name of the circuit
- `date` (Timestamp): The date of the race
- `results` (Array): An array of objects containing race results including:
  - `driver` (String): Driver name
  - `position` (Number): Finishing position
  - `points` (Number): Points scored
  - `fastest_lap` (Boolean): Whether the driver set the fastest lap

### Seasons Collection (Planned)

A future extension will include a `seasons` collection to track statistics by season.

**Proposed Document Fields:**
- `year` (Number): The season year
- `driver_champion` (String): The name of the drivers' champion
- `team_champion` (String): The name of the constructors' champion
- `total_races` (Number): Total number of races in the season 
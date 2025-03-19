from fastapi import HTTPException, status

def validate_driver_exists(drivers_ref, driver_id):
    """
    Validate that a driver with the given ID exists in the database
    
    Args:
        drivers_ref: Reference to the drivers collection
        driver_id: ID of the driver to check
        
    Returns:
        Tuple containing the driver document reference and the driver data
        
    Raises:
        HTTPException: If the driver does not exist
    """
    driver_doc_ref = drivers_ref.document(driver_id)
    driver_doc = driver_doc_ref.get()
    
    if not driver_doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with ID {driver_id} not found"
        )
    
    return driver_doc_ref, driver_doc.to_dict()

def validate_team_exists(teams_ref, team_id):
    """
    Validate that a team with the given ID exists in the database
    
    Args:
        teams_ref: Reference to the teams collection
        team_id: ID of the team to check
        
    Returns:
        Tuple containing the team document reference and the team data
        
    Raises:
        HTTPException: If the team does not exist
    """
    team_doc_ref = teams_ref.document(team_id)
    team_doc = team_doc_ref.get()
    
    if not team_doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found"
        )
    
    return team_doc_ref, team_doc.to_dict()

def validate_team_name_exists(teams_ref, team_name):
    """
    Validate that a team with the given name exists in the database
    
    Args:
        teams_ref: Reference to the teams collection
        team_name: Name of the team to check
        
    Returns:
        True if the team exists, False otherwise
    """
    team_query = teams_ref.where("name", "==", team_name).limit(1).get()
    return len(team_query) > 0

def validate_unique_driver_name(drivers_ref, name, exclude_id=None):
    """
    Validate that no other driver exists with the given name
    
    Args:
        drivers_ref: Reference to the drivers collection
        name: Driver name to check for uniqueness
        exclude_id: Optional ID to exclude from the check (for updates)
        
    Raises:
        HTTPException: If another driver with the same name exists
    """
    query = drivers_ref.where("name", "==", name).get()
    
    for doc in query:
        # If we're excluding an ID (for updates) and this is that document, skip it
        if exclude_id and doc.id == exclude_id:
            continue
            
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Driver with name '{name}' already exists"
        )

def validate_unique_team_name(teams_ref, name, exclude_id=None):
    """
    Validate that no other team exists with the given name
    
    Args:
        teams_ref: Reference to the teams collection
        name: Team name to check for uniqueness
        exclude_id: Optional ID to exclude from the check (for updates)
        
    Raises:
        HTTPException: If another team with the same name exists
    """
    query = teams_ref.where("name", "==", name).get()
    
    for doc in query:
        # If we're excluding an ID (for updates) and this is that document, skip it
        if exclude_id and doc.id == exclude_id:
            continue
            
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team with name '{name}' already exists"
        ) 
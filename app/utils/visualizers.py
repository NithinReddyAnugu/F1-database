"""
Visualization utilities for the F1-Database application.
"""
import matplotlib.pyplot as plt
import io
import base64

def create_driver_points_chart(driver_name, races):
    """
    Create a line chart showing a driver's points progression over races
    
    Args:
        driver_name (str): The name of the driver
        races (list): List of race dictionaries containing results
        
    Returns:
        str: Base64 encoded image of the chart
    """
    # Sort races by date
    sorted_races = sorted(races, key=lambda x: x.get('date', ''))
    
    # Extract race names and points for the driver
    race_names = []
    points = []
    cumulative_points = 0
    
    for race in sorted_races:
        race_names.append(race.get('name', ''))
        
        # Find the driver's result for this race
        driver_result = None
        for result in race.get('results', []):
            if result.get('driver') == driver_name:
                driver_result = result
                break
        
        # Add points if the driver participated in this race
        if driver_result:
            race_points = driver_result.get('points', 0)
            cumulative_points += race_points
        
        points.append(cumulative_points)
    
    # Create the chart
    plt.figure(figsize=(10, 6))
    plt.plot(race_names, points, marker='o', linestyle='-', linewidth=2)
    plt.title(f"{driver_name}'s Points Progression")
    plt.xlabel('Races')
    plt.ylabel('Cumulative Points')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    
    # Convert plot to base64 encoded image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def create_team_comparison_chart(teams_data):
    """
    Create a bar chart comparing teams based on specified metrics
    
    Args:
        teams_data (list): List of team dictionaries with statistics
        
    Returns:
        str: Base64 encoded image of the chart
    """
    team_names = [team.get('name', '') for team in teams_data]
    wins = [team.get('total_race_wins', 0) for team in teams_data]
    
    # Create the chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(team_names, wins)
    
    # Add labels and styling
    plt.title('Total Race Wins by Team')
    plt.xlabel('Team')
    plt.ylabel('Total Race Wins')
    plt.xticks(rotation=45)
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height:.0f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.grid(axis='y')
    
    # Convert plot to base64 encoded image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def create_race_results_chart(race_data):
    """
    Create a horizontal bar chart showing race results
    
    Args:
        race_data (dict): Dictionary containing race information and results
        
    Returns:
        str: Base64 encoded image of the chart
    """
    results = race_data.get('results', [])
    
    # Sort results by position
    sorted_results = sorted(results, key=lambda x: x.get('position', 0))
    
    drivers = [result.get('driver', '') for result in sorted_results]
    points = [result.get('points', 0) for result in sorted_results]
    
    # Create colors list (highlight fastest lap)
    colors = ['#1E88E5' if not result.get('fastest_lap', False) else '#D81B60' 
              for result in sorted_results]
    
    # Create the chart
    plt.figure(figsize=(10, 6))
    bars = plt.barh(drivers, points, color=colors)
    
    # Add labels and styling
    plt.title(f"{race_data.get('name', 'Race')} Results")
    plt.xlabel('Points')
    plt.ylabel('Driver')
    plt.xlim(0, max(points) * 1.1)  # Add some padding to the right
    
    # Add value labels inside each bar
    for bar in bars:
        width = bar.get_width()
        plt.text(width - 0.5, bar.get_y() + bar.get_height()/2.,
                 f'{width:.0f}', ha='right', va='center', color='white', fontweight='bold')
    
    # Add legend for fastest lap
    plt.legend(['Regular Points', 'Fastest Lap'])
    
    plt.tight_layout()
    plt.grid(axis='x')
    
    # Convert plot to base64 encoded image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.getvalue()).decode('utf-8') 
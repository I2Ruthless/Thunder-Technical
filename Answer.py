from datetime import datetime

def find_qualified_games(game_data: list[dict], true_shooting_cutoff: int, player_count: int) -> list[int]:
    qualified_games = {}
    
    for game in game_data:
        game_id = game['gameID']
        # Calculate points scored
        points = (2 * game['fieldGoal2Made'] +
                  3 * game['fieldGoal3Made'] +
                  game['freeThrowMade'])
        
        # Calculate total shot attempts
        total_shots_attempted = (game['fieldGoal2Attempted'] + 
                                 game['fieldGoal3Attempted'] + 
                                 0.44 * game['freeThrowAttempted'])
        
        # Compute True Shooting percentage
        if total_shots_attempted == 0:
            ts_percentage = 0
        else:
            ts_percentage = points / (2 * total_shots_attempted) * 100
        
        # Check if player's TS% meets or exceeds the cutoff
        if ts_percentage >= true_shooting_cutoff:
            if game_id not in qualified_games:
                qualified_games[game_id] = {'count': 0, 'gameDate': game['gameDate']}
            qualified_games[game_id]['count'] += 1
    
    # Filter games that have at least `player_count` players who met the cutoff
    valid_games = [
        (game_id, data['gameDate']) for game_id, data in qualified_games.items()
        if data['count'] >= player_count
    ]
    
    # Sort by game date from most recent to least recent
    valid_games.sort(key=lambda x: datetime.strptime(x[1], '%m/%d/%Y'), reverse=True) 
    
    # Return the list of gameIDs, sorted by date
    return [game_id for game_id, _ in valid_games]

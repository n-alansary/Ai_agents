from typing import List, Dict, Any, Union, Optional


def get_player_profile(name: str) -> str:
    '''Retrieves the full profile, stats, and match history for a specific player.
    Useful when the user asks about a specific person.'''
    player_cursor = collection1.find({'name': {'$regex': f'^{re.escape(name)}$', '$options': 'i'}})
    output = []
    for res in player_cursor:
        del res['_id']
        output.append(res)
    return json.dumps(output, default=str) if output else 'No player with that name is found in the database'

def search_for_attributes_in_players(
    country: str = None,
    gender: str = None,
    racket_sponsor: str = None,
    status: str = None,
    plays: str = None
) -> str:
    '''
    Searches for players matching specific criteria.
    All arguments are optional.
    '''
    query = {}
    if country is not None:
        query['country'] = {'$regex': f'^{re.escape(country)}$', '$options': 'i'}
    if racket_sponsor is not None:
        query['racket_sponsor'] = {'$regex': f'^{re.escape(racket_sponsor)}$', '$options': 'i'}
    if gender is not None:
        query['gender'] = {'$regex': f'^{re.escape(gender)}$', '$options': 'i'}
    if status is not None:
        query['status'] = {'$regex': f'^{re.escape(status)}$', '$options': 'i'}
    if plays is not None:
        query['plays'] = {'$regex': f'^{re.escape(plays)}$', '$options': 'i'}

    projection = {
        "_id": 0,
        "name": 1,
        "current_rank": 1,
        "country": 1,
        "gender": 1,
        "racket_sponsor": 1,
        "status": 1,
        "plays": 1
    }
    response = list(collection1.find(query, projection))
    return json.dumps(response , default=str) if response else 'No player with the criteria was found in the database'

def sort_players_list(
    sort_by: str,
    order: int = 1,
    country: Optional[str] = None,
    gender:  Optional[str] = None, 
) -> str:
    """
    Retrieves players from the database and returns them sorted by a given field.
    Args:
        sort_by: The field to sort by (e.g., "current_rank", "stats.matches_won", "stats.career_titles").
        order: 1 for Ascending, -1 for Descending. Default is 1 (Ascending).
        country: Optional filter by country.
        gender: Optional filter by gender.
    """
    query = {}
    if country is not None:
        query["country"] =  {'$regex': f'^{re.escape(country)}$', '$options': 'i'}
    if gender is not None:
        query["gender"] = {'$regex': f'^{re.escape(gender)}$', '$options': 'i'}
    projection = {"_id": 0, "name": 1, "current_rank": 1, "country": 1, "gender": 1}
    # Also project the sort field if it's nested (like stats.matches_won)
    if sort_by and sort_by not in projection:
        projection[sort_by.split(".")[0]] = 1
    cursor = collection1.find(query, projection).sort(sort_by, order)
    results = list(cursor)
    return json.dumps(results, default=str) if results else "No players found matching the criteria."

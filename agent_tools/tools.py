from typing import List, Dict, Any, Union, Optional
from langchain_core.runnables import RunnableConfig
import json 
import re
from enum import StrEnum


class RacketSponsorEnum(StrEnum):
    DUNLOP = "Dunlop"
    TECNIFIBRE = "Tecnifibre"
    HEAD = "Head"
    UNSQUASHABLE = "Unsquashable"
    VICTOR = "Victor"
    PRINCE = "Prince"

def get_player_profile(config: RunnableConfig ,name: str ) -> str:
    '''Retrieves the full profile, stats, and match history for a specific player.
    Useful when the user asks about a specific person.'''

    collection = config["configurable"]["collection"]

    player_cursor = collection.find({'name': {'$regex': f'^{re.escape(name)}$', '$options': 'i'}})
    output = []
    for res in player_cursor:
        del res['_id']
        output.append(res)
    return json.dumps(output, default=str) if output else 'No player with that name is found in the database'

def search_for_attributes_in_players(
    config: RunnableConfig,
    country: str = None,
    gender: str = None,
    racket_sponsor: RacketSponsorEnum = None,
    status: str = None,
    plays: str = None
) -> str:
    '''
    Searches for players matching specific criteria.
    All arguments are optional.
    '''

    collection = config["configurable"]["collection"]


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
    response = list(collection.find(query, projection))
    return json.dumps(response , default=str) if response else 'No player with the criteria was found in the database'

def sort_players_list(
    config: RunnableConfig,
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

    collection = config["configurable"]["collection"]


    query = {}
    if country is not None:
        query["country"] =  {'$regex': f'^{re.escape(country)}$', '$options': 'i'}
    if gender is not None:
        query["gender"] = {'$regex': f'^{re.escape(gender)}$', '$options': 'i'}
    projection = {"_id": 0, "name": 1, "current_rank": 1, "country": 1, "gender": 1}
    # Also project the sort field if it's nested (like stats.matches_won)
    if sort_by and sort_by not in projection:
        projection[sort_by.split(".")[0]] = 1
    cursor = collection.find(query, projection).sort(sort_by, order)
    results = list(cursor)
    return json.dumps(results, default=str) if results else "No players found matching the criteria."


'--------------------------------------------------------------------------------'


def execute_mongo_query(
    config: RunnableConfig,
    query: Dict[str, Any],
    projection: Optional[Dict[str, Any]] = None,
    sort: Optional[List[List]] = None,
    limit: int = 0
) -> str:
    """
    Executes a MongoDB find query on the squash players collection and returns the results.

    Args:
        query: A MongoDB query filter dictionary (e.g. {"country": "Egypt"} or {"stats.matches_won": {"$gt": 100}}).
        projection: Optional projection dictionary to include/exclude fields (e.g. {"_id": 0, "name": 1}).
                    If not provided, all fields except _id are returned.
        sort: Optional list of [field, direction] pairs for sorting (e.g. [["current_rank", 1]]).
              Direction: 1 for ascending, -1 for descending.
        limit: Maximum number of documents to return. 0 means no limit.
    """
    collection = config["configurable"]["collection"]

    if projection is None:
        projection = {"_id": 0}

    cursor = collection.find(query, projection)

    if sort:
        cursor = cursor.sort(sort)

    if limit > 0:
        cursor = cursor.limit(limit)

    results = list(cursor)
    return json.dumps(results, default=str) if results else "No results found for the given query."


'--------------------------------------------------------------------------------'


def execute_mongo_crud(
    config: RunnableConfig,
    operation: str,
    filter: Optional[Dict[str, Any]] = None,
    data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
    projection: Optional[Dict[str, Any]] = None,
    sort: Optional[List[List]] = None,
    limit: int = 0,
    pipeline: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Executes any MongoDB CRUD operation on the squash players collection.

    Args:
        operation: The operation to perform. Must be one of:
            - "find" : Read documents matching a filter.
            - "insert_one" : Insert a single document (provide it in `data`).
            - "insert_many" : Insert multiple documents (provide a list in `data`).
            - "update_one" : Update the first document matching `filter` with the update expression in `data`.
            - "update_many" : Update all documents matching `filter` with the update expression in `data`.
            - "delete_one" : Delete the first document matching `filter`.
            - "delete_many" : Delete all documents matching `filter`.
            - "count_documents" : Count documents matching `filter`.
            - "aggregate" : Run an aggregation pipeline (provide the pipeline list in `pipeline`).
        filter: A MongoDB filter dictionary for find/update/delete/count operations (e.g. {"country": "Egypt"}).
        data: The document(s) or update expression, depending on the operation:
            - For insert_one: a single document dict (e.g. {"name": "John", "country": "UK"}).
            - For insert_many: a list of document dicts.
            - For update_one/update_many: an update expression (e.g. {"$set": {"status": "Retired"}}).
        projection: Optional fields to include/exclude for find operations (e.g. {"_id": 0, "name": 1}).
        sort: Optional list of [field, direction] pairs for find operations (e.g. [["current_rank", 1]]).
        limit: Maximum number of documents to return for find operations. 0 means no limit.
        pipeline: An aggregation pipeline list for the "aggregate" operation
                  (e.g. [{"$group": {"_id": "$country", "count": {"$sum": 1}}}]).
    """
    collection = config["configurable"]["collection"]
    operation = operation.lower().strip()

    try:
        # --- READ ---
        if operation == "find":
            if filter is None:
                filter = {}
            if projection is None:
                projection = {"_id": 0}
            cursor = collection.find(filter, projection)
            if sort:
                cursor = cursor.sort(sort)
            if limit > 0:
                cursor = cursor.limit(limit)
            results = list(cursor)
            return json.dumps(results, default=str) if results else "No documents found."

        # --- CREATE ---
        elif operation == "insert_one":
            if data is None:
                return "Error: 'data' is required for insert_one. Provide a document dict."
            result = collection.insert_one(data)
            return json.dumps({"inserted_id": str(result.inserted_id)})

        elif operation == "insert_many":
            if data is None or not isinstance(data, list):
                return "Error: 'data' must be a list of documents for insert_many."
            result = collection.insert_many(data)
            return json.dumps({"inserted_ids": [str(id) for id in result.inserted_ids]})

        # --- UPDATE ---
        elif operation == "update_one":
            if filter is None or data is None:
                return "Error: both 'filter' and 'data' (update expression) are required for update_one."
            result = collection.update_one(filter, data)
            return json.dumps({"matched_count": result.matched_count, "modified_count": result.modified_count})

        elif operation == "update_many":
            if filter is None or data is None:
                return "Error: both 'filter' and 'data' (update expression) are required for update_many."
            result = collection.update_many(filter, data)
            return json.dumps({"matched_count": result.matched_count, "modified_count": result.modified_count})

        # --- DELETE ---
        elif operation == "delete_one":
            if filter is None:
                return "Error: 'filter' is required for delete_one."
            result = collection.delete_one(filter)
            return json.dumps({"deleted_count": result.deleted_count})

        elif operation == "delete_many":
            if filter is None:
                return "Error: 'filter' is required for delete_many."
            result = collection.delete_many(filter)
            return json.dumps({"deleted_count": result.deleted_count})

        # --- COUNT ---
        elif operation == "count_documents":
            if filter is None:
                filter = {}
            count = collection.count_documents(filter)
            return json.dumps({"count": count})

        # --- AGGREGATE ---
        elif operation == "aggregate":
            if pipeline is None or not isinstance(pipeline, list):
                return "Error: 'pipeline' must be a list of aggregation stages for aggregate."
            results = list(collection.aggregate(pipeline))
            for doc in results:
                if "_id" in doc:
                    doc["_id"] = str(doc["_id"])
            return json.dumps(results, default=str) if results else "Aggregation returned no results."

        else:
            return f"Error: Unknown operation '{operation}'. Supported: find, insert_one, insert_many, update_one, update_many, delete_one, delete_many, count_documents, aggregate."

    except Exception as e:
        return f"Error executing '{operation}': {str(e)}"

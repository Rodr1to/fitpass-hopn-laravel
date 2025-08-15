import pandas as pd
from geopy.distance import geodesic
from typing import List, Dict, Any

def find_anomalies(checkin_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    detects anomalous check-ins from a list of user check-in data.

    an anomaly is defined as two check-ins by the same user that are more than
    50km apart but less than 1 hour apart in time.

    Args:
        checkin_data: list of dictionaries, each representing a check-in.
                      Expected keys: 'user_id', 'timestamp', 'latitude', 'longitude'.

    Returns:
        list of dictionaries, each representing a detected anomaly.
    """
    if not checkin_data:
        return []

    # pandas df for efficient processing
    df = pd.DataFrame(checkin_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by=['user_id', 'timestamp'], inplace=True)

    anomalies = []

    # group by user and iterate through their check-ins
    for user_id, group in df.groupby('user_id'):
        # shift the data to compare each row with the previous one
        previous_group = group.shift(1)
        
        # calculate time difference in hours
        time_diff = (group['timestamp'] - previous_group['timestamp']).dt.total_seconds() / 3600
        
        # calculate distance using a lambda function for geodesic distance
        dist_km = [
            geodesic(
                (prev_lat, prev_lon), (curr_lat, curr_lon)
            ).km if pd.notna(prev_lat) else 0
            for prev_lat, prev_lon, curr_lat, curr_lon in zip(
                previous_group['latitude'], previous_group['longitude'],
                group['latitude'], group['longitude']
            )
        ]
        
        # find rows that meet the anomaly criteria
        anomalous_rows = group[(pd.Series(dist_km) > 50) & (time_diff < 1)]
        
        if not anomalous_rows.empty:
            for index, row in anomalous_rows.iterrows():
                previous_row = previous_group.loc[index]
                anomalies.append({
                    "user_id": int(user_id),
                    "previous_checkin_time": previous_row['timestamp'].isoformat(),
                    "anomalous_checkin_time": row['timestamp'].isoformat(),
                    "distance_km": round(dist_km[group.index.get_loc(index)], 2)
                })

    return anomalies
import os
import io
import pandas as pd
from dotenv import load_dotenv
from connection import get_connection

load_dotenv()


# PostgreSQL connection parameters
dbname = os.getenv('dbname')
user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')

cursor = get_connection(dbname,user,password,host,port)

cursor.execute('SELECT * FROM recognition_results LIMIT 50000')

results = cursor.fetchall()

# Get column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame from the fetched data
df = pd.DataFrame(results, columns=column_names)

# Print the DataFrame
print(df)

cursor.close()

# Example: Convert 'inserted_at' and 'updated_at' to datetime
df['inserted_at'] = pd.to_datetime(df['inserted_at'])
df['updated_at'] = pd.to_datetime(df['updated_at'])


def find_matches(dataframe, confidence_threshold=0.05, time_window=180):
    # Filter results with confidence above the threshold
    high_confidence_df = dataframe[dataframe['input_confidence'] >= confidence_threshold]

    # Sort by recognition log id and offset_seconds
    high_confidence_df = high_confidence_df.sort_values(by=['recognition_log_id', 'offset_seconds'])

    # Group by recognition log id and find matches within the time window
    potential_matches = []

    for recognition_log_id, group in high_confidence_df.groupby('recognition_log_id'):
        start_time = None
        end_time = None
        match = []

        for _, row in group.iterrows():
            if start_time is None:
                start_time = row['offset_seconds']
                end_time = start_time + time_window
                match.append(row)
            elif row['offset_seconds'] <= end_time:
                match.append(row)
                end_time = max(end_time, row['offset_seconds'] + time_window)
            else:
                potential_matches.append(match)
                match = [row]
                start_time = row['offset_seconds']
                end_time = start_time + time_window
        
        if match:
            potential_matches.append(match)

    return potential_matches

# Find potential matches
matches = find_matches(df)


# Print matches for inspection
for match in matches:
    print("Match found: "*5)
    match_df = pd.DataFrame(match)
    print(match_df)
    print("\n")


# Optionally, save results to a CSV file
for i, match in enumerate(matches):
    match_df = pd.DataFrame(match)
    match_df.to_csv(f'match_{i}.csv', index=False)

























# # Merge entries within 3 minutes interval
# merged_entries = []
# current_group = []
# interval_seconds = 3 * 60  # 3 minutes in seconds

# for idx, row in matches.iterrows():
#     if not current_group:
#         current_group.append(row)
#     else:
#         last_entry_time = current_group[-1]['inserted_at']
#         if (row['inserted_at'] - last_entry_time).total_seconds() <= interval_seconds:
#             current_group.append(row)
#         else:
#             merged_entries.append(current_group)
#             current_group = [row]

# # Add the last group if it's not empty
# if current_group:
#     merged_entries.append(current_group)

# # Create a new DataFrame for merged entries
# merged_data = []
# for group in merged_entries:
#     if group:
#         merged_data.append({
#             'id': group[0]['id'],
#             'file_sha1': group[0]['file_sha1'],
#             'fingerprinted_confidence': max(g['fingerprinted_confidence'] for g in group),
#             'fingerprinted_hashes_in_db': sum(g['fingerprinted_hashes_in_db'] for g in group),
#             'hashes_matched_in_input': sum(g['hashes_matched_in_input'] for g in group),
#             'input_confidence': max(g['input_confidence'] for g in group),
#             'input_total_hashes': sum(g['input_total_hashes'] for g in group),
#             'offset': group[0]['offset'],
#             'offset_seconds': group[0]['offset_seconds'],
#             'song_id': group[0]['song_id'],
#             'song_name': group[0]['song_name'],
#             'recognition_log_id': group[0]['recognition_log_id'],
#             'inserted_at': group[0]['inserted_at'],
#             'updated_at': group[0]['updated_at']
#         })

# merged_df = pd.DataFrame(merged_data)
# merged_df.to_csv('merged_df.csv')

# # Print merged DataFrame
# print(merged_df['song_name'])
import pandas as pd
import json
import re
from datetime import datetime

# Load CSV
df = pd.read_csv('/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/SP_-_Worker_and_Temporary_Worker_Web_Register_-_2026-07-17.csv')

# Filter for A-rated Skilled Worker sponsors only
a_rated = df[
    (df['Type & Rating'].str.contains('A rating', na=False)) & 
    (df['Route'] == 'Skilled Worker')
].copy()

print(f"A-rated Skilled Worker sponsors: {len(a_rated)}")

# Keywords to search for (case-insensitive)
keywords = [
    'robot', 'robotics', 'autonomous', 'ai', 'artificial intelligence', 'machine learning',
    'ml ', 'deep learning', 'neural', 'simulation', 'physics', 'mujoco', 'isaac',
    'computer vision', 'cv ', 'nlp', 'llm', 'generative', 'world model',
    'embodied', 'manipulation', 'grasping', 'locomotion', 'humanoid',
    'drone', 'uav', 'aerial', 'vehicle', 'automotive', 'self-driving',
    'reinforcement learning', 'rl ', 'imitation learning', 'diffusion',
    'sim2real', 'sim-to-real', 'digital twin', 'physics engine',
    'cogvideo', 'video generation', 'adversarial', 'verification',
    'benchmark', 'evaluation', 'safety', 'alignment', 'research',
    'applied ai', 'applied research', 'foundation model', 'multimodal',
    'spatial', '3d', 'perception', 'planning', 'control', 'dynamics'
]

# Compile regex patterns
patterns = [re.compile(rf'\b{re.escape(kw)}\b', re.IGNORECASE) for kw in keywords]

def find_matches(name):
    matches = []
    for kw, pattern in zip(keywords, patterns):
        if pattern.search(name):
            matches.append(kw)
    return matches

# Apply keyword matching
a_rated['matched_keywords'] = a_rated['Organisation Name'].apply(find_matches)
matched = a_rated[a_rated['matched_keywords'].apply(len) > 0].copy()

print(f"Companies with keyword matches: {len(matched)}")

# Sort by number of matches (descending) then by name
matched['match_count'] = matched['matched_keywords'].apply(len)
matched = matched.sort_values(['match_count', 'Organisation Name'], ascending=[False, True])

# Display top matches
for _, row in matched.head(50).iterrows():
    print(f"  {row['Organisation Name']} | {row['Town/City']}, {row['County']} | {row['matched_keywords']}")

# Save full results
output = {
    'updated': datetime.now().isoformat(),
    'total_a_rated_skilled': len(a_rated),
    'total_matched': len(matched),
    'companies': matched[['Organisation Name', 'Town/City', 'County', 'Type & Rating', 'Route', 'matched_keywords']].to_dict('records')
}

with open('/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/csv_discovered_sponsors.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nSaved to csv_discovered_sponsors.json")
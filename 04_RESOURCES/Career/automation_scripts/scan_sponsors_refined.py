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

# More specific keywords - avoid false positives
# Using word boundaries and excluding common false positive contexts
primary_keywords = [
    r'\brobot(ics)?\b', r'\bautonomous\b', r'\bembodied\b', r'\bhumanoid\b',
    r'\bmanipulation\b', r'\bgrasping\b', r'\blocomotion\b',
    r'\bmujoco\b', r'\bisaac\s*(sim|gym|lab)?\b', r'\bphysics\s*(engine|simulation)?\b',
    r'\bsim2real\b', r'\bsim.to.real\b', r'\bdigital\s*twin\b',
    r'\bworld\s*model\b', r'\bcogvideo\b', r'\bvideo\s*generation\b',
    r'\breinforcement\s*learning\b', r'\brl\b', r'\bimitation\s*learning\b',
    r'\badversarial\b', r'\bverification\b', r'\bstress\s*test',
    r'\bcomputer\s*vision\b', r'\bperception\b', r'\bplanning\b', r'\bcontrol\b',
    r'\bapplied\s*(ai|research)\b', r'\bfoundation\s*model\b', r'\bmultimodal\b',
    r'\bspatial\s*(intelligence|computing)\b', r'\b3d\s*(vision|perception|reconstruction)\b',
    r'\bjax\b', r'\bflax\b', r'\brax\b', r'\brobosuite\b', r'\bisaac\s*gym\b',
    r'\bshadow\s*robot\b', r'\bprosthetic\b', r'\bexoskeleton\b',
    r'\bdrone\b', r'\buav\b', r'\baerial\s*robot', r'\bself.driving\b',
    r'\bautonomous\s*vehicle\b', r'\bsimulation\b', r'\bphysics\b'
]

secondary_keywords = [
    r'\bai\b', r'\bml\b', r'\bmachine\s*learning\b', r'\bdeep\s*learning\b',
    r'\bneural\b', r'\bllm\b', r'\bgenerative\b', r'\bdiffusion\b',
    r'\bresearch\b', r'\bbenchmark\b', r'\bevaluation\b', r'\bsafety\b',
    r'\balignment\b', r'\b3d\b', r'\bdynamics\b'
]

# Compile patterns
primary_patterns = [re.compile(kw, re.IGNORECASE) for kw in primary_keywords]
secondary_patterns = [re.compile(kw, re.IGNORECASE) for kw in secondary_keywords]

def find_matches(name):
    primary_matches = []
    secondary_matches = []
    for kw, pattern in zip(primary_keywords, primary_patterns):
        if pattern.search(name):
            primary_matches.append(kw)
    for kw, pattern in zip(secondary_keywords, secondary_patterns):
        if pattern.search(name):
            secondary_matches.append(kw)
    return primary_matches, secondary_matches

# Apply keyword matching
a_rated[['primary_matches', 'secondary_matches']] = a_rated['Organisation Name'].apply(
    lambda x: pd.Series(find_matches(x))
)
a_rated['primary_count'] = a_rated['primary_matches'].apply(len)
a_rated['secondary_count'] = a_rated['secondary_matches'].apply(len)
a_rated['total_score'] = a_rated['primary_count'] * 3 + a_rated['secondary_count']

# Filter: at least 1 primary match, OR 2+ secondary matches
matched = a_rated[
    (a_rated['primary_count'] > 0) | (a_rated['secondary_count'] >= 2)
].copy()

print(f"Companies with refined keyword matches: {len(matched)}")

# Sort by score
matched = matched.sort_values(['total_score', 'primary_count', 'Organisation Name'], ascending=[False, False, True])

# Display top matches
for _, row in matched.head(80).iterrows():
    all_matches = row['primary_matches'] + row['secondary_matches']
    print(f"  {row['Organisation Name']} | {row['Town/City']}, {str(row['County'])[:20]} | Score: {row['total_score']} | {all_matches}")

# Save full results
output = {
    'updated': datetime.now().isoformat(),
    'total_a_rated_skilled': len(a_rated),
    'total_matched': len(matched),
    'companies': matched[['Organisation Name', 'Town/City', 'County', 'Type & Rating', 'Route', 'primary_matches', 'secondary_matches', 'total_score']].to_dict('records')
}

with open('/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/csv_discovered_sponsors_refined.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nSaved to csv_discovered_sponsors_refined.json")
import json
import pandas as pd
import sys
from ast import literal_eval

df = pd.read_csv('Fake_data.csv')

with open("sample.json", "r") as read:
     data = json.load(read)

uuid = data['User Id']
module = data['Module']
sub_module = data['Sub Module']
actions = data['Actions']

ans = df.loc[(df['User Id'] == uuid)]

print(ans)
new_actions = ans['Actions'].tolist()
new_action = literal_eval(new_actions[0])

new_action.sort()
actions.sort()
    

# ans = df.loc[(df['User Id'] == uuid) & (df['Module'] == module) & (df['Sub Module'] == sub_module) & (df['Actions'] == f"{actions}")]
answer = ans.loc[(ans['Module'] == module) & (ans['Sub Module'] == sub_module) & (new_action == actions)]

if answer.empty:
    print("False")
else:
    print("True")

# print(answer)


import os
import json
import csv

input_file = './Data/json/data100.json'
output_file = 'out.json'

data_dir = './Data/json/'
fake_identities_file = './FakeNameGenerator/FakeIdentities.csv'
file_names = os.listdir(data_dir)

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_from_file = json.load(file)
    return json_from_file


all_json = read_json_file(input_file)


import csv

fnames = []
mnames = []
lnames = []
companies = []

with open(fake_identities_file, newline='') as csvfile:
    fake_id_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

    for row in fake_id_reader:
        fnames.append(row['GivenName'])
        mnames.append(row['MiddleInitial'])
        lnames.append(row['Surname'])
        companies.append(row['Company'])


# Obfuscate json

next_fname_idx = 0
taken_fnames = {}
next_lname_idx = 0
taken_lnames = {}
next_company_idx = 0
taken_companies = {}
taken_email_providers = {}
last_email_provider = 0
email_ids = []

last_user_name = 0

for entry in all_json:
    name = entry['Name'].split(' ')
    if len(name) != 3:
        print("Unexpected name length")
        
    new_name = ""
    
    if name[0] in taken_fnames:
        new_name = taken_fnames[name[0]]
    else:
        while(fnames[next_fname_idx] in list(taken_fnames.values())):
            print("taken", fnames[next_fname_idx])
            next_fname_idx += 1
        
        new_name = fnames[next_fname_idx]
        taken_fnames[name[0]] = fnames[next_fname_idx]
        next_fname_idx += 1
        
    new_name = new_name + " " + name[1] + " "
    
    
    if name[2] in taken_lnames:
        new_name += taken_lnames[name[2]]
    else:
        while(lnames[next_lname_idx] in list(taken_lnames.values())):
            next_lname_idx += 1
        
        new_name += lnames[next_lname_idx]
        taken_lnames[name[2]] = lnames[next_lname_idx]
        next_lname_idx += 1
        
    entry['Name'] = new_name
    
    entry['SSN'] = 'XXX-XX-XXXX'
    
    cur_phone = entry['Phone'].split('-')
    entry['Phone'] = cur_phone[0] + '-YYY-YYYY'
    
    cur_add = entry['Address'].split(' ')
    entry['Address'] = "nnnn " + cur_add[1] + " " + cur_add[2]
    
    
    name_parts = new_name.split(' ')
    email_company = entry['Email'].split("@")[1]
    email_company_split = email_company.split('.')
    email_company = '.'.join(email_company_split)
    
    if email_company in taken_email_providers:
        new_email_company = taken_email_providers[email_company]
    else:
        last_email_provider += 1
        taken_email_providers[email_company] = str(last_email_provider)
        new_email_company = str(last_email_provider)
    
    entry['Email'] = name_parts[0] + name_parts[1][:-1] + name_parts[2] + "@" + new_email_company + "." + email_company_split[-1]
    
    
    loc = entry['Location'].split(', ')
    lat = loc[0].split('.')[0]
    lng = loc[1].split('.')[0]
    entry['Location'] = lat + ", " + lng
    
    cur_company = entry['Company']
    if cur_company in taken_companies:
        new_company = taken_companies[cur_company]
    else:
        while(companies[next_company_idx] in list(taken_companies.values())):
            next_company_idx += 1
        
        new_company = companies[next_company_idx]
        taken_companies[cur_company] = companies[next_company_idx]
        next_company_idx += 1
        
    entry['Company'] = new_company
    
    entry['UserName'] = "a" + str(last_user_name) + str(last_user_name) + str(last_user_name)
    last_user_name += 1

    entry['WeightKG'] = entry['WeightKG'].split('.')[0]



with open(output_file, 'w') as outfile:
    json.dump(all_json, outfile)


print("Written file")

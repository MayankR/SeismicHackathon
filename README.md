# SeismicHackathon
Hackathon at Seismic office, after meeting at UCSD Career Fair

# Problem
Given JSON data containing a lot of user information, obfuscate as much user's personally identifiable information as possible

# Approach
- Downloaded several fake identities from an online generator mentioned in problem statement pdf file
- Wrote code while debugging in included python notebook file
- Finally ported code to .py file
- .py file has input and output file path variable in beginning
- identified IID fields manually in data beforehand while exploring data
- Iterate over all dataset records, obfuscating the user data present in them
- Write out a final output json file

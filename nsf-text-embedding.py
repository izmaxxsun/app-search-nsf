# from elasticsearch import Elasticsearch, helpers
import csv
import os
import json
from pathlib import Path
import random
from datetime import datetime, timedelta
from elastic_enterprise_search import AppSearch
from elasticsearch import Elasticsearch, helpers

base_path = Path(__file__).parent
file_path = (base_path / "arxiv-small.json").resolve()
INDEX_NAME = "nsf-proposals-with-random-dates"

def divide_chunks(l, n):
      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

# Sample Test Data
reviewer_names = ['John', 'Andrew', 'Dany', 'Chris', 'Nick', 'George', 'Louis Theran', 'Huan Yang']
directorates = ['BIO', 'CISE', 'EHR', 'ENG', 'ERE', 'GEO', 'OIA', 'OISE', 'MPS', 'SBE', 'TIP']
statuses = ['Decline', 'DDConcurred', 'Proposal Awarded', 'Full Proposal Invited', 'Full Proposal Not Invited', 'Discourage Submission of Full Proposal', 'Pending', 'Assigned to PM', 'Withdrawn', 'Other', 'Returned without Review']
divisions = ['DBI', 'DEB', 'EF', 'IOS', 'MCB', 'OAC', 'CCF', 'CNS', 'IIS', 'DGE', 'DRL', 'DUE', 'HRD']
institutions = ['Institution A', 'Institution B', 'Institution C', 'Institution D', 'Institution E', 'Institution F']
states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
announcements = ['NSF 18-550', 'NSF 22-1', 'NSF 22-502']
funding_programs = ['Information Technology', 'Not Applicable', 'EFRI Research Projects']
funding_program_codes = ['1640', '7633', '033Y', '132Y']
managing_programs = ['SBIR Phase 1', 'SBIR Phase 2', 'SBIR Phase 3']
managing_program_codes = ['5371', '7918', '8019']
award_amounts = [400000, 2000000, 524987]
requested_amounts = [506507, 16000, 637962]
program_officers = ['Chen, James', 'Phillips, Michael', 'Davis, Susan']
proposal_id_start = 1840000


class Proposal:
    def __init__(self, proposal_id, status, directorate, division, 
                    institution, state, pi_name, pi_institution, title, announcement,
                    funding_program, funding_program_code, managing_program,
                    managing_program_code, award_amount, requested_amount,
                    program_officer, nsf_received_date, od_concur_date, reviewer_name):
        self.proposal_id = proposal_id
        self.status = status
        self.directorate = directorate
        self.division = division
        self.institution = institution
        self.institution_state = state
        self.pi_name = pi_name
        self.pi_institution = pi_institution
        self.title = title

        self.program_announcement = announcement
        self.funding_program = funding_program
        self.funding_program_code = funding_program_code
        self.managing_program = managing_program
        self.managing_program_code = managing_program_code
        self.award_amount = award_amount
        self.requested_amount = requested_amount
        self.program_officer = program_officer
        self.nsf_received_date = nsf_received_date
        self.od_concur_date = od_concur_date

        self.reviewer_name = reviewer_name

doc_list = []

with open(file_path) as f:
    lines = f.readlines()

    for line in lines:
        # print(line)
        data = json.loads(line)
        print(data)

        # Increment Proposal ID
        proposal_id_start += 1
        proposal_id = proposal_id_start

        # Set other data
        status = random.choice(statuses)
        directorate = random.choice(directorates)
        division = random.choice(divisions)
        institution = random.choice(institutions)
        institution_state = random.choice(states)
        pi_name = data['submitter']
        pi_institution = random.choice(institutions)
        title = data['title']
        program_announcement = random.choice(announcements)
        funding_program = random.choice(funding_programs)
        funding_program_code = random.choice(funding_program_codes)
        managing_program = random.choice(managing_programs)
        managing_program_code = random.choice(managing_program_codes)
        award_amount = random.choice(award_amounts)
        requested_amount = random.choice(requested_amounts)
        program_officer = random.choice(program_officers)
        nsf_received_date = data['update_date']
        nsf_received_date_obj = datetime.strptime(nsf_received_date, '%Y-%m-%d')
        random_days = random.randint(1,60)
        od_concur_date = nsf_received_date_obj + timedelta(days=random_days)
        reviewer_name = random.choice(reviewer_names)

        proposal = Proposal(proposal_id, status, directorate, division, institution, institution_state, pi_name, pi_institution, 
                                title, program_announcement, funding_program, funding_program_code, managing_program, managing_program_code, award_amount,
                                requested_amount, program_officer, nsf_received_date_obj.isoformat() + 'Z', od_concur_date.isoformat() + 'Z', reviewer_name)
        
        proposal_dict = proposal.__dict__
        doc_list.append(proposal_dict)

# Break list into batches per API limit
# https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html

batch_list = divide_chunks(doc_list, 100)

# app_search = AppSearch("https://izmaxx-hostrisk-8-1.ent.us-central1.gcp.cloud.es.io:9243",bearer_auth=os.environ.get('APP_SEARCH_API_KEY'))

# engine_info = app_search.get_engine(engine_name='nsf-testing')
# print(engine_info)
CLOUD_ID='izmaxx-hostrisk-81:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDNmZWZmZGQ0ZjJjNDQ2OWI4ZjI2M2IyNDg5YWQ4NGY3JGMwNTA0ZTM0YTJkMDQxYjg4NjZlMWFiNWJlMTliYmM3'
CLOUD_API_KEY='MXV4X0Y0RUJSdC1PNmxBcjVSZnE6d3Z4QVRZZ25UQTYxS2NDR3JENDBCZw=='

# for batch in batch_list:
#     app_search_result = app_search.index_documents(
#         engine_name="nsf-testing2",
#         documents=batch
#     )

# print(app_search_result)
es = Elasticsearch(cloud_id=CLOUD_ID,api_key=CLOUD_API_KEY)
result = es.ping()
print(result)
if result:
    print("Connected to Elasticsearch")
    try:
        resp = helpers.bulk(es, doc_list, index=INDEX_NAME)
        print ("helpers.bulk() RESPONSE:", resp)
        print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))
    except helpers.BulkIndexError as bulkIndexError:
        print("Indexing error: {0}".format(bulkIndexError))
else:
    print("Not connected")






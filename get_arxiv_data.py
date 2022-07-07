import arxiv
# from elasticsearch import Elasticsearch, helpers
import csv
import os
import json
from pathlib import Path
import random
from datetime import datetime, timedelta
from elastic_enterprise_search import AppSearch

base_path = Path(__file__).parent
file_path = (base_path / "arxiv-small.json").resolve()
INDEX_NAME = "nsf-proposals"

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
                    program_officer, nsf_received_date, od_concur_date, reviewer_name, abstract):
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
        self.abstract = abstract

def create_randomized_proposal(reviewer_names, directorates, statuses, divisions, institutions, states, announcements, funding_programs, funding_program_codes, managing_programs, managing_program_codes, award_amounts, requested_amounts, program_officers, proposal_id_start, Proposal, result, authors):
    proposal_id_start += 1
    proposal_id = proposal_id_start
    status = random.choice(statuses)
    directorate = random.choice(directorates)
    division = random.choice(divisions)
    institution = random.choice(institutions)
    institution_state = random.choice(states)
    pi_name = authors
    pi_institution = random.choice(institutions)
    title = result.title
    program_announcement = random.choice(announcements)
    funding_program = random.choice(funding_programs)
    funding_program_code = random.choice(funding_program_codes)
    managing_program = random.choice(managing_programs)
    managing_program_code = random.choice(managing_program_codes)
    award_amount = random.choice(award_amounts)
    requested_amount = random.choice(requested_amounts)
    program_officer = random.choice(program_officers)
    nsf_received_date = result.published
  # nsf_received_date_obj = datetime.strptime(nsf_received_date, '%Y-%m-%d')

    random_days = random.randint(1,60)
    od_concur_date = nsf_received_date + timedelta(days=random_days)
    reviewer_name = random.choice(reviewer_names)
    abstract = result.summary

    proposal = Proposal(proposal_id, status, directorate, division, institution, institution_state, pi_name, pi_institution, 
                          title, program_announcement, funding_program, funding_program_code, managing_program, managing_program_code, award_amount,
                          requested_amount, program_officer, nsf_received_date, od_concur_date, reviewer_name, abstract)
                            
    return proposal

doc_list = []

search = arxiv.Search(
  query = "ti:net AND ti:zero",
  max_results = 10,
  sort_by = arxiv.SortCriterion.SubmittedDate
)


for result in search.results():
  print(result.title)
  authors = []
  for author in result.authors:
    authors.append(author.name)

  proposal = create_randomized_proposal(reviewer_names, directorates, statuses, divisions, institutions, states, announcements, funding_programs, funding_program_codes, managing_programs, managing_program_codes, award_amounts, requested_amounts, program_officers, proposal_id_start, Proposal, result, authors)
  
  proposal_dict = proposal.__dict__
  print(proposal_dict)
  doc_list.append(proposal_dict)

        
# Break list into batches per API limit
# https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html
batch_list = divide_chunks(doc_list, 100)

# Connect to Elastic App Search
app_search = AppSearch("https://izmaxx-hostrisk-8-1.ent.us-central1.gcp.cloud.es.io:9243",bearer_auth=os.environ.get('APP_SEARCH_API_KEY'))

for batch in batch_list:
    app_search_result = app_search.index_documents(
        engine_name="nsf-testing2",
        documents=batch
    )

print(app_search_result)


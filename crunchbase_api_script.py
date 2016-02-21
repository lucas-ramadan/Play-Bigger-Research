import pycrunchbase as pcb
import os
from io import open
from csv import reader

__author__ = 'Lucas Ramadan'

def get_company_list(filename):
	""" 
	Quick function to handle reading in CSV files, and getting companies
	"""
	with open(filename, 'r') as f:
		data = [row for row in reader(f.read().splitlines())]
	
	# now get the company names from data, ignoring header row
	# take the set so that we do not make duplicate API calls
	companies = set([d[0] for d in data[1:]])

	return companies

def get_company_description(company_name, cb):
	
	"""
	This function will make the CrunchBase API call for a given company name.
	"""

	# force company_name to be lowercase
	company_name = company_name.lower()

	# fix formatting for crunchbase API
	if ' ' in company_name:
		company_name = company_name.replace(' ', '-')

	# try getting description of company, otherwise make empty
	try:
		company_description = cb.organization(company_name).description

	except: 
		print "Can't find company: %s" % company_name
		company_description = u''

	# force NoneType descriptions to be empty strings, for file writing
	if company_description == None:
		company_description = u''

	# finally give back the description data
	return company_description

def get_all_descriptions(company_list):
	
	"""
	This function will iterate through the company list
	and gather the description data for each company in the list. 
	It will then write the description to a file, as company_name.txt .
	It will also keep track of the companies that have missing descriptions.
	"""

	# first, get CB API Key from hidden file
	with open('.CB_key', 'r') as f: 
		cb_key = f.read().replace('\n', '')

	# initialize cb connection
	cb = pcb.CrunchBase(cb_key)

	# will save the missing list later
	missing = []

	# run through the company list and get description data
	for company in company_list:

		description = get_company_description(company, cb)

		# ie we didn't find a description for the company, make note
		if description == u'' or description == None:
			missing.append(unicode(company))

		# just a little bit of filepath creating
		filename = company + '.txt'
		path = os.path.dirname(os.path.abspath(__file__))+'/descriptions'
		full_filename = os.path.join(path, filename)
		
		# write company description to file
		with open(full_filename, 'w', encoding='utf-8') as c:
			c.write(description)

	# finally, save the missing companies file
	with open('no_description_companies.txt', 'w', encoding='utf-8') as t:
		t.writelines(missing)

# run the script 
if __name__ == '__main__':
	# TODO - update this with arg v?

	# first get the data from the specified file 
	companies = get_company_list('Q2_2015_updated_master (v30).csv')
	# companies = ['theBench']
	# companies = ['Credit Karma']

	# finally, run the get_all_descriptions function to get the files
	get_all_descriptions(companies)

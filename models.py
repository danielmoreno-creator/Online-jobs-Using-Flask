import os
from pymongo import MongoClient
from bson import ObjectId

class JobListing(object):
    def __init__(self, job_id=None, job_title=None, company_name=None, location=None, job_description=None, application_instructions=None, employer_id=None):
        self.job_id = job_id
        self.job_title = job_title
        self.company_name = company_name
        self.location = location
        self.job_description = job_description
        self.application_instructions = application_instructions
        self.employer_id = employer_id

    @staticmethod
    def find_all():
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client['job_board']
        job_listings = list(db['job_listings'].find())
        return job_listings
    
    @staticmethod
    def find_by_id(job_id):
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client['job_board']
        job_listing = db['job_listings'].find_one({'_id': ObjectId(job_id)})
        return job_listing

    @staticmethod
    def find_all_by_employer(employer_id):
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client['job_board']
        job_listings = list(db['job_listings'].find({'employer_id': ObjectId(employer_id)}))
        return job_listings

    def save(self):
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client['job_board']
        if self.job_id is None:
            self.job_id = ObjectId()
        db['job_listings'].update_one({'_id': self.job_id}, {'$set': self.to_dict()}, upsert=True)

    def to_dict(self):
        return {
            'job_title': self.job_title,
            'company_name': self.company_name,
            'location': self.location,
            'job_description': self.job_description,
            'application_instructions': self.application_instructions,
            'employer_id': self.employer_id
        }

class JobApplication(object):
    def __init__(self, application_id=None, job_id=None, applicant_name=None, applicant_email=None, applicant_contact_information=None):
        self.application_id = application_id
        self.job_id = job_id
        self.applicant_name = applicant_name
        self.applicant_email = applicant_email
        self.applicant_contact_information = applicant_contact_information

    @staticmethod
    def find_all_by_job(job_id):
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client['job_board']
        job_applications = list(db['job_applications'].find({'job_id': ObjectId(job_id)}))
        return job_applications

    def save(self):
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client['job_board']
        if self.application_id is None:
            self.application_id = ObjectId()
        db['job_applications'].update_one({'_id': self.application_id}, {'$set': self.to_dict()}, upsert=True)

    def to_dict(self):
        return {
            'job_id': self.job_id,
            'applicant_name': self.applicant_name,
            'applicant_email': self.applicant_email,
            'applicant_contact_information': self.applicant_contact_information
        }

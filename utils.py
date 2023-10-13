import re

def validate_job_application(job_application):
    errors = {}

    if not job_application['applicant_name']:
        errors['applicant_name'] = 'Applicant name is required.'

    if not job_application['applicant_email']:
        errors['applicant_email'] = 'Applicant email is required.'

    if not re.match(r'[^@]+@[^@]+\.[^@]+', job_application['applicant_email']):
        errors['applicant_email'] = 'Invalid applicant email address.'

    if not job_application['applicant_contact_information']:
        errors['applicant_contact_information'] = 'Applicant contact information is required.'

    return errors

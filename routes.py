from flask import render_template, redirect, url_for, request
from models import JobListing, JobApplication

# Import the 'app' instance from app.py to create the app.route decorators
from app import app

@app.route('/search')
def search_job_listings():
    # Get the search query from the request
    search_query = request.args.get('search_query')

    # Use the JobListing.find_all() method to retrieve all job listings
    job_listings = JobListing.find_all()

    # Filter job listings based on the search query
    job_listings = [job for job in job_listings if search_query.lower() in job.job_title.lower()]

    # Render the job listings page with the filtered results
    return render_template('job_listings.html', job_listings=job_listings)

@app.route('/employer/edit-job/<job_id>')
def edit_job(job_id):
    # Get the job listing with the given ID
    job_listing = JobListing.find_by_id(job_id)

    # Render the edit job page
    return render_template('edit_job.html', job_listing=job_listing)

@app.route('/employer/edit-job/<job_id>', methods=['POST'])
def edit_job_submit(job_id):
    # Update the job listing with the new values
    job_listing = JobListing.find_by_id(job_id)
    job_listing.job_title = request.form['job_title']
    job_listing.company_name = request.form['company_name']
    job_listing.location = request.form['location']
    job_listing.job_description = request.form['job_description']
    job_listing.application_instructions = request.form['application_instructions']

    # Save the job listing to the database
    job_listing.save()

    # Redirect to the employer dashboard page
    return redirect(url_for('employer_dashboard'))

@app.route('/employer/delete-job/<job_id>')
def delete_job(job_id):
    # Delete the job listing with the given ID
    job_listing = JobListing.find_by_id(job_id)
    if job_listing:
        job_listing.delete()  # Assuming you have a 'delete' method in your model
    # Redirect to the employer dashboard page
    return redirect(url_for('employer_dashboard'))

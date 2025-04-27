import pandas as pd
from typing import List, Dict, Optional

class DataIntegrator:
    def __init__(self):
        # Load sample data
        self.jobs_df = pd.read_csv('data/job_listings.csv')
        self.events_df = pd.read_csv('data/events.csv')
        self.mentorship_df = pd.read_csv('data/mentorship_programs.csv')

    def search_jobs(self, query: str) -> List[Dict]:
        """
        Search for jobs matching the query
        """
        # Convert query to lowercase for case-insensitive search
        query = query.lower()
        
        # Search in job titles and descriptions
        matching_jobs = self.jobs_df[
            self.jobs_df['title'].str.lower().str.contains(query) |
            self.jobs_df['description'].str.lower().str.contains(query)
        ]
        
        return matching_jobs.to_dict('records')

    def search_events(self, query: str) -> List[Dict]:
        """
        Search for events matching the query
        """
        # Convert query to lowercase for case-insensitive search
        query = query.lower()
        
        # Search in event names and descriptions
        matching_events = self.events_df[
            self.events_df['name'].str.lower().str.contains(query) |
            self.events_df['description'].str.lower().str.contains(query)
        ]
        
        return matching_events.to_dict('records')

    def get_mentorship_programs(self) -> List[Dict]:
        """
        Get all mentorship programs
        """
        return self.mentorship_df.to_dict('records')

    def get_event_details(self, event_id: str) -> Optional[Dict]:
        """
        Get details for a specific event
        """
        event = self.events_df[self.events_df['id'] == event_id]
        if not event.empty:
            return event.iloc[0].to_dict()
        return None

    def get_job_details(self, job_id: str) -> Optional[Dict]:
        """
        Get details for a specific job
        """
        job = self.jobs_df[self.jobs_df['id'] == job_id]
        if not job.empty:
            return job.iloc[0].to_dict()
        return None 
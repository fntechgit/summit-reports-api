# openstack-survey-api
GraphQL API to access survey data and reports

After cloning:

- create virtual environment :
  * on project root run : 
      - python3.6 -m venv venv
      - source venv/bin/activate
      
- install requirements : 
  * pip install -r requirements.txt
  * if you add requirements update file by running "pip freeze > requirements.txt"
  
- set Openstack DB credentials from .env
  
  
  Run Project : 
  - python ./manage.py makemigrations
  - python ./manage.py migrate
  - python ./manage.py runserver
  - go to http://localhost:8000/reports?access_token=xxx
  - Example: 
    TAG REPORT 
    {
  reportData: tags(summitId: 31, published: true) {
    results: results(limit: 25) {
      id
      tag
      eventCount(summitId: 31)
    }
    totalCount
  }
}


# openstack-survey-api
GraphQL API to access survey data and reports

After cloning:

- create virtual environment :
  * on project root run : 
      - virtualenv venv
      - source venv/bin/activate
      
- install requirements : 
  * pip install -r requirements.txt
  * if you add requirements update file by running "pip freeze > requirements.txt"
  
- create 'reports_api' DB
  * also check in settings.py the DB credentials
  
  
  Run Project : 
  - python ./manage.py runserver
  - go to http://localhost:8000/reports?access_token=xxx
  - Example: 
    query {
        allQuestions(name: "FirstName") {
            edges {
              node {
                id,
                name
              }
            }
        }
    }

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
  
- set Openstack DB credentials from .env
  
  
  Run Project : 
  - python ./manage.py makemigrations
  - python ./manage.py migrate
  - python ./manage.py runserver
  - go to http://localhost:8000/reports?access_token=xxx
  - Example: 
    TAG REPORT 
    {
      allTags(hasEventsFromSummit:25) {
        edges {
          node {
            id
            tag
            events (summit_Id:25, published:true){
              edges {
                node {
                  id
                }
              }
            }
          }
        }
      }
    }

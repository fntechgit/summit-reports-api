from django.shortcuts import render
from django import http
import json
from django.db import models

# Create your views here.


def get_tag_report(request):


    json_result = SurveySerializer(survey).data
    data = json.dumps(json_result, indent=2)

    return http.HttpResponse(data, content_type="application/json")
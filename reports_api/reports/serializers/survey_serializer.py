from rest_framework import serializers
from reports_api.reports.models import Survey, SurveyStep, SurveyStepTemplate, SurveyAnswer, SurveyQuestionTemplate, SurveyQuestionValueTemplate, Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields= '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = SurveyAnswer
        fields = '__all__'

    def get_value(self, obj):
        if not obj.value: return 'N/A';
        temp_value = obj.value

        if obj.question.value_options.all().count():
            if obj.question.is_multi_value():
                answers = obj.value.split(',')
                temp_value_array = []
                for answer in answers:
                    if  obj.question.is_double_entry():
                        dbl_answer_temp = answer.split(':')
                        dbl_answer = obj.question.value_options.get(id=dbl_answer_temp[0]).value + ':' + obj.question.value_options.get(id=dbl_answer_temp[1]).value
                        temp_value_array.append(dbl_answer)
                    else:
                        temp_value_array.append(obj.question.value_options.get(id=answer).value)

                temp_value = ', '.join(temp_value_array)
            else:
                temp_value = obj.question.value_options.get(id=obj.value).value

        return temp_value

    def get_question(self, obj):
        return obj.question.label


class StepSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True, required=False)
    name = serializers.SerializerMethodField()

    class Meta:
        model = SurveyStep
        fields = ['id', 'name', 'state', 'answers']

    def get_name(self, obj):
        return obj.step_template.friendly_name

    def validate(self, data):
        if data['answers'].count == 0:
            raise serializers.ValidationError("must have answers")
        return data


class EntitySurveySerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, required=False)
    class Meta:
        model = Survey
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, required=False)
    entity_surveys = EntitySurveySerializer(many=True, required=False)
    owner = MemberSerializer()

    class Meta:
        model = Survey
        fields = ['id','last_edited','lang','state','owner','steps','entity_surveys']





from rest_framework import serializers
from .models import Interview, Question, Answer, PossibleAnswer


class PossibleAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PossibleAnswer
        fields = ('id', 'text')


class QuestionSerializer(serializers.ModelSerializer):
    possible_answers = PossibleAnswerSerializer(required=False, many=True)

    def to_representation(self, instance):
        rep = super(QuestionSerializer, self).to_representation(instance)
        if not rep.get('possible_answers'):
            rep.pop('possible_answers')
        return rep

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'possible_answers')


class InterviewSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(required=True, many=True)

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(InterviewSerializer, self).__init__(*args, **kwargs)

        if self.context.get('request'):
            request = self.context['request']
            if request.method == 'PUT':
                self.fields.pop('start_time')

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        interview = Interview(**validated_data)
        interview.save()

        for question in questions:
            possible_answers = question.pop('possible_answers', None)
            new_question = Question.objects.create(interview=interview, **question)
            if possible_answers and new_question.type is not Question.TEXT_ANSWER:
                for possible_answer in possible_answers:
                    PossibleAnswer.objects.create(question=new_question, **possible_answer)
        return interview

    class Meta:
        model = Interview
        fields = ['name', 'start_time', 'end_time', 'description', 'questions']


class AnswerSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(AnswerSerializer, self).__init__(many=True, *args, **kwargs)

    def create(self, validated_data):
        question = validated_data['question']
        if question.type == Question.TEXT_ANSWER and not validated_data.get('text_answer'):
            raise serializers.ValidationError('Need text answer')
        if question.type != Question.TEXT_ANSWER and not validated_data.get('answer'):
            raise serializers.ValidationError('Need choice answer')
        if (question.type == Question.ONE_ANSWER
                and validated_data.get('answer')
                and 0 > len(validated_data['answer']) > 1):
            raise serializers.ValidationError('Only one answer required')
        if (question.type == Question.MANY_ANSWER
                and validated_data.get('answer')
                and 0 > len(validated_data['answer'])):
            raise serializers.ValidationError('Choice answer required')
        choice_answers = validated_data.pop('answer', None)
        # Тут немного юзер анонимный приходит, не знаю с чем связано если честно, не смог нагуглить
        answer = Answer.objects.create(user=self.context.get('user'), **validated_data)
        if choice_answers:
            for choice_answer in choice_answers:
                answer.answer.add(choice_answer)
        return answer

    def to_representation(self, instance):
        rep = super(AnswerSerializer, self).to_representation(instance)
        interview__id = rep.get('interview')
        interview = Interview.objects.get(id=interview__id)
        question__id = rep.get('question')
        question = Question.objects.get(id=question__id)
        answer__id = rep.get('answer')
        if answer__id:
            rep['answer'] = []
            for pk in answer__id:
                answer = PossibleAnswer.objects.get(id=pk)
                rep['answer'].append({'id': answer.id, 'text': answer.text})
        rep['question'] = {'id': question.id, 'text': question.text, 'type': question.type}
        rep['interview'] = {'id': interview.id, 'name': interview.name}
        if question.type == Question.TEXT_ANSWER:
            rep.pop('answer')
        else:
            rep.pop('text_answer')
        return rep

    class Meta:
        model = Answer
        fields = ['interview', 'answer', 'text_answer', 'question']

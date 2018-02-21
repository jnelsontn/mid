from rest_framework import serializers
from .func import get_max_value
from .models import *


class ProductAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductArea
        fields = ('product_area_id', 'product_area_name', )


class FeaturesSerializer(serializers.ModelSerializer):

    product_area = serializers.PrimaryKeyRelatedField(queryset=ProductArea.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())

    def create(self, validated_data):
        project = validated_data['project']
        priority = validated_data.get('priority', None)
        max_value = get_max_value(project)

        if max_value:
            if priority is None or priority == '':
                validated_data['priority'] = 1
            elif priority > max_value or priority == 0:
                if priority == 0:
                    validated_data['priority'] = 1
                elif priority > max_value:
                    validated_data['priority'] = max_value + 1
        else:
            validated_data['priority'] = 1

        return Features.objects.create(**validated_data)

    def update(self, instance, validated_data):
        project = instance.project
        max_value = get_max_value(project)

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        priority = validated_data.get('priority', None)
        if max_value:
            if priority is None or priority == '':
                instance.priority = 1
            elif priority >= max_value:
                instance.priority = max_value + 1
            elif priority == 0:
                instance.priority = 1
            else:
                instance.priority = priority
        else:
            instance.priority = 1

        instance.target_date = validated_data.get('target_date', instance.target_date)
        instance.project = instance.project
        instance.product_area = validated_data.get('product_area', instance.product_area)
        instance.save()

        return instance

    class Meta:
        model = Features
        fields = ('features_id', 'title', 'description', 'priority',
                  'target_date', 'project', 'product_area')


class ProjectsSerializer(serializers.ModelSerializer):

    features = FeaturesSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        fields = '__all__'


class ClientsSerializer(serializers.ModelSerializer):

    projects = ProjectsSerializer(many=True, read_only=True)

    class Meta:
        model = Clients
        fields = '__all__'

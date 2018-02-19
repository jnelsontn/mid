from rest_framework import serializers
from .models import *


class ProductAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductArea
        fields = ('product_area_id', 'product_area_name', )


class FeaturesSerializer(serializers.ModelSerializer):

    product_area = serializers.PrimaryKeyRelatedField(queryset=ProductArea.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.title)
        instance.priority = validated_data.get('priority', instance.title)
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



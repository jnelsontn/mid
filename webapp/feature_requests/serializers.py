from rest_framework import serializers
from .models import *


class ProductAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductArea
        fields = ('product_area_id', 'product_area_name', )


class FeaturesSerializer(serializers.ModelSerializer):

    product_area = serializers.PrimaryKeyRelatedField(queryset=ProductArea.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())

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



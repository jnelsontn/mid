from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .serializers import *

import random


class CreateObjectsTest(APITestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.client_create = {'client_name': 'Client Five'}
        self.project_create = {'client': 1, 'project_name': 'Project Blue'}
        self.feature_create = {'title': 'Oranges', 'description': 'Bag of Oranges', 'project': 1, 'priority': 1,
                               'target_date': '2015-02-02', 'product_area': 3 }

    def test_can_create_client(self):
        response = self.client.post(reverse('clients-list'), self.client_create)
        queryset = Clients.objects.all().values_list('client_name', flat=True)
        self.assertIn('Client Five', queryset)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_project(self):
        response = self.client.post(reverse('projects-list'), self.project_create)
        queryset = Projects.objects.all().values_list('project_name', flat=True)
        self.assertIn('Project Blue', queryset)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_feature(self):
        response = self.client.post(reverse('features-list'), self.feature_create)
        queryset = Features.objects.filter(project=1).values_list('title', flat=True)

        self.assertIn('Oranges', queryset)
        self.assertEqual(Features.objects.filter(project=1).count(), 7)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_bad_feature(self):
        new_feature = self.feature_create
        new_feature['project'] = 900
        response = self.client.post(reverse('features-list'), new_feature)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_non_existent_feature(self):
        response = self.client.get(reverse('features-detail', kwargs={'pk': Features.objects.last().pk + 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ChangePriorityTest(APITestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.feature_request_one = {"title": "Generic Feature A", "description": "Generic Feature A", "project": 1,
                                    "priority": 2, "target_date": "2018-02-19", "product_area": 2}
        self.feature_request_two = {"title": "Generic Feature B", "description": "Generic Feature B", "project": 1,
                                    "priority": 2, "target_date": "2018-02-19", "product_area": 2}
        self.feature_request_three = {"title": "Generic Feature C", "description": "Generic Feature C", "project": 1,
                                      "priority": 1, "target_date": "2018-02-19", "product_area": 2}
        self.new_feature = {'title': 'Oranges', 'description': 'Bag of Oranges', 'project': 1, 'priority': 1,
                            'target_date': '2015-02-02', 'product_area': 3}

    def test_priority_change_one_to_two(self):
        self.client.put(reverse('features-detail', kwargs={'pk': 1}), self.feature_request_one)
        self.assertEqual(Features.objects.get(pk=1).priority, 2)
        self.assertEqual(Features.objects.get(pk=2).priority, 1)

    def test_priority_change_three_to_one(self):
        self.client.put(reverse('features-detail', kwargs={'pk': 3}), self.feature_request_three)
        self.assertEqual(Features.objects.get(pk=3).priority, 1)
        self.assertEqual(Features.objects.get(pk=1).priority, 2)
        self.assertEqual(Features.objects.get(pk=2).priority, 3)
        self.assertEqual(Features.objects.get(pk=4).priority, 4)

    def test_new_feature_priority_one(self):
        self.client.post(reverse('features-list'), self.new_feature)
        self.assertEqual(Features.objects.filter(project=1).count(), 7)
        self.assertEqual(Features.objects.get(pk=1).priority, 2)
        self.assertEqual(Features.objects.last().priority, 1)

    def test_out_of_range_priority(self):
        feature_two = self.feature_request_two
        feature_two['priority'] = random.randint(10, 90)

        response = self.client.put(reverse('features-detail', kwargs={'pk': 2}), feature_two)
        self.assertNotContains(response, feature_two['priority'])
        self.assertEqual(Features.objects.get(pk=2).priority, 6)


class CreateClientProjectFeatureTest(APITestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.client_create = {'client_name': 'Client Five'}
        self.project_create = {'client': 5, 'project_name': 'Project Blue'}
        self.feature_create = {'title': 'Oranges',
                               'description': 'Bag of Oranges',
                               'priority': 1,
                               'target_date': '2015-02-02',
                               'project': 8,
                               'product_area': 3
                               }

    def test_created_feature_is_equal_to_submit(self):
        self.client.post(reverse('clients-list'), self.client_create)
        new_project = self.client.post(reverse('projects-list'), self.project_create)
        new_feature = self.client.post(reverse('features-list'), self.feature_create)

        response = self.client.get(reverse('features-detail', kwargs={'pk': new_feature.data['features_id']}))
        response_dict = response.data
        del response_dict['features_id']

        self.assertDictEqual(response_dict, self.feature_create)
        self.assertEqual(Features.objects.filter(project=new_project.data['project_id']).count(), 1)

        self.assertIn('Client Five', Clients.objects.all().values_list('client_name', flat=True))
        self.assertIn('Project Blue', Projects.objects.all().values_list('project_name', flat=True))
        self.assertIn('Oranges', Features.objects.all().values_list('title', flat=True))

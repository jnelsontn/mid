from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=30)

    def __str__(self):
        return self.client_name


class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    client = models.ForeignKey(Clients, on_delete=models.PROTECT, related_name='projects')

    def __str__(self):
        return self.project_name + ' (' + self.client.client_name + ')'

    class Meta:
        unique_together = (('project_id', 'client'),)


class Features(models.Model):
    features_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    project = models.ForeignKey(Projects, on_delete=models.PROTECT, related_name='project')
    priority = models.IntegerField(null=False, blank=False, default=1)
    target_date = models.DateField()
    product_area = models.ForeignKey('ProductArea', on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return self.title + ' (' + str(self.priority) + ')' + ' Project: ' + str(self.project)

    class Meta:
        unique_together = (('features_id', 'project'),)


class ProductArea(models.Model):
    product_area_id = models.AutoField(primary_key=True)
    product_area_name = models.CharField(max_length=100)

    def __str__(self):
        return self.product_area_name



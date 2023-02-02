from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User



unique_attribute_validator = UniqueValidator(queryset=User.objects.all(), lookup='iexact')


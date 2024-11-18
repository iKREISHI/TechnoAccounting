from rest_framework import serializers

from apps.accounting.models import Rental



class RentalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['equipment', 'renter', 'assign_by', 'start_time',
                  'end_time', 'actual_return_time', 'status', 'location']

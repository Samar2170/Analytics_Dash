from django.core.management.base import BaseCommand
from core.models import AppInstalls
import pandas as pd


class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        df = pd.read_csv('Assets/installs - installs.csv')
        for index, row in df.iterrows():
            date = row['date']
            package_name = row['package_name']
            carrier = row['carrier']
            daily_device_installs = row['daily_device_installs']
            active_device_installs = row['active_device_installs']
            AppInstalls.objects.create(date=date, package_name=package_name, carrier=carrier, daily_device_installs=daily_device_installs, active_device_installs=active_device_installs)
        print('Data inserted successfully')


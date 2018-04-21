import csv

from django.core.management.base import BaseCommand
from schools import models


class Command(BaseCommand):
    help = 'Import schools from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs['path']) as f:
            reader = csv.DictReader(f, delimiter=',')

            models.School.objects.bulk_create([
                models.School(**self._school_value(row))
                for row in reader
            ])

    def _school_value(self, row):
        row.update({
            'name': row['school_name'],
            'website': row['url_address'],
            'phone_number': row['telephone_no'],
            'fax_number': row['fax_no'],
            'email': row['email_address'],
            'vision_statement': row['visionstatement_desc'],
            'mission_statement': row['missionstatement_desc'],
            'philosophy': row['philosophy_culture_ethos'],
            'type': row['type_code'],
            'session': row['session_code'],
            'main_level': row['mainlevel_code'],
            'language': row['mothertongue1_code'],
            'offer': row['special_sdp_offered']
        })
        return {k: row[k] for k in models.School.field_names}

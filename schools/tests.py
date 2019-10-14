import csv

import pytest
from django_elasticsearch_dsl.registries import registry

from . import documents, models, views


def to_school_value(row):
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
    return {k: row[k] for k in documents.SchoolDocument.Django.fields}


@pytest.mark.django_db
def test_pagination(rf, django_assert_num_queries):
    with open('general-information-of-schools.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        models.School.objects.bulk_create([
            models.School(**to_school_value(row))
            for row in reader
        ])

        for index in registry.get_indices([models.School]):
            index.create()

        for doc in registry.get_documents([models.School]):
            doc().update(doc().get_queryset())

    request = rf.get('/api/v1/schools', {'q': 'china'})
    response = views.SchoolListView.as_view()(request)
    assert response.status_code == 200
    assert response.data['count'] == 14
    assert len(response.data['results']) == 14

    request = rf.get('/api/v1/schools', {'q': 'china', 'limit': 10})
    response = views.SchoolListView.as_view()(request)
    assert response.status_code == 200
    assert response.data['count'] == 14
    assert len(response.data['results']) == 10
    assert response.data['next'] is not None
    assert response.data['previous'] is None

    request = rf.get('/api/v1/schools', {'q': 'china', 'offset': 10})
    response = views.SchoolListView.as_view()(request)
    assert response.status_code == 200
    assert response.data['count'] == 14
    assert len(response.data['results']) == 4
    assert response.data['next'] is None
    assert response.data['previous'] is not None

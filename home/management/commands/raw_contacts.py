import json
from home.models import JsonRegistration, RawRegistration

# create model for RawRegistration

for json_contact_row in JsonRegistration.objects.all():
    uuid = json_contact_row.uuid

    # Update contact
    if RawRegistration.objects.filter(uuid=uuid):
        print("updating a contact with uuid %s" % uuid)
        raw_contacts = RawRegistration.objects.get(uuid=uuid)
    # Create contact
    else:
        print("creating a contact with uuid %s" % uuid)
        raw_contacts = RawRegistration()
        raw_contacts.uuid = uuid

    # Create api_data from json_contact_row to import to RawRegistration
    api_data = json.loads(json_contact_row.json)
    # In 2017 RapidPro added capacity to have several telephone numbers for one contact
    # In Nigeria personnel with two or more telephone numbers are registered on separate rows
    raw_contacts.urn = api_data['urns'][0]
    raw_contacts.name = api_data['name']
    # Data on siteid, type, post and mail are dictionaries in dictionaries in the api data
    raw_contacts.siteid = api_data['fields']['siteid']
    raw_contacts.type = api_data['fields']['type']
    raw_contacts.post = api_data['fields']['post']
    raw_contacts.mail = api_data['fields']['mail']
    raw_contacts.first_seen = api_data['created_on']
    raw_contacts.last_seen = api_data['modified_on']

    print
    api_data['urns']
    raw_contacts.save()
    print(raw_contacts.name)






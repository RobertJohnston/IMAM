import json
from home.models import JsonProgram, RawProgram

# create model for RawProgram, make migrations, migrate

for json_program_row in JsonProgram.objects.all():
    id = json_program_row.id

    # Update contact
    if RawProgram.objects.filter(id=id):
        print("updating a contact with uuid %s" % id)
        raw_program = RawProgram.objects.get(id=id)
    # Create contact
    else:
        print("creating a contact with uuid %s" % id)
        raw_program = RawProgram()
        raw_program.id = id

    # Create api_data from json_program_row to import to RawProgram
    api_data = json.loads(json_program_row.json)


    raw_program.last_seen = api_data['modified_on']



    contact_uuid
    urn
    name
    groups
    role
    siteid
    first_seen
    last_seen
    weeknum
    type
    age_group
    beg
    amar
    tin
    dcur
    dead
    defu
    dmed
    tout
    confirm
    state_num
    lga_num

    year
    last_seen_weeknum
    rep_year_wn
    rep_weeknum
    last_seen_dotw
    last_seen_hour
    year_weeknum
    iso_rep_year_wn
    iso_year_weeknum
    iso_diff
    # since_x_weeks = models.BigIntegerField(blank=True, null=True)

    print
    api_data['urns']
    raw_program.save()
    print(raw_program.name)


stuff = {
    "modified_on": "2016-06-28T12:19:16.836849Z",
    "created_on": "2016-06-28T12:09:27.827611Z",
    "contact": {
        "name": "Abdullahi Lawali Araba.",
        "uuid": "25ad4c50-5316-4f41-9aaf-d58aba7216ff"
    },
    "values": {
        "tout_o": {
            "category": "0 - 9999",
            "node": "080391f8-79c6-4ee8-8c4c-217295d0c3c0",
            "value": 0.0,
            "time": "2016-06-28T12:16:00.591663Z"
        },
        "weeknum": {
            "category": "1 - 53",
            "node": "17449ec7-7390-4605-b3a9-39438849119a",
            "value": 23.0,
            "time": "2016-06-28T12:12:15.074772Z"
        },
        "beg_o": {
            "category": "0 - 9999",
            "node": "2afcda2d-b90a-4caf-83a1-71a223c63082",
            "value": 66.0,
            "time": "2016-06-28T12:12:50.753793Z"
        },
        "amar_o": {
            "category": "0 - 9999",
            "node": "e7d96279-b9fb-4ed6-8d0f-85fca4ed272d",
            "value": 8.0,
            "time": "2016-06-28T12:14:08.427802Z"
        },
        "msg_routing": {
            "category": "Site",
            "node": "9e71a65a-1d5e-4757-8f40-b51a5c1becdc",
            "value": "Site",
            "time": "2016-06-28T12:19:16.390776Z"
        },
        "defu_o": {
            "category": "0 - 9999",
            "node": "8a405d35-4717-48de-8c51-061c99d467fb",
            "value": 0.0,
            "time": "2016-06-28T12:15:13.727809Z"
        },
        "confirm": {
            "category": "Yes",
            "node": "1e7b41ad-745b-450b-b373-1cbd5846ca16",
            "value": "Yes",
            "time": "2016-06-28T12:19:16.074387Z"
        },
        "dead_o": {
            "category": "0 - 9999",
            "node": "8a235d64-a25b-4587-8ee0-c7f77d7ebbb4",
            "value": 0.0,
            "time": "2016-06-28T12:14:56.495848Z"
        },
        "role": {
            "category": "Implementation",
            "node": "112b23e2-6e60-4f14-bc55-53c069f31250",
            "value": "Site",
            "time": "2016-06-28T12:12:15.199256Z"
        },
        "dcur_o": {
            "category": "0 - 9999",
            "node": "a42e4631-f17d-460a-9605-98611c376ed5",
            "value": 10.0,
            "time": "2016-06-28T12:14:39.311012Z"
        },
        "type": {
            "category": "OTP",
            "node": "ecd56eb1-28ff-4f9b-8a88-54336dfda9ea",
            "value": "OTP",
            "time": "2016-06-28T12:12:15.476958Z"
        },
        "dmed_o": {
            "category": "numeric",
            "node": "ceb77a6c-f5f4-45ed-9e95-ae60a02384e8",
            "value": 0.0,
            "time": "2016-06-28T12:15:38.282794Z"
        }
    },
    "exited_on": "2016-06-28T12:19:16.830654Z",
    "path": [
        {
            "node": "43943e8d-0403-4649-87f6-286778fd9e0d",
            "time": "2016-06-28T12:09:28.005824Z"
        },
        {
            "node": "17449ec7-7390-4605-b3a9-39438849119a",
            "time": "2016-06-28T12:09:28.174900Z"
        },
        {
            "node": "112b23e2-6e60-4f14-bc55-53c069f31250",
            "time": "2016-06-28T12:12:15.098503Z"
        },
        {
            "node": "ecd56eb1-28ff-4f9b-8a88-54336dfda9ea",
            "time": "2016-06-28T12:12:15.358533Z"
        },
        {
            "node": "dfdde2e9-1856-49c0-8f4a-6f7c4cac187e",
            "time": "2016-06-28T12:12:15.495990Z"
        },
        {
            "node": "2afcda2d-b90a-4caf-83a1-71a223c63082",
            "time": "2016-06-28T12:12:15.704045Z"
        },
        {
            "node": "fce56473-f815-483d-8af8-8aae82ee0c9e",
            "time": "2016-06-28T12:12:50.787910Z"
        },
        {
            "node": "e7d96279-b9fb-4ed6-8d0f-85fca4ed272d",
            "time": "2016-06-28T12:12:51.225428Z"
        },
        {
            "node": "cf3761e7-00c6-45e5-9d6b-9c9a47096a9d",
            "time": "2016-06-28T12:14:08.452380Z"
        },
        {
            "node": "a42e4631-f17d-460a-9605-98611c376ed5",
            "time": "2016-06-28T12:14:08.656661Z"
        },
        {
            "node": "b38e6f55-4035-4fde-8e0e-fbf6cc3901da",
            "time": "2016-06-28T12:14:39.335713Z"
        },
        {
            "node": "8a235d64-a25b-4587-8ee0-c7f77d7ebbb4",
            "time": "2016-06-28T12:14:39.502191Z"
        },
        {
            "node": "d13df39f-848c-4687-80d9-8f0c6d433a53",
            "time": "2016-06-28T12:14:56.516750Z"
        },
        {
            "node": "8a405d35-4717-48de-8c51-061c99d467fb",
            "time": "2016-06-28T12:14:57.152357Z"
        },
        {
            "node": "d628ffcc-e2e7-493b-a600-9ae6aeff72cd",
            "time": "2016-06-28T12:15:13.742974Z"
        },
        {
            "node": "ceb77a6c-f5f4-45ed-9e95-ae60a02384e8",
            "time": "2016-06-28T12:15:13.962799Z"
        },
        {
            "node": "4db21a6f-e86a-4e21-8524-90e927fd98ee",
            "time": "2016-06-28T12:15:38.295632Z"
        },
        {
            "node": "080391f8-79c6-4ee8-8c4c-217295d0c3c0",
            "time": "2016-06-28T12:15:38.511833Z"
        },
        {
            "node": "e915aab8-13e3-491d-a36a-292d4ba35aa8",
            "time": "2016-06-28T12:16:00.683741Z"
        },
        {
            "node": "1e7b41ad-745b-450b-b373-1cbd5846ca16",
            "time": "2016-06-28T12:16:00.997993Z"
        },
        {
            "node": "0edd1076-fb93-44ba-909f-91bd8a9898da",
            "time": "2016-06-28T12:19:16.091253Z"
        },
        {
            "node": "9e71a65a-1d5e-4757-8f40-b51a5c1becdc",
            "time": "2016-06-28T12:19:16.283309Z"
        },
        {
            "node": "05809541-e3e6-44e6-9f19-939a8071ed7f",
            "time": "2016-06-28T12:19:16.409308Z"
        }
    ],
    "flow": {
        "name": "IMAM Program",
        "uuid": "a9eed2f3-a92c-48dd-aa10-4f139b1171a4"
    },
    "id": 275389835,
    "exit_type": "completed",
    "responded": True
}

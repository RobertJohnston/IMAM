# coding: utf-8
from temba_client.v2 import TembaClient
client = TembaClient('rapidpro.io', open('token').read())
client.get_flows()
list(client.get_flows())
a = client.get_flows().iterfetches()
a
list(a)
client = TembaClient('rapidpro.io', open('token').read().strip())
a = client.get_flows().iterfetches()
list(a)
flows = _
flows
f=flows[0]
f
f = flows[0]
f
f = flows[0]
f
flows
f = flows[0][0]
f
f.name
[x.name for x flows[0]]
[x.name for x in flows[0]]
f
f.Runs
get_ipython().magic(u'pinfo f.Runs')
get_ipython().magic(u'pinfo f.runs')
f.runs
f.Runs
f.Runs.active
{x.name for x in flows[0]}
{x.name: x for x in flows[0]}
{x.name: x for x in flows[0]}[u'IMAM Program']
f = {x.name: x for x in flows[0]}[u'IMAM Program']
f.runs
f.Runs == f.runs
f.Runs.active
get_ipython().magic(u'pinfo f.Runs.active')
f.Runs.active()
f.Runs.active
f.Runs.active.deserialize
f.Runs.active.deserialize()
f.Runs.active.src
f.Runs.active.optional
f.Runs.active
f.runs.completed
f.runs.active
f.runs.create
a
client
client.get_runs
get_ipython().magic(u'pinfo client.get_runs')
f
f.uuid
client.get_runs(flow=f)
r = client.get_runs(flow=f).iterfetches()
r
r.next()
runs = _
run = runs[0]
run
run.values()
run.values
run.contact
run.contact.uuid
run
run.path
run.responded
run.Value
run.Value.category
run[]
run['']
run.values
run.values['amar_o']
amar = run.values['amar_o']
amar.value
amar.category
amar.node
amar.deserialize
get_ipython().magic(u'pinfo amar.deserialize')
amar.time
run.exit_type
run.contact
client.get_contacts()
client.get_contacts(group='Nut Personnel').iterfetches(retry_on_rate_exceed=True).next()
contacts = _
contact = contacts[0]
contact.fields
contact.fields
contact.uuid
contact.urns
contact.name
contact.groups
contact.groups[0].name
[x.name for x in contact.groups]
contact.fields
contact['siteid']
contact.modified_on
contact.blocked
contact.created_on
contact.stopped
[x.modified_on for x in contacts]
contact.created_on
contact.fields
from uuid import UUID
contact.uuid
UUID(contact.uuid)
len(contact.uuid)
client.get_contacts(group='Nut Personnel')
client.get_contacts(group='Nut Personnel').count
z = client.get_contacts(group='Nut Personnel')
z.params
z.url
run
run.fields
run.value
run.values
run.values
run.values['amar_o']
w = run.values['amar_o']
w.value
w.category
w.value
get_ipython().magic(u'pinfo w.deserialize')
get_ipython().magic(u'pinfo2 w')
w.value
w.time

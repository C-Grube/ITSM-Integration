#!/usr/bin/env python3

import requests
import json

# ------------------------------------------------------------------------------------------------------------
# Setup Variables For The Creation Of The Ticket
# ------------------------------------------------------------------------------------------------------------

customer_name_for_ticket = '[CUSTOMER NAME]'
ticket_status = 'New'
incident_type = 'Incident'
ticket_short_description = '[TICKET SHORT DESCRIPTION]'
ticket_description = '[TICKET DESCRIPTION]'
owned_by_team = '[TICKET TEAM OWNER]'
service = '[SERVICE NAME]]'
category = '[CATEGORY]'
subcategory = '[SUBCATEGORY]'
priority = '[PRIORITY]'

# ------------------------------------------------------------------------------------------------------------
# Authentication
# ------------------------------------------------------------------------------------------------------------

# Setting global login variables
base_uri = '[BASE URI]'
api_key = '[API KEY]'
username = '[USERNAME]'
password = '[PASSWORD]'


# Returns an access token
def get_access_token():
    token_uri = base_uri + 'token'
    auth_mode = 'Internal'
    data = {
        'Accept': 'application/json',
        'grant_type': 'password',
        'client_id': api_key,
        'username': username,
        'password': password,
        }
    access_token = json.loads(requests.post(url=token_uri,
                              data=data).content)['access_token']
    return access_token


# ------------------------------------------------------------------------------------------------------------
# Getting Template For The Incident Buisness Object & Creating New Incident Ticket
# ------------------------------------------------------------------------------------------------------------

# Returns the objectID for the incident buisness object
def get_buisness_object_summary_incident(access_token):
    summary_uri = base_uri \
        + 'api/V1/getbusinessobjectsummary/busobname/Incident'
    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-Type': 'application/json'}
    r = requests.get(summary_uri, headers=headers)
    incident_buisness_object_id = json.loads(r.content)[0]['busObId']
    return incident_buisness_object_id


# Returns the template for the indicent buiness object
def request_for_buisness_object_template(access_token,
        incident_buisness_object_id):
    template_uri = base_uri + 'api/V1/GetBusinessObjectTemplate'
    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-Type': 'application/json'}
    template_request = \
        json.dumps({'busObId': incident_buisness_object_id,
                   'includedRequired': 'True', 'includeAll': 'True'})
    r = requests.post(template_uri, headers=headers,
                      data=template_request)
    incident_buisness_object_template = r.content
    return json.loads(incident_buisness_object_template)


# Fills out the fields in the indicent buisness object
def fill_fields(access_token, incident_buisness_object_template):
    field_dict = {
        'CustomerVUnetID': customer_name_for_ticket,
        'Status': ticket_status,
        'Description': ticket_description,
        'ShortDescription': ticket_short_description,
        'Source': 'Phone',
        'IncidentType': incident_type,
        'OwnedByTeamLock': 'True',
        'OwnedByTeam': owned_by_team,
        'Service': service,
        'Category': category,
        'Subcategory': subcategory,
        'Priority': priority,
        'PriorityLock': 'True',
        }

    for field in incident_buisness_object_template['fields']:
        if field['name'] in field_dict.keys():
            field['dirty'] = 'true'
            field['value'] = field_dict[field['name']]

    prepared_template = incident_buisness_object_template['fields']
    return prepared_template


# ------------------------------------------------------------------------------------------------------------
# Creating The Ticket
# ------------------------------------------------------------------------------------------------------------

# Creates a new ticket using the newly generated incient buisness object
def create_new_buisness_object(access_token, prepared_template,
                               incident_buisness_object_id):
    create_buisness_object_uri = base_uri + 'api/V1/SaveBusinessObject'
    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-Type': 'application/json'}
    create_buisness_object_request = \
        json.dumps({'busObId': incident_buisness_object_id,
                   'fields': prepared_template})
    r = requests.post(create_buisness_object_uri, headers=headers,
                      data=create_buisness_object_request)


# ------------------------------------------------------------------------------------------------------------
# Main Function Begins Here
# ------------------------------------------------------------------------------------------------------------

def main():
    access_token = get_access_token()
    incident_buisness_object_id = get_buisness_object_summary_incident(access_token)
    incident_buisness_object_template = request_for_buisness_object_template(access_token, incident_buisness_object_id)
    prepared_template = fill_fields(access_token, incident_buisness_object_template)
    create_new_buisness_object(access_token, prepared_template, incident_buisness_object_id)


if __name__ == '__main__':
    main()
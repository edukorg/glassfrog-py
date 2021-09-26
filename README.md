![Github CI](https://github.com/edukorg/glassfrog-py/workflows/Github%20CI/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/616db0cff952ea5c8a6a/maintainability)](https://codeclimate.com/github/edukorg/glassfrog-py/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/616db0cff952ea5c8a6a/test_coverage)](https://codeclimate.com/github/edukorg/glassfrog-py/test_coverage)
[![python](https://img.shields.io/badge/python-3.8-blue.svg)]()

# Glassfrog API Client

Friendly client to navigate in [Glassfrog's API](https://documenter.getpostman.com/view/1014385/glassfrog-api-v3/2SJViY)

### Setup

- Install with: ``pip install glassfrog``
- Add your [API token](https://support.glassfrog.com/support/solutions/articles/9000066846-how-do-i-get-api-keys-) to the environment variable `GLASSFROG_API_TOKEN`

## Usage

All supported models have 2 methods that can be used to locate resources:
- `.get(id: int)` fetches the resource given its ID
- `.list()` iterates over all known resources

Most models also have attributes to help navigate through related resources, such as fetching all roles from a circle.

Here's an example of exploration:

```
from glassfrog import models

for circle in models.Circles.list():  # fetch all circles from the organization
  print(circle.name)
  
  for role in circle.roles:  # fetch all roles from a each circle
    print(role.purpose)
    
    for people in role.people:  # fetch all people that are assigned to each role
      print(people.name)
```


## Models

### Circle
 
 - **Can be listed?**: YES
 - **Attributes**: name, short_name, strategy
 - **Linked Resources**: organization, roles, policies, domains, supported_role

### Person
 
 - **Can be listed?**: YES
 - **Attributes**: name, email
 - **Linked Resources**: organizations, circles, assignments

### Role
 
 - **Can be listed?**: YES
 - **Attributes**: name, short_name, is_core, purpose, elected_until
 - **Linked Resources**: organization, circle, supporting_circle, domains, accountabilities, people, assignments

### Assignments

 - **Can be listed?**: YES
 - **Attributes**: focus, election, exclude_from_meetings
 - **Linked Resources**: person, role

### Organization
  
 - **Can be listed?**: NO
 - **Attributes**: description

### Policy

 - **Can be listed?**: NO
 - **Attributes**: title, body

### Accountability
 
 - **Can be listed?**: NO
 - **Attributes**: description

### Project
 
 - **Can be listed?**: NO
 - **Attributes**: created_at, archived_at, description, status, waiting_on_who, waiting_on_what, value, effort, roi, private_to_circle
 - **Linked Resources**: circle, person, role

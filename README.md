# python-wfscript
A Python library for loading and executing wfscript methods

## Installation
Install python-wfscript `default` branch:
```bash
python -m pip install git+https://github.com/dylanbenden/python-wfscript.git
```

Install python-wfscript `v2.0` release/tag:
```bash
python -m pip install git+https://github.com/dylanbenden/python-wfscript.git@v0.2
``` 
or, e.g
```bash
pipenv install git+https://github.com/dylanbenden/python-wfscript.git@v0.2#egg=python-wfscript
```

## Example
```yaml
- !INPUT
  first_name: !Validator core/specs::requried_string
  last_name: !Validator core/specs::required_string

- !BODY
  - !Action
    - !IDENTITY hr/data::add_employee==production
    - !INPUT
      first_name: !Input first_name
      last_name: !Input last_name
    - !OUTPUT
      - !State
        employee_id: !Output employee.employee_id
  - !Method
    - !IDENTITY it/users::provision_new_user==production
    - !INPUT
      first_name: !Input first_name
      last_name: !Input last_name
    - !OUTPUT
      - !State
        new_employee_email: !Output email

- !OUTPUT
  new_user:
    first_name: !Input first_name
    last_name: !Input last_name
    email: !State new_employee_email
    employee_id: !State new_employee_id

```
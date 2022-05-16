from ....names.decorators import action_identity


@action_identity('content_root/executing::add_prospect==production')
def add_prospect_1_0(first_name, last_name, email):
    # pretend to add a record
    return f'{first_name.lower()}.{last_name.lower()}'

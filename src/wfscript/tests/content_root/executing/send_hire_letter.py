from ....names.decorators import action_identity


@action_identity('content_root/executing::send_hire_letter==production')
def send_hire_letter_1_0(first_name, last_name, email):
    # pretend to send a hire letter, simulate generation of a unique code
    return f'CODE-98765'

from ....names.decorators import action_identity


@action_identity('content_root/executing::accept_offer==production')
def accept_offer_1_0(user_name, acceptance_code_generated, acceptance_code_provided):
    if acceptance_code_generated == acceptance_code_provided:
        return f'User {user_name} has successfully accepted their offer'
    else:
        return f'User {user_name} provided an incorrect acceptance code'

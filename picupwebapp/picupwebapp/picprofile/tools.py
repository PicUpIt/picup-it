from hashlib import md5

def get_gravatar_url(email):
    gravatar_base = 'https://www.gravatar.com/avatar/'
    gravatar_email = md5(email.lower()).hexdigest()
    gravatar_query = '{0}{1}'.format(gravatar_base, gravatar_email)
    return gravatar_query
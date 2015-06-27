from picupwebapp.picprofile.models import get_or_create_profile
from tools import get_gravatar_url

def picup_profile(request):
	"""Picup profile context processor.
	
	Note
	----
	Adds gravatar url and few other other variables.
	"""
	user = request.user
	result = {}
	if user.is_authenticated():
		result['gravatar_url'] = get_gravatar_url(user.email)
		result['auth_picup_profile'] = get_or_create_profile(user)
	else:
		result['auth_picup_profile'] = None
	return result

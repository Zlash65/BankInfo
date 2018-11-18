from django.shortcuts import redirect

def home_redirect(request):
	''' redirect to home route '''
	return redirect('/bank/')
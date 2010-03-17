from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from model_forms import AdminUserForm

def get_error_message(request):
    '''get_error_message returns the current error message in session (if it
    exists) only once, after that it is destroyed'''
    error_message = request.session.get('error_message', None)
    request.session['error_message'] = None
    return error_message

def manager_login_required(f):
    '''Wrapper for views that require the user to be authenticated as a
    manager. If not, they are sent to the login manager page with an error
    We also store the url they were attempting to enter so we can redirect
    them there after the login process'''
    def wrap(request, *args, **kwargs):
        if 'manager' not in request.session.keys():
            request.session['error_message'] = 'Please login to the page'
            request.session['last_url_before_redirect'] = request.META.get('HTTP_REFERER', '/catalog/manager/')
            return HttpResponseRedirect('/catalog/manager/login')
        else:
            return f(request, *args, **kwargs)
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

@manager_login_required
def index(request):
    '''Welcome page of the manager site'''
    return render_to_response('manager/index.html',
        { 
            'username': request.session.get('manager', ''),
            'error_message': get_error_message(request),
        }
    )
    
def manager_login(request):
    '''Login site for managers, shows form with GET requests, processes them 
    with POST. Everything is pretty standard'''
    
    if request.method == 'POST':
        login_form = AdminUserForm(request.POST)
        if login_form.is_valid():
            # Get an instance of the model without sending it to the db
            admin_user = login_form.save(commit = False) 
            if admin_user.validate_user():
                request.session['manager'] = admin_user.username
                return HttpResponseRedirect(request.session.get('last_url_before_redirect', '/catalog/manager'))
            else:
                request.session['error_message'] = 'Invalid user/password combination'
    else:
        # If the user is already logged in as a manager, block the request
        if 'manager' in request.session.keys():
            request.session['error_message'] = 'Cannot login again, please logout first'
            return HttpResponseRedirect(request.session.get('last_url_before_redirect', '/catalog/manager'))
            
        login_form = AdminUserForm()
        
    return render_to_response('manager/login.html', 
        {
            'error_message': get_error_message(request),
            'form': login_form
        }
    )

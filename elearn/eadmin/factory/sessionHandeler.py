from datetime import datetime
# clears session
def clearSession(request):
    request.session["isLoggedIn"] = False
    request.session["username"] = ""
    request.session["name"] = ""
    request.session["accessLevel"] = ""
    request.session["loggedInTime"] = ""
    request.session["activeTime"] = ""
    
# renew active time 
def renewSession(request):
    request.session["activeTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# check if request is valid
def requestIsValid(request):
    if not request.session.get("isLoggedIn"):
        clearSession(request)
        return False
    thatTime = datetime.strptime(request.session.get("activeTime"), '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - thatTime).seconds > 60*60: #10 minutes in seconds
        clearSession(request)
        return False
    renewSession(request)
    return True
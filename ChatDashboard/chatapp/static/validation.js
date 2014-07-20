function validatePassword(password) {
    var passpattern = /^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$/;
    var pos = 0;

    pos = password.search(passpattern);

    if (pos === -1) {
        return false;
    }
	return true;

}

function validateEmail(email) {
    //var passpattern = /[^@]+@[^@]+\.[^@]+/;///^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var emailpattern = ^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$;
    var pos = 0;

    pos = email.search(emailpattern);

    if (pos === -1) {
        return false;
    }
	return true;

}
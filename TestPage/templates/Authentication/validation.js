function validatePassword(password) {
    var passpattern = /^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$/;
    var pos = 0;

    pos = password.search(passpattern);

    if (pos === -1) {
        return false;
    }

}

function validateEmail(email) {
    var passpattern = /[^@]+@[^@]+\.[^@]+/;///^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var pos = 0;

    pos = email.search(passpattern);

    if (pos === -1) {
        return false;
    }

}
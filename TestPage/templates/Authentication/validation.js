function validatePassword(password) {
    var passpattern = /^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$/;
    var pos = 0;

    pos = password.search(passpattern);

    if (pos === -1) {
        return false;
    }

}
from util.users_validation import UsersValidation


def test_username_length():
    assert (
        not UsersValidation()
        .are_username_and_password_valid("verylooooooongnameeeeeeeeeeee", "password")
        .is_valid()
    )
    assert (
        not UsersValidation().are_username_and_password_valid("", "password").is_valid()
    )


def test_incorrect_username():
    assert (
        not UsersValidation()
        .are_username_and_password_valid("#us)er!", "password")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user!", "password")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid(" user123", "password")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123 ", "password")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("  user  ", "password")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("    ", "password")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("!?%1", "password")
        .is_valid()
    )


def test_correct_username():
    assert (
        UsersValidation()
        .are_username_and_password_valid("user", "Correct1Pass!")
        .is_valid()
    )
    assert (
        UsersValidation()
        .are_username_and_password_valid("123", "Correct1Pass!")
        .is_valid()
    )
    assert (
        UsersValidation()
        .are_username_and_password_valid("user123", "Correct1Pass!")
        .is_valid()
    )
    assert (
        UsersValidation()
        .are_username_and_password_valid("ThisNameContains20ch", "Correct1Pass!")
        .is_valid()
    )


def test_password_length():
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "toosmall")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "tooooooooooooooooobiiiiiiiiiiig")
        .is_valid()
    )


def test_incorrect_password():
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "password")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "password1")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "password!")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "Password")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "PASSWORD")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "Password1")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "Password!")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "Pass!1#")
        .is_valid()
    )
    assert (
        not UsersValidation()
        .are_username_and_password_valid("user123", "Pass1word.")
        .is_valid()
    )


def test_correct_password():
    assert (
        UsersValidation()
        .are_username_and_password_valid("user123", "!Q1w2e3r4")
        .is_valid()
    )
    assert (
        UsersValidation()
        .are_username_and_password_valid("user123", "#Qwerty1")
        .is_valid()
    )
    assert (
        UsersValidation()
        .are_username_and_password_valid("user123", "Pass1!  ")
        .is_valid()
    )
    assert (
        UsersValidation()
        .are_username_and_password_valid("user123", "  Pp1$  ")
        .is_valid()
    )

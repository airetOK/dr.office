import re


class UsersValidationOutput:
    def __init__(self, message="", is_valid=True):
        self.__message = message
        self.__is_valid = is_valid

    def get_message(self) -> str:
        return self.__message

    def is_valid(self) -> bool:
        return self.__is_valid


class UsersValidation:
    def are_username_and_password_valid(
        self, username: str, password: str
    ) -> UsersValidationOutput:
        if len(username) not in range(1, 21):
            return UsersValidationOutput(
                """Юзернейм має бути
                не довше 20 літер""",
                False,
            )

        if len(password) not in range(8, 21):
            return UsersValidationOutput(
                """Пароль має бути не менше за 8
                літер та довше ніж 20 літер""",
                False,
            )

        if re.fullmatch("[A-Za-z0-9]{1,20}", username) is None:
            return UsersValidationOutput(
                """Юзернейм має складатись з
                латинських літер або цифр""",
                False,
            )

        if (
            re.fullmatch(
                "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$",
                password,
            )
            is None
        ):
            return UsersValidationOutput(
                """Пароль має містити принаймні одну велику англійську літеру,
                                        принаймні одну малу англійську літеру,
                                        принаймні одну цифру,
                                        принаймні один символ""",
                False,
            )

        return UsersValidationOutput()

class LanguageService:

    LANGUAGES = {
        'Англійська': 'gbr',
        'Польська': 'pol',
        'Українська': 'ukr'
    }

    def get_svg_name_by_language(self, language: str):
        return self.LANGUAGES.get(language, 'unknown')

    def get_language_names(self):
        return self.LANGUAGES.keys()
LANGUAGES = {
    'Англійська': 'gbr',
    'Польська': 'pol',
    'Українська': 'ukr'
}

def get_svg_name_by_language(language: str):
    return LANGUAGES.get(language, 'unknown')

def get_language_names():
    return LANGUAGES.keys()
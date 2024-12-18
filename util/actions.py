actions_by_language = {
        'ua': [
            'Анестезія',
            'Видалення зуба',
            'Відбілювання',
            'Встановлення брекетів на верхній щелепі',
            'Встановлення брекетів на нижній щелепі',
            'Встановлення самолігатурних брекетів',
            'Вторинне ендо (ліки)',
            'Вторинне ендо (пломбування)',
            'Герметизація',
            'Заміна дуги на верхній щелепі',
            'Заміна дуги на нижній щелепі',
            'Заміна резинок на верхній щелепі',
            'Заміна резинок на нижній щелепі',
            'Зняття відбитків (альгінат)',
            'Зняття відбитків (A-силікон)',
            'Зняття відбитків (C-силікон)',
            'Кальцій',
            'Консультація',
            'Корекція реставрації',
            'Кофердам',
            'МТА',
            'Не прийшов',
            'Первинне ендо (ліки)',
            'Первинне ендо (пломбування)',
            'Препарування під коронку',
            'Професійна гігієна',
            'Реставрація зуба',
            'РТГ',
            'Скловолоконний штифт',
            'Фіксація к/к вкладки',
            'Фіксація м/к коронки',
            'Фіксація цирконієвої коронки',
            'Флюоризація'
        ]
}

def get_actions_by_language(lang: str='ua'):
    return actions_by_language.get(lang)
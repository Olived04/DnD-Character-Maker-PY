import easygui as eg
import pprint

attributes = [
    "Class",
]

ability_scores = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma"
]

skills = {
    "Acrobatics": "Dexterity",
    "Animal Handling": "Wisdom",
    "Arcana": "Intelligence",
    "Athletics": "Strength",
    "Deception": "Charisma",
    "History": "Intelligence",
    "Insight": "Wisdom",
    "Intimidation": "Charisma",
    "Investigation": "Intelligence",
    "Medicine": "Wisdom",
    "Nature": "Intelligence",
    "Perception": "Wisdom",
    "Performance": "Charisma",
    "Persuasion": "Charisma",
    "Religion": "Intelligence",
    "Sleight of Hand": "Dexterity",
    "Stealth": "Dexterity",
    "Survival": "Wisdom",
}


def get_intput(name, category_name, category_list):
    character[name][category_name] = {}
    for attr in category_list:
        value = eg.integerbox(f"What is your {attr}?")
        character[name][category_name][attr] = value


def skill_calc(name):
    character[name]["Skills"] = {}
    for skill, ability in skills.items():
        ability_score = character[name]["Ability scores"][ability]
        modifier = (ability_score - 10) // 2
        character[name]["Skills"][skill] = modifier


def search():
    while True:
        choice_list = list(character.keys())

        if len(choice_list) == 1:
            choice_list = choice_list * 2

        char_name = eg.choicebox("Would you like to view a character"
                                  " or change their name"
                                  " or an attribute in this list?",
                         choices=choice_list)

        if char_name is None:
            return None

        change = eg.ynbox(f"Their current name is {char_name}."
                          "\nWould you like to change it?")
        if change:
            new_value = eg.enterbox("What would you like their new name to be?")
            if new_value:
                character[new_value] = character.pop(char_name)
                char_name = new_value

        choice_list = list(character[char_name].keys())
        choice = eg.choicebox("Would you like to view an attribute"
                              " and or edit an attribute in this list?",
                     choices=choice_list)

        if choice == "Skills":
            choice_list = list(character[char_name]["Skills"].keys())
            choice = eg.choicebox("Would you like to view and or"
                                  " change a value in this list?",
                     choices=choice_list)
            output = character[char_name]["Skills"][choice]
            change = eg.ynbox(f"Your skill for {choice} is {output}"
                              "\n Would you like to change it?")
            if change:
                new_value = eg.integerbox("What would you like to change it to?")
                character[char_name]["Skills"][choice] = new_value

        elif choice == "Ability scores":
            choice_list = list(character[char_name]["Ability scores"].keys())
            choice = eg.choicebox("Would you like to view and or"
                                  " change a value in this list?",
                     choices=choice_list)
            output = character[char_name]["Ability scores"][choice]
            eg.ynbox(f"Your ability score {choice} is {output}"
                     "\n Would you like to change it?")
            if change:
                new_value = eg.integerbox("What would you like to change it to?")
                character[char_name]["Ability scores"][choice] = new_value

        else:
            output = character[char_name][choice]
            change = eg.ynbox(f"Your {choice} is {output}"
                                "\n Would you like to change it?")
            if change:
                new_value = eg.enterbox("What would you like to change it to?")
                character[char_name][choice] = new_value

        again = eg.ynbox("Would you like to change or see more attributes?")
        if not again:
            break

    return char_name


character = {}

while True:
    name = eg.enterbox("What is your character's name?")
    character[name] = {}

    for attr in attributes:
        value = eg.enterbox(f"What is your {attr}?")
        character[name][attr] = value

    get_intput(name, "Ability scores", ability_scores)
    skill_calc(name)

    while True:
        again = eg.ynbox("Would you like to edit or view one of your values?")
        if again == False:
            break
        new_name = search()
        if new_name is None:
            continue
        else:
            name = new_name
        skill_calc(name)

    while True:
        remove = eg.ynbox("Would you like to remove a character?")
        if remove == True:
            try:
                char_remove = eg.choicebox("What character would you like to remove?",
                         choices=list(character.keys()))
            except ValueError:
                eg.msgbox("You can't remove a character if you only have 1")
                break
            sure = eg.ynbox("Are you sure you want to remove this character?")
            if sure == True:
                character.pop(char_remove)
            else:
                break
        else:
            break
    again = eg.ynbox("Would you like to add another character?")
    if again == False:
        break

pprint.pprint(character, sort_dicts=False)

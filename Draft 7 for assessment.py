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


def get_intput(category_name, category_list):
    character[name][category_name] = {}
    for attr in category_list:
        value = eg.integerbox(f"What is your {attr}?")
        character[name][category_name][attr] = value

def skill_calc():
    character[name]["Skills"] = {}
    for skill, ability in skills.items():
        ability_score = character[name]["Ability scores"][ability]
        print(ability_score)
        modifier = (ability_score - 10) // 2
        character[name]["Skills"][skill] = modifier

def search():
    choice_list = character
    choice = eg.choicebox("Would you like to view a character or change their name"
                          " or an attribute in this list?",
                 choices=choice_list)
    change = eg.ynbox("Would you like to change their name?")
    if change == True:
        new_value = eg.enterbox("What would you like it to be?")
        character[name] = new_value
        
    if choice == "Skills":
        choice_list = character[name]["Skills"]
        choice = eg.choicebox("Would you like to view and or"
                              " change a value in this list?",
                 choices=choice_list)
        output = character[name]["Skills"][choice]
        change = eg.ynbox(f"Your skill for {choice} is {output}",
                          "\n Would you like to change it?")
        if change == True:
            new_value = eg.integerbox("What would you like to change it to?")
            character[name]["Skills"][choice] = new_value
            
    elif choice == "Ability scores":
        choice_list = character[name]["Ability scores"]
        choice = eg.choicebox("Would you like to view and or"
                              " change a value in this list?",
                 choices=choice_list)
        output = character[name]["Ability scores"][choice]
        eg.ynbox(f"Your ability score {choice} is {output}",
                 "\n Would you like to change it?")
        if change == True:
            new_value = eg.integerbox("What would you like to change it to?")
            character[name]["Ability scores"][choice] = new_value
        
    else:
        new_value = eg.enterbox("What would you like to change it to?")
        character[name][choice] = new_value

character = {}

while True:
    name = eg.enterbox("What is your characters name?")
    character[name] = {}

    for attr in attributes:
        value = eg.enterbox(f"What is your {attr}?")
        character[name][attr] = value
        

    get_intput("Ability scores", ability_scores)
    skill_calc()
    while True:
        again = eg.ynbox("Would you like to edit or view one of your values?")
        if again == False:
            break
        search()
        skill_calc()
    while True:
        remove = eg.ynbox("Would you like to remove a character?")
        if remove == True:
            choice_list = character
            try:
                char_remove = eg.choicebox("What character would you like to remove?",
                         choices=choice_list)
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

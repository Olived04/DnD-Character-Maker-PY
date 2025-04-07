import easygui as eg
character = {}

name = eg.enterbox("What is your characters name?")
character[name] = {}

attributes = [
    "Class: ",
    "Level: ",
    "Race: ",
    "Proficiency Bonus: ",
    "Hit Points: ",
    "Armour Class: ",
    "Attacks: "
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
        
for attr in attributes:
    value = eg.enterbox(f"What is your {attr}?")
    character[name][attr] = value
    
get_intput("Ability scores", ability_scores)

print(character)

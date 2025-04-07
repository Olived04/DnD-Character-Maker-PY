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


#example of a function and what it will do
def get_intput(category_name, category_list):
    character[name][category_name] = {}
    for attr in category_list:
        value = eg.integerbox(f"What is your {attr}?")
        character[name][category_name][attr] = value

def skill_calc():
    character[name]["skills"] = {}
    for skill, ability in skills.items():
        ability_score = character[name]["Ability scores"][ability]
        print(ability_score)
        modifier = (ability_score - 10) // 2
        character[name]["skills"][skill] = modifier
        
for attr in attributes:
    value = eg.enterbox(f"What is your {attr}?")
    character[name][attr] = value
    

get_intput("Ability scores", ability_scores)
print(character[name]["Ability scores"])
skill_calc()

print(character)

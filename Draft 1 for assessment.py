import easygui as eg
character = {}

name = eg.enterbox("What is your characters name?")
character[name] = {}

#example of a function and what it will do
def strinput(characters, name, attribute, value):
    if name not in characters:
        characters[name] = {}
    characters[name][attribute] = value
attribute = "COolness"
value = eg.enterbox("what is your character like?")
characters = {}
strinput(characters, name, attribute, value)

print(characters)

#Just a basic idea of how I want my dictionary to look
character = {
    name: {
        "Class": "",
        "Level": "",
        "Race": "",
        "Proficiency bonus": "",
        "Ability scores": {
            "Strength": "",
            "Dexterity": "",
            "Constitution": "",
            "Intelligence": "",
            "Wisdom": "",
            "Charisma": ""
            },
        "Skills":{#These can all be calculated using the ability score modifiers
            "Acrobatics": "",
            "Animal Handling": "",
            "Arcana": "",
            "Athletics": "",
            "Deception": "",
            "History": "",
            "Insight": "",
            "Intimidation": "",
            "Investigation": "",
            "Medicine": "",
            "Nature": "",
            "Perception": "",
            "Performance": "",
            "Persuasion": "",
            "Religion": "",
            "Sleight of Hand": "",
            "Stealth": "",
            "Survival": ""
            },
        "Hit Points": "",
        "Armour Class": "",
        "Attacks": ""}
    }


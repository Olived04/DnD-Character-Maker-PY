import easygui as eg  # GUI library for input boxes and message boxes
"""GUI library for input boxes and message boxes"""

# Basic character information fields
attributes = [
    "Class",
]

# Core D&D ability scores
ability_scores = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma"
]

# Mapping of each skill to the ability score it relies on
skills = {
    "Acrobatics": "Dexterity",
    "Animal Handling": "Wisdom",
    "Arcana": "Intelligence",
    "Athletics": "Strength",
    "Deception": "Charisma",
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

# Get input from the user for a category (e.g., Ability scores)
def get_input(name, category_name, category_list):
    character[name][category_name] = {}
    for attr in category_list:
        value = eg.integerbox(f"What is your {attr}?")  # Prompt user for score
        if value is None:
            return  # Cancelled
        character[name][category_name][attr] = value

# Calculate skill modifiers from associated ability scores
def skill_calc(name):
    character[name]["Skills"] = {}
    for skill, ability in skills.items():
        ability_score = character[name]["Ability scores"][ability]
        modifier = (ability_score - 10) // 2  # D&D formula for ability modifier
        character[name]["Skills"][skill] = modifier

# Function to edit a specific attribute inside a section (like a skill or ability score)
def search_category_edit(char_name, section_name):
    keys = list(character[char_name][section_name].keys())
    choice = eg.choicebox(f"Edit which {section_name}?", choices=keys)
    if choice is None:
        return
    current = character[char_name][section_name][choice]
    change = eg.ynbox(f"{choice} is currently {current}. Change it?")
    if change:
        new_val = eg.integerbox(f"Enter new value for {choice}:")
        if new_val is None:
            return
        character[char_name][section_name][choice] = new_val

# View or edit existing character data
def edit():
    if not character:
        eg.msgbox("No characters to edit.")
        return

    while True:
        choice_list = list(character.keys())

        if len(choice_list) == 1:
            choice_list = choice_list * 2  # Duplicate list if only 1 choice (easygui fix)

        char_name = eg.choicebox("Would you like to view a character"
                                 " or change their name"
                                 " or an attribute in this list?",
                                 choices=choice_list)
        if char_name is None:
            return

        # Rename character
        change = eg.ynbox(f"Their current name is {char_name}."
                          "\nWould you like to change it?")
        if change:
            new_value = eg.enterbox("What would you like their new name to be?")
            if new_value is None:
                return
            character[new_value] = character.pop(char_name)
            char_name = new_value

        # Choose an attribute to view or edit
        choice_list = list(character[char_name].keys())
        choice = eg.choicebox("Would you like to view or edit an attribute?",
                              choices=choice_list)
        if choice is None:
            return

        # Edit nested categories
        if choice == "Skills" or choice == "Ability scores":
            search_category_edit(char_name, choice)
        else:
            # View and edit simple values
            output = character[char_name][choice]
            change = eg.ynbox(f"Your {choice} is {output}\nWould you like to change it?")
            if change:
                new_value = eg.enterbox("What would you like to change it to?")
                if new_value is None:
                    continue
                character[char_name][choice] = new_value

        again = eg.ynbox("Would you like to change or see more attributes?")
        if not again:
            break

# Add a new character to the dictionary
def add_character(char_name):

    character[char_name] = {}

    # Prompt for each main attribute
    for attr in attributes:
        value = eg.enterbox(f"What is your {attr}?")
        if value is None:
            return
        character[char_name][attr] = value

    # Get ability scores and calculate derived skills
    get_input(char_name, "Ability scores", ability_scores)
    skill_calc(char_name)
    view_full_character(char_name)
    correct = eg.ynbox("Was that information correct?")
    if correct == False:
        edit()
    

# Delete a character from the dictionary
def remove_character():
    if len(character) <= 1:
        eg.msgbox("You can't remove a character if you have only 1 or none.")
        return

    char_remove = eg.choicebox("What character would you like to remove?",
                               choices=list(character.keys()))
    if char_remove is None:
        return

    sure = eg.ynbox("Are you sure you want to remove this character?")
    if sure:
        character.pop(char_remove)

# View attributes of a selected character
def search():
    if not character:
        eg.msgbox("No characters to search.")
        return

    while True:
        choice_list = list(character.keys())

        if len(choice_list) == 1:
            choice_list = choice_list * 2  # Duplicate to avoid easygui bug

        char_name = eg.choicebox("What character would you like to view?",
                                 choices=choice_list)
        if char_name is None:
            return

        choice_list = list(character[char_name].keys())
        choice = eg.choicebox("Which attribute would you like to view?",
                              choices=choice_list)
        if choice is None:
            return

        if choice == "Skills" or choice == "Ability scores":
            search_category_edit(char_name, choice)
        else:
            output = character[char_name][choice]
            eg.msgbox(f"Your {choice} is {output}")

        again = eg.ynbox("Would you like to see more attributes?")
        if not again:
            break

# Output character data to the terminal
def print_character():
    print(character)
    if not character:
        print("No characters to display.")
        return
    for name in character:
        print(name)
        for attribute in character[name]:
            if attribute == "Ability scores":
                for attr in character[name]["Ability scores"]:
                    print(attr, ":", character[name]["Ability scores"][attr])
            elif attribute == "Skills":
                for attr in character[name]["Skills"]:
                    print(attr, ":", character[name]["Skills"][attr])
            else:
                print(attribute, ":", character[name][attribute])

def view_full_character(char_name):
    output = f"Name: {char_name}\n"
    for attribute, value in character[char_name].items():
        if attribute == "Ability scores":
            output += "Ability scores\n"
            for attr, val in character[char_name]["Ability scores"].items():
                output += f"    {attr}: {val}\n"
                
        elif attribute == "Skills":
            output += "Skills\n"
            for attr, val in character[char_name]["Skills"].items():
                output += f"    {attr}: {val}\n"
                
        else:
            output += f"{attribute}: {value}\n"
    eg.textbox(f"{char_name}'s stats", text=output)

# Main program loop with menu options
def main_menu():
    while True:
        choice_list = ["Add new character", "Edit characters", "Search characters",
                       "Remove character", "Print characters to shell",
                       "View full character", "Quit"]
        choice = eg.choicebox("Would you liketo...", choices=choice_list)

        if choice == "Add new character":
            char_name = eg.enterbox("What is your character's name?")
            if char_name is None:
                return
            add_character(char_name)
        elif choice == "Edit characters":
            edit()
        elif choice == "Search characters":
            search()
        elif choice == "Remove character":
            remove_character()
        elif choice == "Print characters to shell":
            print_character()
        elif choice == "View full character":
            choice_list = list(character.keys())
            if len(choice_list) == 1:
                choice_list = choice_list * 2  # Duplicate to avoid easygui bug
            char_name = eg.choicebox("What character would you like to view?",
                         choices=choice_list)
            view_full_character(char_name)
        else:
            break  # Exit the loop and end the program


# Initialize character dictionary with a sample character
character = {
    "Doug": {
        "Class": "Fighter",
        "Ability scores": {
            "Strength": 16,
            "Dexterity": 14,
            "Constitution": 15,
            "Intelligence": 12,
            "Wisdom": 12,
            "Charisma": 14
        },
        "Skills": {
            "Acrobatics": 2,
            "Animal Handling": 1,
            "Arcana": 1,
            "Athletics": 3,
            "Deception": 2,
            "History": 1,
            "Insight": 1,
            "Intimidation": 2,
            "Investigation": 1,
            "Medicine": 1,
            "Nature": 1,
            "Perception": 1,
            "Performance": 2,
            "Persuasion": 2,
            "Religion": 1,
            "Sleight of Hand": 2,
            "Stealth": 2,
            "Survival": 1
        }
    }
}

# Welcome message and launch menu
eg.msgbox("Welcome to Ollie's awesome character creator!")
main_menu()

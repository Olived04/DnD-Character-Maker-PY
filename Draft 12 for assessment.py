import easygui as eg
import pprint

# List of attributes for the character (used for general information)
attributes = [
    "Class",
]

# List of ability scores 
ability_scores = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma"
]

# A dictionary mapping each skill to the relevant ability score
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

# Function to get input for different categories
def get_input(name, category_name, category_list):
    character[name][category_name] = {}
    for attr in category_list:
        value = eg.integerbox(f"What is your {attr}?")
        if value is None:
            return  # Exit if user cancels
        character[name][category_name][attr] = value

# Function to calculate the modifiers for each skill based on ability scores
def skill_calc(name):
    character[name]["Skills"] = {}
    for skill, ability in skills.items():
        ability_score = character[name]["Ability scores"][ability]
        modifier = (ability_score - 10) // 2  # Standard formula for calculating modifiers
        character[name]["Skills"][skill] = modifier
    main_menu()

# Function to edit categories like Skills or Ability Scores
def search_category_edit(char_name, section_name):
    keys = list(character[char_name][section_name].keys())  # Get list of keys in the section
    choice = eg.choicebox(f"Edit which {section_name}?", choices=keys)  # Ask the user which to edit
    if choice is None:
        return  # Exit if user cancels
    current = character[char_name][section_name][choice]  # Get the current value of the selected attribute
    change = eg.ynbox(f"{choice} is currently {current}. Change it?")  # Ask user if they want to change it
    if change:
        new_val = eg.integerbox(f"Enter new value for {choice}:")  # Get the new value
        if new_val is None:
            return  # Exit if user cancels
        character[char_name][section_name][choice] = new_val  # Update the value
    main_menu()

# Function to search, edit, or view attributes for a character
def edit():
    while True:
        choice_list = list(character.keys())  # List of character names

        # If there's only one character, duplicate the list so it doesn't get stuck
        if len(choice_list) == 1:
            choice_list = choice_list * 2

        char_name = eg.choicebox("Would you like to view a character"
                                  " or change their name"
                                  " or an attribute in this list?",
                         choices=choice_list)  # Let user choose a character
        if char_name is None:
            return None  # Exit if user cancels

        # Ask if the user wants to change the character's name
        change = eg.ynbox(f"Their current name is {char_name}."
                          "\nWould you like to change it?")
        if change:
            new_value = eg.enterbox("What would you like their new name to be?")
            if new_value is None:
                return None  # Exit if user cancels
            character[new_value] = character.pop(char_name)  # Rename the character
            char_name = new_value

        # Ask which attribute they want to edit
        choice_list = list(character[char_name].keys())
        choice = eg.choicebox("Would you like to view an attribute"
                              " and or edit an attribute in this list?",
                     choices=choice_list)

        # If the choice is "Skills" or "Ability scores", let them edit those
        if choice == "Skills" or choice == "Ability scores":
            search_category_edit(char_name, choice)

        else:
            output = character[char_name][choice]  # Show current value of the chosen attribute
            change = eg.ynbox(f"Your {choice} is {output}"
                                "\n Would you like to change it?")  # Ask if user wants to change it
            if change:
                new_value = eg.enterbox("What would you like to change it to?")  # Get new value
                if new_value is None:
                    continue  # Continue if user cancels
                character[char_name][choice] = new_value  # Update the value

        # Ask if the user wants to view or edit more attributes
        again = eg.ynbox("Would you like to change or see more attributes?")
        if not again:
            break  # Break the loop if user is done

    return char_name
    main_menu()

def add_character():
    name = eg.enterbox("What is your character's name?")
    if name is None:
        return  # Exit if user cancels

    character[name] = {}  # Create a new dictionary for this character

    # Get the value for each attribute
    for attr in attributes:
        value = eg.enterbox(f"What is your {attr}?")
        if value is None:
            break  # Exit if user cancels
        character[name][attr] = value

    # Get ability scores and calculate skills
    get_input(name, "Ability scores", ability_scores)
    skill_calc(name)
    main_menu()

def remove_character():
    try:
        # Ask user which character to remove
        char_remove = eg.choicebox("What character would you like to remove?",
                      choices=list(character.keys()))
        if char_remove is None:
            return  # Exit if user cancels
    except ValueError:
        eg.msgbox("You can't remove a character if you only have 1")  # Handle error if only 1 character exists
        return
    sure = eg.ynbox("Are you sure you want to remove this character?")
    if sure == True:
        character.pop(char_remove)  # Remove the character from the list
    else:
        return
    main_menu()

def search():
    while True:
        choice_list = list(character.keys())  # List of character names

        # If there's only one character, duplicate the list so it doesn't get stuck
        if len(choice_list) == 1:
            choice_list = choice_list * 2

        char_name = eg.choicebox("What character would you like to view?",
                         choices=choice_list)  # Let user choose a character
        if char_name is None:
            return None  # Exit if user cancels
        
        choice_list = list(character[char_name].keys())
        choice = eg.choicebox("Which attribute would you like to view?",
                             choices=choice_list)

        # If the choice is "Skills" or "Ability scores", let them edit those
        if choice == "Skills" or choice == "Ability scores":
            search_category_edit(char_name, choice)

        else:
            output = character[char_name][choice]  # Show current value of the chosen attribute
            eg.msgbox(f"Your {choice} is {output}")

        # Ask if the user wants to view more attributes
        again = eg.ynbox("Would you like to see more attributes?")
        if not again:
            break  # Break the loop if user is done

    return char_name
    main_menu()

def print_character():
    for name in character:
        print(name)
        for attribute in character[name]:
            if attribute == "Ability scores":
                for attribute in character[name]["Ability scores"]:
                    print(attribute, ":", character[name]["Ability scores"][attribute])
            elif attribute == "Skills":
                for attribute in character[name]["Skills"]:
                    print(attribute, ":", character[name]["Skills"][attribute])
            else:
                print (attribute, ":", character[name][attribute])
    main_menu()

# Main character creation and modification loop
character = {}




# Main Menu loop
def main_menu():
    choice_list = ["Add new character", "Edit characters", "Search characters",
                   "Remove character", "Print characters to shell", "Quit"]
    choice = eg.choicebox("Would you like to...", choices=choice_list)

    if choice == "Add new character":
        add_character()
    elif choice == "Edit characters":
        edit()
    elif choice == "Search characters":
        search()
    elif choice == "Remove character":
        remove_character()
    elif choice == "Print characters to shell":
        print_character()
    else:
        quit()

eg.msgbox("Welcome to Ollies awesome character creator")
main_menu()

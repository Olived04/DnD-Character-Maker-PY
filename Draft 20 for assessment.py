"""GUI library for input boxes and message boxes."""
import easygui as eg  # Import easygui to create GUI dialogs

MAX_ABILITY_SCORE = 20  # Maximum allowed ability score (as string here)

# Main menu options presented to the user
MAIN_MENU_OPTIONS = [
    "Add new character", "Edit characters",
    "Search characters", "Remove character",
    "Print characters to shell",
    "View full character", "Add a new attribute", "Quit"
]

# Basic character attributes outside of ability scores
attributes = [
    "Class"
]

# Core D&D ability scores tracked for each character
ability_scores = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma"
]

# Mapping each skill to its governing ability score
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


def choose_character():
    """Show a choice dialog for the user to pick a character."""
    global char_name

    choice_list = list(character.keys())  # Get list of character names

    if len(choice_list) == 1:
        # If only one character, just show a button box with that character
        char_name = eg.buttonbox("Choose your character",
                                 title="Choose your character",
                                 choices=choice_list)
        # If user clicks button, default to first character in list
        if char_name:
            char_name = choice_list[0]
        else:
            return  # User cancelled
    else:
        # If multiple characters, show a choicebox (list selection)
        char_name = eg.choicebox("What character would you like to choose?",
                                 choices=choice_list,
                                 title="Choose your character")


def get_input(name, category_name, category_list):
    """
    Prompt the user to input integer values for a category of attributes.

    e.g. ability scores.
    Stores the results in the character dictionary.
    """
    character[name][category_name] = {}

    for attr in category_list:
        # Prompt user to input integer with upper bound 20
        value = eg.integerbox(f"What is your {attr}?",
                              title="Input values",
                              upperbound=MAX_ABILITY_SCORE)
        if value is None:
            return None  # User cancelled input, return None to signal this

        # Save the entered value in the character dict
        character[name][category_name][attr] = value

    return name  # Return character name on success


def skill_calc(name):
    """
    Calculate skill modifiers based on the character's ability scores.

    Modifier formula: (ability_score - 10) // 2
    Stores the modifiers in character[name]['Skills'].
    """
    character[name]["Skills"] = {}

    for skill, ability in skills.items():
        ability_score = character[name]["Ability scores"][ability]

        modifier = (ability_score - 10) // 2  # Standard D&D calculation

        character[name]["Skills"][skill] = modifier


def search_category_edit(char_name, section_name):
    """
    Allows user to select a key within a nested category.

    (like 'Skills' or 'Ability scores')
    and edit its value via GUI dialogs.
    """
    keys = list(character[char_name][section_name].keys())

    choice = eg.choicebox(f"Edit which {section_name}?", choices=keys,
                          title="Choose a value to edit")

    if choice is None:
        return  # User cancelled

    current = character[char_name][section_name][choice]

    change = eg.ynbox(f"{choice} is currently {current}. Change it?",
                      title="Change subvalue?")
    if change:
        new_val = eg.integerbox(f"Enter new value for {choice}:",
                                title="Enter new value")

        if new_val is None:
            return  # User cancelled

        character[char_name][section_name][choice] = new_val


def edit():
    """
    Allow the user to edit an existing character's name and attributes.

    Loops until user chooses to stop editing.
    """
    global char_name
    while True:
        choose_character()

        if char_name is None:
            break  # User cancelled character selection

        # Ask if user wants to rename the character
        change = eg.ynbox(f"Their current name is {char_name}."
                          "\nWould you like to change it?",
                          title="Change name?")
        if change:
            new_value = eg.enterbox("What would you like "
                                    "their new name to be?", title="New name")

            if new_value is None:
                return  # Cancelled rename
            # Rename character key in dictionary
            character[new_value] = character.pop(char_name)
            char_name = new_value

        choice_list = list(character[char_name].keys())

        # Ask which attribute to view or edit
        choice = eg.choicebox("Would you like to view or edit an attribute?",
                              choices=choice_list, title="Edit attribute?")
        if choice is None:
            return  # Cancelled attribute selection

        if choice == "Skills" or choice == "Ability scores":
            # For nested dictionaries, call the nested edit function
            search_category_edit(char_name, choice)

        else:
            # For simple attributes, show current value and allow editing
            output = character[char_name][choice]

            change = eg.ynbox(f"Your {choice} is {output}\nWould you like to"
                              " change it?", title="Change it?")

            if change:
                new_value = eg.enterbox("What would you like to change it to?",
                                        title="New value")

                if new_value is None:
                    return  # Cancelled
                character[char_name][choice] = new_value

        # Ask if user wants to edit more attributes
        again = eg.ynbox("Would you like to change or see more attributes?",
                         title="See more attributes?")
        if not again:
            break  # Exit edit loop


def add_character(char_name):
    """
    Create a new character with user-inputted basic attributes, ability scores.

    calculates skills automatically, then confirms correctness.
    """
    character[char_name] = {}

    for attr in attributes:
        # Ask user for each basic attribute (e.g. class)
        value = eg.enterbox(f"What is your {attr}?", title="Input attribute")

        if value:
            character[char_name][attr] = value

        else:
            # If user cancels, delete the new character and return
            del character[char_name]
            return

    # Prompt for ability scores; if cancelled, delete character and return
    if get_input(char_name, "Ability scores", ability_scores) is None:
        del character[char_name]
        return

    # Calculate skill modifiers based on input ability scores
    skill_calc(char_name)

    # Show the full character details for user confirmation
    view_full_character(char_name, "Double check your information please")

    # Ask if info was correct; if not, allow editing
    correct = eg.ynbox("Was that information correct?",
                       title="Would you like to edit?")

    if correct is False:
        edit()


def remove_character():
    """Remove a character after user selects and confirms."""
    if len(character) <= 1:
        # Prevent removing if only 1 or zero characters left
        eg.msgbox("You can't remove a character if you have only 1 or none.",
                  title="Pretty self explanatory")
        return

    char_remove = eg.choicebox("What character would you like to remove?",
                               choices=list(character.keys()),
                               title="Pick a character")
    if char_remove is None:
        return  # Cancelled

    sure = eg.ynbox("Are you sure you want to remove this character?",
                    title="Are you sure?")

    if sure:
        character.pop(char_remove)  # Remove character from dict


def search():
    """Allow the user to select a character and view their attributes."""
    if not character:
        eg.msgbox("No characters to search.")
        return

    while True:
        choose_character()

        if char_name is None:
            return

        choice_list = list(character[char_name].keys())

        choice = eg.choicebox("Which attribute would you like to view?",
                              choices=choice_list)
        if choice is None:
            return

        if choice == "Skills" or choice == "Ability scores":
            # For nested dicts, allow editing nested values
            search_category_edit(char_name, choice)

        else:
            output = character[char_name][choice]
            eg.msgbox(f"Your {choice} is {output}")

        again = eg.ynbox("Would you like to see more attributes?")

        if not again:
            break


def print_character_shell(char_name):
    """Print all character details to the console for debugging or review."""
    if char_name is None:
        return

    print(char_name)

    for attribute in character[char_name]:
        if attribute == "Ability scores":
            for attr in character[char_name]["Ability scores"]:
                print(attr, ":", character[char_name]["Ability scores"][attr])

        elif attribute == "Skills":
            for attr in character[char_name]["Skills"]:
                print(attr, ":", character[char_name]["Skills"][attr])

        else:
            print(attribute, ":", character[char_name][attribute])


def view_full_character(char_name, blurb):
    """
    Display a summary of the character attributes and scores in a text box.

    Optionally show a blurb (like a message or note) alongside.
    """
    if char_name is None:
        return

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

    # Display the text box with the full output
    if blurb is None:
        eg.textbox(f"{char_name}'s stats",
                   text=output, title="Full character :)")
    else:
        eg.textbox(f"{char_name}'s stats {blurb}",
                   text=output, title="Full character :)")


def add_attribute():
    """
    Adds custom attribute to the selected character.

    Ensures non-empty keys and values are entered.
    """
    global char_name
    while True:
        key_name = eg.enterbox("What would you like the new "
                               "attribute to be called?\ne.g. Coolness")

        if key_name is None or key_name == "":
            eg.msgbox("You need to have a value for your attribute.",
                      title="Error")
            break

        value = eg.enterbox("What you like like the value to be?"
                            "\n e.g. 1 Million")
        if value is None or value == "":
            eg.msgbox("You need to have a value for your attribute.",
                      title="Error")
            break

        else:
            # Add the new attribute to the character dictionary
            character[char_name][key_name] = value

        again = eg.ynbox("Would you like to add more attributes?")
        if not again:
            break


def main_menu():
    """
    Main program loop shows the menu and handles user choices.

    Calls respective functions based on user's menu selection.
    """
    global char_name

    while True:
        choice_list = MAIN_MENU_OPTIONS

        choice = eg.choicebox("Would you like to...", choices=choice_list,
                              title="Main menu")

        if choice == "Add new character":
            char_name = eg.enterbox("What is your character's name?")
            if char_name:
                add_character(char_name)

        elif choice == "Edit characters":
            edit()

        elif choice == "Search characters":
            search()

        elif choice == "Remove character":
            remove_character()

        elif choice == "Print characters to shell":
            choose_character()
            print_character_shell(char_name)

        elif choice == "View full character":
            choose_character()
            view_full_character(char_name, None)

        elif choice == "Add a new attribute":
            choose_character()
            add_attribute()

        else:
            break  # Quit program


# Initialize character dictionary with one sample character for testing
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

# Show welcome message before launching main menu
welcome = eg.buttonbox("Welcome to Ollie's awesome character creator!",
                       choices=["Welcome"], title="Welcome")
if welcome is None:
    quit()  # Exit if user closes the dialog

# Start the main program loop
main_menu()

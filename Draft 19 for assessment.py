"""GUI library for input boxes and message boxes."""
import easygui as eg  # GUI library for input boxes and message boxes

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

def choose_character():
    global char_name
    
    choice_list = list(character.keys())
    
    if len(choice_list) == 1:
        char_name = eg.buttonbox("Choose your character", title="Choose your character",
                     choices=choice_list)
        
        if char_name:
            char_name = choice_list[0]
            
        else:
            return
    else:
        char_name = eg.choicebox("What character would you like to choose?",
                                 choices=choice_list,
                                 title="Choose your character")
        

def get_input(name, category_name, category_list):
    """Prompt the user to enter values for a category.

    and store them in the character dictionary.
    """
    
    character[name][category_name] = {}
    
    for attr in category_list:
        value = eg.integerbox(f"What is your {attr}?",
                              title="Input values", upperbound="20")
        if value is None:
            return None
        
        character[name][category_name][attr] = value
        
    return name

def skill_calc(name):
    """Calculate skill modifiers based on associated ability scores."""
    
    character[name]["Skills"] = {}
    
    for skill, ability in skills.items():
        ability_score = character[name]["Ability scores"][ability]
        
        modifier = (ability_score - 10) // 2
        
        character[name]["Skills"][skill] = modifier


def search_category_edit(char_name, section_name):
    """Allow the user to edit a value within a nested category."""
    
    keys = list(character[char_name][section_name].keys())
    
    choice = eg.choicebox(f"Edit which {section_name}?", choices=keys,
                          title="Choose a value to edit")
    
    if choice is None:
        return
    
    current = character[char_name][section_name][choice]
    
    change = eg.ynbox(f"{choice} is currently {current}. Change it?",
                      title="Change subvalue?")
    if change:
        new_val = eg.integerbox(f"Enter new value for {choice}:",
                                title="Enter new value")
        
        if new_val is None:
            return
        
        character[char_name][section_name][choice] = new_val


def edit():
    global char_name
    """Allow the user to rename or edit an existing character.

    and their attributes.
    """
    
    while True:
        choose_character()
        
        if char_name is None:
            break
        
        change = eg.ynbox(f"Their current name is {char_name}."
                          "\nWould you like to change it?", title = "Change name?")
        if change:
            new_value = eg.enterbox("What would you like "
                                    "their new name to be?", title="New name")
            
            if new_value is None:
                return
            character[new_value] = character.pop(char_name)
            char_name = new_value

        choice_list = list(character[char_name].keys())
        
        choice = eg.choicebox("Would you like to view or edit an attribute?",
                              choices=choice_list, title="Edit attribute?")
        if choice is None:
            return

        if choice == "Skills" or choice == "Ability scores":
            search_category_edit(char_name, choice)
            
        else:
            output = character[char_name][choice]
            
            change = eg.ynbox(f"Your {choice} is {output}\nWould you like to"
                              " change it?", title="Change it?")
            
            if change:
                new_value = eg.enterbox("What would you like to change it to?",
                                        title="New value")
                
                if new_value is None:
                    return
                character[char_name][choice] = new_value

        again = eg.ynbox("Would you like to change or see more attributes?",
                         title="See more attributes?")
        if not again:
            break


def add_character(char_name):
    """Create a new character with inputted attributes.

    and calculated skills.
    """
    
    character[char_name] = {}

    for attr in attributes:
        value = eg.enterbox(f"What is your {attr}?", title="Input attribute")
        
        if value:
            character[char_name][attr] = value
            
        else:    
            del character[char_name]
            return   
        

    if get_input(char_name, "Ability scores", ability_scores) is None:
        del character[char_name]
        return
    
    skill_calc(char_name)
    
    view_full_character(char_name, "Double check your information please")
    
    correct = eg.ynbox("Was that information correct?",
                       title="Would you like to edit?")
    
    if correct is False:
        edit()


def remove_character():
    """Remove an existing character from the dictionary."""
    if len(character) <= 1:
        eg.msgbox("You can't remove a character if14 you have only 1 or none.",
                  title="Pretty self explanatory")
        return

    char_remove = eg.choicebox("What character would you like to remove?",
                               choices=list(character.keys()),
                               title="Pick a character")
    if char_remove is None:
        return

    sure = eg.ynbox("Are you sure you want to remove this character?",
                    title="Are you sure?")
    
    if sure:
        character.pop(char_remove)


def search():
    """Allow the user to search for and view character attributes."""
    
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
            search_category_edit(char_name, choice)
            
        else:
            output = character[char_name][choice]
            eg.msgbox(f"Your {choice} is {output}")

        again = eg.ynbox("Would you like to see more attributes?")
        
        if not again:
            break


def print_character_shell(char_name):
    """Print all character data to the console."""
    
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
    """Display all data for a given character in a text box."""
    
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
            
    if blurb == None:
        eg.textbox(f"{char_name}'s stats",
                   text=output, title="Full character :)")
        
    else:
        eg.textbox(f"{char_name}'s stats {blurb}",
                   text=output, title="Full character :)")

def add_attribute(char_name):
    """Allow the user to add a custom attribute"""

    while True:
        key_name = eg.enterbox("What would you like the new "
                               "attribute to be called?\ne.g. Coolness")
        
        if key_name is None or key_name == "":
            eg.msgbox("You need to have a value for your attribute.", title="Error")
            break
        
        value = eg.enterbox("What you like like the value to be \n e.g. 1 Million")
        if value is None or value == "":
            eg.msgbox("You need to have a value for your attribute.", title="Error")
            break
        
        else:
            character[char_name][key_name] = value
            
        again = eg.ynbox("Would you like to add more attributes?")
        if not again:
            break        


def main_menu():
    global char_name
    """Display the main menu and handle user choices."""
    
    while True:
        choice_list = ["Add new character", "Edit characters",
                       "Search characters", "Remove character",
                       "Print characters to shell",
                       "View full character", "Add a new attribute", "Quit"]
        
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
            add_attribute(char_name)
            
        else:
            break


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
welcome = eg.buttonbox("Welcome to Ollie's awesome character creator!",
                       choices=["Welcome"], title="Welcome")
if welcome == None:
    quit()
    
main_menu()

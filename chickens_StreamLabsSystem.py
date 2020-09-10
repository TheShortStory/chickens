import json
import os
import sys
import codecs
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

# ---------------------------
#   [Required] Script Information
# ---------------------------
ScriptName = "ChickenGame"
Website = "sarah@sarahstoryengineering.com"
Description = "Guess how many chickens will hatch!"
Creator = "TheShortStory"
Version = "1.3.0"

# ---------------------------
#   Global Variables
# ---------------------------
guessingOpen = False
guesses = []
settings = {}
start_time = None


# ---------------------------
#   [Required] Initialize chatbot
# ---------------------------
def Init():
    global settings
    directory = os.path.dirname(__file__)

    try:
        with codecs.open(os.path.join(directory, "settings.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    except Exception as e:
        Parent.Log(ScriptName, e)
        settings = {
            'prizeAmount': 100,
            'startGamePermission': 'moderator',
            'participatePermission': 'everyone',
            'timeLimit': 5,
        }

    return


# ---------------------------
#   [Required] Execute Data / Process messages
# ---------------------------
def Execute(data):
    command = data.GetParam(0)
    user_id = data.User
    if command == '!chickens' and Parent.HasPermission(user_id, settings['participatePermission'], ''):
        guess = data.GetParam(1)
        user_id = data.User
        user_name = data.UserName
        make_guess(user_name, user_id, guess)

    elif command == '!chickenstart' and Parent.HasPermission(user_id, settings['startGamePermission'], ''):
        open_guessing()

    elif command == '!chickenclose' and Parent.HasPermission(user_id, settings['startGamePermission'], ''):
        close_guessing()

    elif command == '!chickenwinner' and Parent.HasPermission(user_id, settings['startGamePermission'], ''):
        winning_count = data.GetParam(1)
        get_winners(winning_count)

    else:
        return


# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------
def Tick():
    guessing_time_limit = settings.get('timeLimit')
    if start_time and guessingOpen and guessing_time_limit:
        elapsed_time = (datetime.now() - start_time).total_seconds()
        elapsed_time_minutes = elapsed_time / 60
        if elapsed_time_minutes > guessing_time_limit:
            close_guessing()
    return


# ---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
# ---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    global settings
    settings = json.loads(jsonData)
    return


# ---------------------------
#   Chicken Game Functions!!
# ---------------------------
def open_guessing():
    global guesses
    guesses = []
    global guessingOpen
    guessingOpen = True
    global start_time
    start_time = datetime.now()
    Parent.SendStreamMessage(
        "We're going to play the chicken game! Guess how many chickens will hatch using the !chickens command. The winners will get {} {}! Example: !chickens 4".format(
            settings['prizeAmount'], Parent.GetCurrencyName()
        )
    )


def close_guessing():
    global guessingOpen
    guessingOpen = False
    global start_time
    start_time = None
    guess_string = ''
    for guess in guesses:
        guess_string += '{}: {}\n'.format(guess['user_name'], guess['number'])
    Parent.SendStreamMessage(
        "Guessing is now closed for the chicken game! Here's what everyone guessed:\n {}".format(guess_string)
    )


def make_guess(username, user_id, guess):
    if not guessingOpen:
        Parent.SendStreamMessage("There's no active chicken game right now. Try again later!")
        return

    try:
        num_chickens = int(guess)
    except ValueError:
        Parent.SendStreamMessage("You have to guess a number to join the chicken game! Example: !chickens 4")
        return

    if user_id in [guess['user_id'] for guess in guesses]:
        Parent.SendStreamMessage("Sorry, {}, you can only submit one guess for the chicken game!".format(username))
        return

    guesses.append({
        'user_name': username,
        'user_id': user_id,
        'number': num_chickens
    })
    Parent.SendStreamMessage("{} guessed that there will be {} chickens!".format(username, guess))


def get_winners(number_of_chickens):
    try:
        num_chickens = int(number_of_chickens)
    except ValueError:
        return

    winners = [guess for guess in guesses if guess['number'] == num_chickens]
    if winners:
        Parent.AddPointsAll({
            winner['user_id']: settings['prizeAmount']
            for winner in winners
        })

        winner_string = ",".join(winner['user_name'] for winner in winners)
        Parent.SendStreamMessage(
            "Winner Winner Chicken Dinner!! The winners are: {}. They have each received {} {}".format(
                winner_string, settings['prizeAmount'], Parent.GetCurrencyName()
            )
        )
    else:
        Parent.SendStreamMessage("Awww, man, no winners in the chicken game this time!")

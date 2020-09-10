# The Chicken Game

Download the zip of this repo [here](https://github.com/TheShortStory/chickens/releases), then upload it into Streamlabs Chatbot. Instructions here: https://streamlabs.com/content-hub/post/chatbot-scripts-desktop 

## Commands:

#### Streamer/Mods:

`!chickenstart`: Starts a new chicken game and opens up the floor for guessing.

`!chickenclose`: Close the guessing. No new guesses will be accepted. This command is not necessary - the guessing will automatically close once the time limit expires. It is here in case you need to close guessing before the time limit runs out.

`!chickenwinner <number>`: Find and announce the winners. They will be awarded channel currency. Default is 100 pts, but this is configurable.

#### Viewers:

`!chickens <number>`: Submit a guess for how many chickens you think will hatch.

## Configuration

There are 4 values you can configure:

| Name  | Description  | Default  |
|-------|--------------|----------|
| Prize Amount  | The amount of channel currency to award the winner  | 100 |
| Start Game Permission  | Who is allowed to start, end, and announce the winners of the game  | moderator |
| Participate Permission  | Who is allowed to make guesses and participate in the game  | everyone  |
| Time Limit  | The time limit in minutes for how long the guessing is open  | 5  |

from openai import OpenAI

# ------------------------------------------------------------
# OpenAI Client
# ------------------------------------------------------------

client = OpenAI()


# ------------------------------------------------------------
# Display introduction
# ------------------------------------------------------------

def introduction():

    print("\n" + "=" * 70)
    print("          CHATGPT-BASED INTERACTIVE STORYTELLING")
    print("=" * 70)

    print("\nWelcome to your Interactive Storytelling Adventure!")
    print("\nYou are the author and the main decision-maker.")
    print("Describe your story, characters and actions naturally.")
    print("The AI will create and continue the story based on your input.")

    print("\nExamples:")
    print("  Story idea: A mystery in an abandoned city")
    print("  Character: A detective named Maya who is afraid of darkness")
    print("  Setting: A remote village during a thunderstorm")
    print("  Action: I open the locked door and enter the room.")

    print("\nType 'quit' at any time to exit.")
    print("=" * 70)


# ------------------------------------------------------------
# Get initial story information
# ------------------------------------------------------------

def get_story_setup():

    print("\n" + "-" * 70)
    print("                     CREATE YOUR STORY")
    print("-" * 70)

    genre = input(
        "\nWhat kind of story would you like to create?\n"
        "You can describe the genre in your own words: "
    )

    character = input(
        "\nDescribe your main character:\n"
        "Name, personality, background, abilities, etc.: "
    )

    setting = input(
        "\nDescribe the setting or world of the story:\n"
        "You can be as creative as you want: "
    )

    story_idea = input(
        "\nWhat is the main idea or situation of the story?\n"
        "Describe it in your own words: "
    )

    return genre, character, setting, story_idea


# ------------------------------------------------------------
# Generate the opening story using OpenAI
# ------------------------------------------------------------

def generate_opening(
    genre,
    character,
    setting,
    story_idea
):

    prompt = f"""
You are an expert interactive storyteller.

Create the opening of an interactive story using the
information provided by the user.

STORY STYLE / GENRE:
{genre}

MAIN CHARACTER:
{character}

SETTING:
{setting}

STORY IDEA:
{story_idea}

Instructions:

- Use the user's ideas as the foundation of the story.
- Do not force the story into a predefined genre.
- Do not change the character unnecessarily.
- Create a vivid and engaging opening.
- Establish the setting and situation.
- Introduce an interesting conflict, mystery, goal or problem.
- Write approximately 300 words.
- End at a natural point where the player can decide what to do.
- Do not provide predefined choices.
- Do not mention that you are an AI.

Return only the story.
"""

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text.strip()

    except Exception as error:

        print("\nUnable to generate the story.")
        print("Error:", error)

        return None


# ------------------------------------------------------------
# Continue the story based on ANY user input
# ------------------------------------------------------------

def continue_story(
    story,
    user_action,
    genre,
    character,
    setting
):

    prompt = f"""
You are an interactive storytelling AI.

Continue the story based on the player's latest action.

ORIGINAL STORY STYLE:
{genre}

MAIN CHARACTER:
{character}

SETTING:
{setting}

STORY SO FAR:
{story}

PLAYER'S LATEST ACTION:
{user_action}

Instructions:

- Continue directly from the existing story.
- Treat the player's action as intentional.
- The player can write ANY action, dialogue, idea or decision.
- Do not restrict the player to predefined choices.
- Make the player's decision meaningfully affect the story.
- Maintain continuity with previous events.
- Remember important characters, locations and events.
- Introduce new events naturally.
- Allow the story to evolve dynamically.
- Do not restart the story.
- Do not contradict established facts unless it is part of the story.
- Write approximately 250-350 words.
- End at an interesting point where the player can decide what to do next.
- Do not give numbered choices.
- Do not mention that you are an AI.

Return only the next part of the story.
"""

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text.strip()

    except Exception as error:

        print("\nUnable to continue the story.")
        print("Error:", error)

        return None


# ------------------------------------------------------------
# Generate the ending
# ------------------------------------------------------------

def generate_ending(
    story,
    genre,
    character,
    setting
):

    prompt = f"""
You are an expert storyteller.

Create a satisfying conclusion for the interactive story below.

STORY STYLE:
{genre}

MAIN CHARACTER:
{character}

SETTING:
{setting}

STORY:
{story}

Instructions:

- Resolve the main conflict or goal.
- Respect the choices made by the player.
- Give important characters meaningful conclusions.
- Connect the ending to earlier events.
- Make the ending feel earned and satisfying.
- The ending may be happy, sad, mysterious, unexpected,
  open-ended or any other style appropriate to the story.
- Do not force a particular type of ending.
- Write approximately 400 words.
- Do not mention that you are an AI.

Return only the final chapter.
"""

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text.strip()

    except Exception as error:

        print("\nUnable to generate the ending.")
        print("Error:", error)

        return None


# ------------------------------------------------------------
# Main storytelling adventure
# ------------------------------------------------------------

def storytelling_adventure():

    introduction()

    # --------------------------------------------------------
    # Get story information from user
    # --------------------------------------------------------

    genre, character, setting, story_idea = get_story_setup()

    print("\n" + "=" * 70)
    print("                    STORY BEGINS")
    print("=" * 70)

    print("\nChatGPT is creating your story...\n")

    story = generate_opening(
        genre,
        character,
        setting,
        story_idea
    )

    if story is None:
        return

    print(story)

    # --------------------------------------------------------
    # Interactive story loop
    # --------------------------------------------------------

    chapter = 1

    while True:

        print("\n" + "-" * 70)
        print(f"                    CHAPTER {chapter}")
        print("-" * 70)

        print("\nWhat does your character do next?")
        print("Describe your action naturally.")
        print("You can write anything: an action, dialogue,")
        print("decision, question, or event.")

        user_action = input("\nYour action: ")

        # Exit the game
        if user_action.lower().strip() == "quit":
            print("\nThank you for playing!")
            return

        # Ask the AI to continue the story
        print("\nChatGPT is continuing your story...\n")

        new_story = continue_story(
            story,
            user_action,
            genre,
            character,
            setting
        )

        if new_story is None:
            return

        print(new_story)

        # Add new story to story history
        story += "\n\n" + new_story

        chapter += 1

        # ----------------------------------------------------
        # Ask whether the player wants to continue
        # ----------------------------------------------------

        print("\n" + "-" * 70)

        while True:

            choice = input(
                "\nContinue the adventure, finish the story, "
                "or quit? (continue/finish/quit): "
            ).lower().strip()

            if choice == "continue":
                break

            elif choice == "finish":

                print("\n" + "=" * 70)
                print("                    FINAL CHAPTER")
                print("=" * 70)

                print("\nChatGPT is creating the conclusion...\n")

                ending = generate_ending(
                    story,
                    genre,
                    character,
                    setting
                )

                if ending is not None:
                    print(ending)

                print("\n" + "=" * 70)
                print("                       THE END")
                print("=" * 70)

                return

            elif choice == "quit":

                print("\nThank you for playing!")
                return

            else:

                print(
                    "Please type 'continue', 'finish', or 'quit'."
                )


# ------------------------------------------------------------
# Program execution
# ------------------------------------------------------------

if __name__ == "__main__":

    try:

        storytelling_adventure()

    except KeyboardInterrupt:

        print("\n\nStorytelling session ended.")

    except Exception as error:

        print("\nAn unexpected error occurred:")
        print(error)


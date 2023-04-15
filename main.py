import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Back, Style
from utils.AI_Output_Input import *
from utils.ImageGenerator import *

# load values from the .env file if it exists
load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

global language
language = 'English'

INSTRUCTIONS = f"""You are an helpful AI assistant of Ankit Yadav who is 14 years old boy who developed you.
Your Name is Friday. You are female.
Your reply should in {language} language only.
You should be so funny and humble.
You are powered by Yahkart and build by Ankit Yadav. 
If user request to play song or watch youtube or open website then you can open any website by just providing one link of request by appending "Source/Web: <and link of user request here>"  at the end of prompt.
You can generate, draw and create any image by generating the ultra real prompt for Stable Diffusion and append the prompt to generate image here "Source/generateImage: <add the prompt to generate image here> at the end of prompt and do it when user ask to draw or generate any image!"""

TEMPERATURE = 0.5
MAX_TOKENS = 80
FREQUENCY_PENALTY = 0.6
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10


def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    speakByPytts("Thinking...")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens= MAX_TOKENS if language == 'English' else 150,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content


def generateImage(prompt):
    """Get a url of generate image

    Parameters:
        prompt (str): The instructions for the chat bot - this determines how it will behave

    Returns:
        The response prompt url
    """
    speakByPytts("Wait, Generating Image")
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url


def get_moderation(question):
    """
    Check the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None


def main():
    # os.system("cls" if os.name == "nt" else "clear")
    # keep track of previous questions and answers
    previous_questions_and_answers = []
    while True:
        # ask the user for their question
        new_question = takeCommand()
        if language == "english" and len(previous_questions_and_answers) == 0 and "friday" not in new_question.lower():
            pass
            
        else:
            if " " == new_question or len(new_question) == 0 or new_question == "None":
                    pass
            else:
                    
                    # check the question is safe
                    errors = get_moderation(new_question)
                    if errors:
                        print(
                            Fore.RED
                            + Style.BRIGHT
                            + "Sorry, you're question didn't pass the moderation check:"
                        )
                        for error in errors:
                            print(error)
                        print(Style.RESET_ALL)
                        continue

                    response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

                    # add the new question and answer to the list of previous questions and answers
                    previous_questions_and_answers.append((new_question, response))

                    # print the response
                    print(Fore.GREEN + Style.BRIGHT + "Here you go: " + Style.NORMAL + Style.RESET_ALL + response)

                    global query
                    query = ''
                    
                    if 'Source/' in response:
                        query = response.split("Source/")[1]

                    response = response.split("Source/")[0]
                    speak(response)

                    if query and 'Web:' in query:
                        OpenWebsite(query.split("Web: ")[1])

                    if query and 'generateImage:' in query:
                        imagePrompt = query.split("generateImage: ")[1]
                        # OpenWebsite(generateImage(prompt=imagePrompt))
                        generateImageByStableDiffusion(imagePrompt)


if __name__ == "__main__":
    # voiceType('female')
    # voiceSpeed(170)
    SpeakingEnergy(400)
    # voiceType("Adam")
    # listeningLanguageChange('hi-In')
    # listeningLanguageChange('ne-NP')
    initializeAiVideoFun()
    main()
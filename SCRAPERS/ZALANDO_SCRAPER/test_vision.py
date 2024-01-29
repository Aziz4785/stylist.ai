import openai
import requests
from PIL import Image
from io import BytesIO
import time
import os
openai.api_key = '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'
print("Current Working Directory: " + os.getcwd())
def download_and_save_image(image_url, save_format='png'):
   

    # Check if the save format is valid
    if save_format.lower() not in ['png', 'jpg', 'jpeg', 'webp']:
        raise ValueError("Invalid save format. Choose 'png', 'jpg', or 'webp'.")

    try:
        # Print the URL for debugging
        print(f"Attempting to download image from URL: {image_url}")

        # Download the image
        response = requests.get(image_url)
        time.sleep(2)
        if response.status_code != 200:
            raise Exception("Failed to download the image. Status code: " + str(response.status_code))

    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Continue with the rest of your function...


    # Open the image using BytesIO
    image = Image.open(BytesIO(response.content))

    # Save the image in the desired format
    file_name = f"downloaded_image.{save_format.lower()}"
    image.save(file_name, format=save_format.upper())

    print(f"Image saved as {file_name}")


# URL of the clothing image
image1_HD = "https://img01.ztat.net/article/spp-media-p1/946a36a616774b3aaa3d87851949b20c/721ab1e95d2142a8a4d4bdc41127c5df.jpg?imwidth=1800"
image1_mini = "https://img01.ztat.net/article/spp-media-p1/946a36a616774b3aaa3d87851949b20c/721ab1e95d2142a8a4d4bdc41127c5df.jpg?imwidth=156"
image2_mini = "https://img01.ztat.net/article/spp-media-p1/cf0de7482cb1414dbe668113b5d5c9dd/5060492fae0c4d84ad034a38884993ca.jpg?imwidth=156"
image3_mini = "https://img01.ztat.net/article/spp-media-p1/9e641d64ef444036bc9dcba04a99d9b9/eb3124d7d12e4dbb8a0e5c4bd143ca9d.jpg?imwidth=156"
# Additional features extracted from the website
additional_info = """
brand : adidas Originals
name : ADICOLOR CLASSICS - Sweatshirt
Material and maintenance :
Composition: 52% cotton, 48% polyester
Material: Sweat
Care instructions: Bleaching prohibited 
Product Details :
Collar shape: Round neck
Pattern/Color: Stripes
Additional information: Elastic waist"""
"""
def decribe_clothing_multi(infos,image1,image2,image3):
    response = openai.ChatCompletion.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this piece of clothing. These images represent the same piece of clothing. Here are some additional informations about it " + infos
         +"Please do not repeat the details already provided about the material composition, care instructions etc.."},
            {
            "type": "image_url",
            "image_url": {
                "url": image1,
            },
            },
            {
            "type": "image_url",
            "image_url": {
                "url": image2,
            },
            },
            {
            "type": "image_url",
            "image_url": {
                "url": image3,
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )
    print(response.choices[0].message.content)
"""
def describe_clothing_multi(infos, images):
    # Ensure that no more than 3 images are considered
    images = images[:3]

    # Create the messages list
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this piece of clothing. These images represent the same piece of clothing. Here are some additional informations about it " + infos
         +"Please do not repeat the details already provided about the material composition, care instructions etc.."}
            ]
        }
    ]

    # Add image URLs to the messages
    for img_url in images:
        messages[0]["content"].append({
            "type": "image_url",
            "image_url": {
                "url": img_url,
            }
        })

    # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=200,
    )

    # Print the response
    return response.choices[0].message.content
"""
def describe_clothing(additional_info,image_url):
    #download_and_save_image(image_url, "png")
    # Making the request to the GPT-4 Vision API
    try:
        response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
        {
        "role": "user",
        "content": [
        {"type": "text", "text": "Describe this piece of clothing. Here are some additional informations about it " + additional_info
         +"Please do not repeat the details already provided about the material composition, care instructions etc.."},
            {
            "type": "image_url",
            "image_url": {
                "url": image_url,
            },
            },
        ],
        }
    ],
            max_tokens=200
        )

        # Print the response
        print(response.choices[0].message.content)
    except Exception as e:
        print("Error during API call:", e)
        return None
"""
#describe_clothing(additional_info,image1_mini)
decribe_clothing_multi(additional_info,image1_mini,image2_mini,image3_mini)
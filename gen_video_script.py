
import cohere



import os
import shutil


#prompt="Write a short paragraph about christians"
prompt="Write a few paragraphs of powerful night prayers including bible verses for christians"

max_tokens=500




# Define folder name and clear flag
folder_name = "scripts/"
clear_flag = 1  # Set to True to clear the folder contents

# Check if the folder exists
if not os.path.exists(folder_name):
    os.makedirs(folder_name)  # Create the folder if it doesn't exist
    print(f"Folder '{folder_name}' created.")
if clear_flag:
    shutil.rmtree(folder_name)  # Delete the folder and its contents
    os.makedirs(folder_name)   # Recreate the empty folder
 



# Initialize the Cohere client
co = cohere.Client('eVETg688WO5ALfJXDHOUImyyZM1xJo_yours')

# Generate text
response = co.generate(
    model='command-xlarge',
    prompt=prompt,
    max_tokens=max_tokens
)

# Print and save the generated text
script_text = response.generations[0].text
print(script_text)

with open(folder_name +"script.txt", "w") as file:
    file.write(script_text)

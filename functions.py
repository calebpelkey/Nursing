import json
import os
import openai

def create_assistant(client, name, description, training_data_file='Nursing_Knowledge.docx', model='gpt-4-1106-preview'):
    assistant_file_path = 'assistant.json'
    assistant_id = None

    try:
        if os.path.exists(assistant_file_path):
            with open(assistant_file_path, 'r') as file:
                assistant_data = json.load(file)
                assistant_id = assistant_data['assistant_id']
                print("Loaded existing assistant ID.")
        else:
            if os.path.exists(training_data_file):
                with open(training_data_file, "rb") as doc_file:
                    # Create the file object in the OpenAI system
                    file_object = client.files.create(file=doc_file, purpose='assistants')
            else:
                raise FileNotFoundError(f"Training data file '{training_data_file}' not found.")

            # Detailed instructions for the assistant
            instructions = f"{name} is designed to {description}. It uses the provided document for detailed information."

            # Create the assistant
            assistant = client.Assistant.create(
                name=name,
                instructions=instructions,
                model=model,
                tools=[{"type": "retrieval"}],
                file_ids=[file_object.id]  # Use the ID of the file object
            )

            # Save the assistant ID
            with open(assistant_file_path, 'w') as file:
                json.dump({'assistant_id': assistant.id}, file)
                print("Created a new assistant and saved the ID.")

            assistant_id = assistant.id

    except Exception as e:
        print(f"Error in creating assistant: {e}")

    return assistant_id

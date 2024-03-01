import os
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\karan\Desktop\vision api\vision-api-414610-4c5c5e83ae2f.json'

def detect_labels_and_save_folder(folder_path, output_folder):
    """Detects labels in all images in the folder and saves results to text files."""
    client = vision.ImageAnnotatorClient()

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.png', '.jpeg')):  # Add more file extensions if needed
            image_path = os.path.join(folder_path, filename)

            with open(image_path, "rb") as image_file:
                content = image_file.read()

            image = vision.Image(content=content)

            response = client.label_detection(image=image)
            labels = response.label_annotations

            output_file_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_labels.txt')

            with open(output_file_path, 'w') as result_file:
                result_file.write("Labels:\n")
                for label in labels:
                    result_file.write(label.description + "\n")

            if response.error.message:
                raise Exception(
                    "{}\nFor more info on error messages, check: "
                    "https://cloud.google.com/apis/design/errors".format(response.error.message)
                )

# Example usage
input_folder_path = r'C:\Users\karan\Desktop\vision api\media'
output_folder_path = r'C:\Users\karan\Desktop\vision api\media\output.txt'
detect_labels_and_save_folder(input_folder_path, output_folder_path)

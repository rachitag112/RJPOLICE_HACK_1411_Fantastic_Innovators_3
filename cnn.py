import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
​
# Load the Faster R-CNN with Inception ResNet V2 model from TensorFlow Hub
detector = hub.load("https://www.kaggle.com/models/tensorflow/faster-rcnn-inception-resnet-v2/frameworks/TensorFlow2/variations/640x640/versions/1")
​
# Path to your dataset folder
dataset_path = '/kaggle/input/your-dataset-folder'
​
# List all image files in the dataset folder
image_files = [file for file in os.listdir(dataset_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
​
# Process each image in the dataset
for image_file in image_files:
    # Construct the full path to the image
    image_path = os.path.join(dataset_path, image_file)
​
    # Read the image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
​
    # Reshape the image to match the expected input format
    image_tensor = tf.convert_to_tensor(image_rgb, dtype=tf.uint8)
    image_tensor = tf.expand_dims(image_tensor, axis=0)
​
    # Run object detection
    detector_output = detector(image_tensor)
​
    # Extract relevant information from the output
    num_detections = detector_output["num_detections"].numpy()[0]
    detection_boxes = detector_output["detection_boxes"].numpy()
    detection_classes = detector_output["detection_classes"].numpy().astype(int)
    detection_scores = detector_output["detection_scores"].numpy()
​
    # Visualize the results on the image
    for i in range(int(num_detections)):
        class_id = detection_classes[i]
        score = detection_scores[i]
        box = detection_boxes[i]
​
        if score > 0.5:  # Set a threshold for confidence
            ymin, xmin, ymax, xmax = box
            ymin, xmin, ymax, xmax = int(ymin * image.shape[0]), int(xmin * image.shape[1]), int(ymax * image.shape[0]), int(xmax * image.shape[1])
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(image, f"Class: {class_id}, Score: {score:.2f}", (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
​
    # Display and save the image with bounding boxes
    plt.imshow(image)
    plt.axis('off')
    plt.savefig(os.path.join('/kaggle/working', f'detected_{image_file}'))
    plt.close()
    
    # Release the video capture object
cap.release()
​
# Close the display window
cv2.waitKey(1)
cv2.destroyAllWindows()
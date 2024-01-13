import os
import glob
import concurrent.futures
import cv2

# Define the preprocessing function
def preprocess(video_file, output_folder):
    try:
        # Create a folder for each video file
        video_name = os.path.splitext(os.path.basename(video_file))[0]
        video_output_folder = os.path.join(output_folder, video_name)
        os.makedirs(video_output_folder, exist_ok=True)

        # OpenCV processing tasks here
        cap = cv2.VideoCapture(video_file)

        # Set the desired frame rate to 30 fps
        frame_rate = 30

        # Calculate the number of frames to extract at the desired frame rate
        extract_every_nth_frame = int(cap.get(cv2.CAP_PROP_FPS) / frame_rate)
        if extract_every_nth_frame < 1:
            extract_every_nth_frame = 1

        # Calculate the number of frames to extract
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        num_frames_to_extract = max(num_frames // extract_every_nth_frame, 1)

        # Extract frames and save them as images
        for i in range(num_frames_to_extract):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i * extract_every_nth_frame)
            ret, frame = cap.read()
            if ret:
                # Resize the frame to 640x640 pixels
                frame = cv2.resize(frame, (640, 640))

                image_name = f"frame_{i:06d}.jpg"
                image_path = os.path.join(video_output_folder, image_name)
                cv2.imwrite(image_path, frame)

        # Release the video capture object
        cap.release()

    except Exception as e:
        print(f"Error processing {video_file}: {e}")

# Process all videos in a designated folder
def process_top_level_folders(root_folder, output_root_folder):
    top_level_folders = [folder for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))]

    for top_level_folder in top_level_folders:
        folder_path = os.path.join(root_folder, top_level_folder)
        output_folder = os.path.join(output_root_folder, top_level_folder)

        process_all_videos(folder_path, output_folder)

def process_all_videos(folder_path, output_folder):
    video_files = glob.glob(os.path.join(folder_path, "**/*.mp4"), recursive=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda x: preprocess(x, output_folder), video_files)

# Example usage:
root_folder = r"D:\Anomaly-Detection-Dataset\tester imager"
output_root_folder = r"D:\Anomaly-Detection-Dataset\tester imager processed"

process_top_level_folders(root_folder, output_root_folder)

import gradio as gr
import shutil
import os
import cv2


# import av


def video_demo(video):
    destination = "input/"
    copied = shutil.copy(video, destination)
    if copied:
        print("Video saved successfully")

    output_path = "output/output.mp4"
    # cap = cv2.VideoCapture(output_path)
    # if not cap.isOpened():
    #     print("Error: Could not open video file.")
    return output_path


def slide(x):
    return x


# demo = gr.Interface(fn=video_demo,
#                     inputs=[
#                         gr.Video(label="In", interactive=True),
#                     ],
#                     outputs=gr.Video(label="Out")
#                     )

with gr.Blocks() as demo:
    with gr.Row():
        gr.Interface(
            fn=video_demo,
            inputs=[
                gr.Video(label="In", interactive=True),
            ],
            outputs=gr.Video(label="Out")
        )
        with gr.Column():
            slider = gr.Slider(minimum=0, maximum=100, value=80, step=1, label="Confidence Threshold", randomize=True)
            slider.release(slide, inputs=[slider], outputs=gr.Number())

if __name__ == "__main__":
    demo.launch()

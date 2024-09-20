import typer

from src import show, spotter2, split3, vid, translate
import config

def main(image_path: str = "bilde.jpg"):
    split3.split_image(image_name=image_path, visualize=True)
    focus_points = spotter2.find_points(debug=True)

    if spotter2.check_difference(focus_points):
        raise Exception("Generated focus points are too far apart")

    translate.translate_image_to_focus_point(focus_points)
    vid.make_vid(name="output_video.avi")
    show.play_video(config.OUTPUT_VIDEO_PATH + "/" + "output_video.avi")


if __name__ == '__main__':
    typer.run(main)

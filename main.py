import os

import typer

import config
from src import show, spotter2, split3, vid, translate


def main(image_path: str = "bilde.jpg", visualize_split: bool = True, debug: bool = False, output_video: str = "output_video.avi"):
    split3.split_image(image_name=image_path, visualize=visualize_split)
    focus_points = spotter2.find_points(debug=debug)

    if spotter2.check_difference(focus_points):
        raise Exception("Generated focus points are too far apart")

    translate.translate_image_to_focus_point(focus_points)
    vid.make_vid(name=output_video)
    show.play_video(os.path.join(config.OUTPUT_VIDEO_PATH, "output_video.avi"))


if __name__ == '__main__':
    typer.run(main)

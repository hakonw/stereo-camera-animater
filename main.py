import typer

import show
import split3
import spotter2
import translate
import vid


def main(image_path: str = "bilde.jpg"):
    split3.split_image(image_name=image_path)
    focus_points = spotter2.find_points(debug=True)

    if spotter2.check_difference(focus_points):
        raise Exception("Points are too far apart")

    translate.translate_image_to_focus_point(focus_points)
    vid.make_vid()
    show.play_video("output_video.avi", scale_factor=0.2, frame_ms=30)


if __name__ == '__main__':
    typer.run(main)

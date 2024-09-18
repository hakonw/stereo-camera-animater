

import split3
import spotter2
import translate
import vid

if __name__ == '__main__':
    split3.split_image()
    focus_points = spotter2.find_points()
    translate.translate_image_to_focus_point(focus_points)
    vid.make_vid()
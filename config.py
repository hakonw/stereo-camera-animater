# config.py

# Paths
OUTPUT_DIR = "output"                          # Main output directory
SPLIT_DIR = f"{OUTPUT_DIR}/splitted"           # Directory for split images
SPOTTED_DIR = f"{OUTPUT_DIR}/spotted"          # Directory for focus points marked images
TRANSLATED_DIR = f"{OUTPUT_DIR}/translated"    # Directory for translated images
OUTPUT_VIDEO_PATH = f"{OUTPUT_DIR}"            # Path for the generated video

# Image Processing
SCALE_FACTOR = 0.1                             # Scale factor for image resizing during display
GROW_STEP = 15                                 # Grow step for image splitting
DARKNESS_THRESHOLD = 2000                      # Threshold for growing boxes
BOX_SIZE_LIMIT_RATIO = 0.3                     # Maximum box size limit as a ratio of the image width

# Focus Points Detection
SCALE_FACTOR_SINGLE = 0.2                      # Scale factor for image resizing during display
ROI_SIZE = 200                                 # Size of the ROI for focus point detection in px
MAX_DIFFERENCE_LIMIT = 200                     # Maximum allowed difference between focus points

# Video Creation
FRAME_DURATION = 4                             # Number of frames each image will display in the video
LOOP_COUNT = 5                                 # Number of loops in the video sequence
FPS = 24                                       # Frames per second for the video
FRAME_SEQUENCE = [0, 1, 2, 3, 2, 1]            # Sequence of frames for video animation

# Video Playback
SCALE_FACTOR_PLAYBACK = 0.2                    # Scale factor for video playback
PLAYBACK_FRAME_MS_PSEUDO = 30                           # Almost minimum duration per frame in milliseconds for playback


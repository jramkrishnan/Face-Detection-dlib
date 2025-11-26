# Face Detection System using dlib

A security system designed to track and identify people entering a community using facial recognition technology. This project leverages the dlib library's powerful face detection and recognition capabilities to create a reliable monitoring solution.

## Overview

This system uses computer vision techniques to detect and recognize faces in real-time, making it suitable for community security applications, access control, and visitor tracking. Built with Python and dlib, it provides accurate face detection and recognition using state-of-the-art deep learning models.

## Features

- **Real-time Face Detection**: Detects multiple faces simultaneously using dlib's HOG-based detector
- **Face Recognition**: Identifies known individuals by comparing facial features
- **Unknown Person Handling**: Captures and logs unrecognized faces for review
- **Community Access Tracking**: Monitors and records entry/exit events
- **High Accuracy**: Uses dlib's pre-trained ResNet model for reliable recognition

## Technologies Used

- **Python**: Core programming language
- **dlib**: Face detection and recognition library
- **OpenCV**: Image processing and video capture
- **NumPy**: Numerical computations

## Prerequisites

Before running this project, make sure you have:

- Python 3.7 or higher
- CMake (required for dlib installation)
- A webcam or camera device

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jramkrishnan/Face-Detection-dlib.git
cd Face-Detection-dlib
```

2. Install the required dependencies:
```bash
pip install dlib
pip install opencv-python
pip install numpy
```

Note: If you encounter issues installing dlib, you may need to install CMake first:
```bash
# On Ubuntu/Debian
sudo apt-get install cmake

# On macOS
brew install cmake

# On Windows
# Download from https://cmake.org/download/
```

3. Download the required dlib models:
- Shape predictor: [shape_predictor_5_face_landmarks.dat](http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2)
- Face recognition model: [dlib_face_recognition_resnet_model_v1.dat](http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2)

Extract these files and place them in the project directory.

## Project Structure

```
Face-Detection-dlib/
├── images/              # Store known face images here
├── unknown/             # Captured unknown faces
├── models/              # Pre-trained dlib models
├── main.py             # Main execution file
├── face_detector.py    # Face detection module
├── face_recognizer.py  # Face recognition module
└── README.md
```

## Usage

1. **Add Known Faces**: 
   - Place images of authorized individuals in the `images/` folder
   - Name each image file as `[PersonName].jpg` (e.g., `john_doe.jpg`)

2. **Run the System**:
```bash
python main.py
```

3. **Real-time Monitoring**:
   - The system will start the webcam and begin detecting faces
   - Known individuals will be identified with their names displayed
   - Unknown faces will be captured and saved for review

## How It Works

1. **Face Detection**: The system uses dlib's frontal face detector to locate faces in the video stream
2. **Face Landmark Detection**: Identifies 68 facial landmarks to align and normalize faces
3. **Feature Extraction**: Generates a 128-dimensional face descriptor using a deep learning model
4. **Recognition**: Compares extracted features with known face encodings using Euclidean distance
5. **Decision Making**: If the distance is below a threshold (typically 0.6), the face is recognized as a match

## Configuration

You can adjust the following parameters in the configuration file:

- `DETECTION_THRESHOLD`: Sensitivity of face detection (default: 1)
- `RECOGNITION_THRESHOLD`: Distance threshold for face matching (default: 0.6)
- `FRAME_SKIP`: Process every nth frame for better performance (default: 2)
- `SAVE_UNKNOWN_FACES`: Automatically save unrecognized faces (default: True)

## Performance Tips

- Use the HOG-based detector for faster processing on CPU
- For GPU-accelerated detection, compile dlib with CUDA support
- Reduce frame resolution for faster processing at the cost of accuracy
- Adjust the upsample parameter to detect smaller/distant faces

## Applications

- Residential community access control
- Office building security
- Visitor management systems
- Event attendance tracking
- Smart home security integration

## Limitations

- Requires good lighting conditions for optimal performance
- May struggle with faces at extreme angles
- Recognition accuracy depends on image quality of reference photos
- Processing speed is limited on systems without GPU acceleration

## Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## Future Enhancements

- [ ] Add database integration for better data management
- [ ] Implement multi-camera support
- [ ] Add mobile app for notifications
- [ ] Include facial mask detection
- [ ] Generate access logs and analytics dashboard
- [ ] Add anti-spoofing mechanisms

## Acknowledgments

- **dlib library** by Davis King for the excellent face recognition tools
- **OpenCV** community for computer vision resources
- Research papers: "One Millisecond Face Alignment with an Ensemble of Regression Trees" by Kazemi and Sullivan

## License

This project is open source and available under the MIT License.

## Contact

For questions or suggestions, please open an issue on GitHub or reach out through the repository.

---

*Note: This system is designed for legitimate security purposes. Please ensure compliance with local privacy laws and regulations when deploying facial recognition systems.*

# VerbalEyes

> VerbalEyes is a Computer Vision application developed in Python, capable of recognizing faces and detecting objects in real time, communicating the results to the user via voice.

>Author: Rui Pedro Ramos Carvalho — nº 27628
---

## About the Project

This project was developed as part of the **Computer Vision** course unit of the Bachelor's Degree in Computer Engineering at IPVC. The main objective is to create an interactive and accessible application that:

- Recognizes the user's face;
- Detects objects in real time with YOLOv8;
- Identifies in which hand the object is located;
- Generates a descriptive voice message.

The system was trained with a subset of the COCO dataset, focusing only on common household objects such as books, phones, bottles, and others.

---

## Features

- Face recognition with `face_recognition`
- Object detection using YOLOv8 (Ultralytics)
- Speech generation with `gTTS` (Google Text-to-Speech)
- Hand position estimation (left/right) based on object location
- Support for webcam and video files
- Generation of messages like: `Rui, you have a bottle in your right hand`

---

## Model Training


| Metric      | Result     |
|-------------|------------|
| Precision   | ~0.85      |
| Recall      | ~0.73      |
| mAP50       | ~0.75      |
| Notes       | Consistent loss reduction, final tests with 150 epochs |

---

## How it Works

- The model detects objects and explicitly ignores the "person" class to avoid redundancies.
- The screen is divided into 3 zones: left (right hand), right (left hand), and center.
- Based on vertical position, it determines if the object is being held.
- The final message is converted to speech with `gTTS` and played.

---

## Demo

[![Watch the demo on YouTube](https://img.youtube.com/vi/HENOUiK7blE/hqdefault.jpg)](https://youtu.be/HENOUiK7blE)

> *Click the image above to watch the application in action.*

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ruicarvalho1/VerbalEyes.git
cd VerbalEyes
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate         # Windows
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

To run the application:

```bash
python verbalEyes.py
```

---

## License

Distributed under the MIT License.

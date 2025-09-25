# Autonomous Electrical Car (Vision computer)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/) 
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://www.tensorflow.org/) 
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)](https://opencv.org/) 
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Embedded-red)](https://www.raspberrypi.com/)

An **educational and experimental project** that combines **embedded systems**, **computer vision**, and **AI for autonomous vehicles**.  
Developed as part of an industrial computer science curriculum, this smart car uses a **Raspberry Pi**, a **camera**, and an **I²C motor/servo shield** to interpret road signs (Stop, Left, Right) in real time and execute the appropriate driving commands.

---

## Objectives

- Apply **deep learning** (CNN with Keras/TensorFlow) to traffic sign recognition.  
- Build a **real-time embedded system** using Raspberry Pi and Python.  
- Demonstrate **autonomous driving decisions** (stop, left turn, right turn) based on visual input.  
- Integrate **ultrasonic sensors** for safe obstacle avoidance.  
- Provide a modular framework for training, inference, and robotic control.

---

## Key Features

- **Traffic Sign Detection & Classification** (Stop, Left, Right).  
- **Flask REST API** server for AI inference.  
- **Raspberry Pi Client** for camera capture and embedded control.  
- **Ultrasonic obstacle detection** for collision avoidance.  
- Modular training pipeline with **dataset structure** for reproducibility.  

---

## Project Structure

```
IntelligentCar/
├─ README.md
└─ TransProject/
   ├─ dataset/               # training and testing data (organized by class)
   │  ├─ train/
   │  │  ├─ class_0/ (Stop)
   │  │  ├─ class_1/ (Left)
   │  │  └─ class_2/ (Right)
   │  └─ test/
   ├─ models/                # trained CNN models (.h5)
   └─ scripts/
      ├─ car_control.py      # Flask server for AI inference
      ├─ train_model.py      # CNN training script
      └─ Client/
         ├─ Clinet.py        # Raspberry Pi client (camera + control)
         ├─ mDev.py          # I²C motor & servo + ultrasonic control
         └─ test.py          # simple tests
```

---

## Installation & Requirements

- **Python 3.10+**  
- **Raspberry Pi** with camera and I²C enabled  

### Python Libraries
```
flask
opencv-python
imutils
requests
numpy
tensorflow==2.15.*
keras==2.15.*
scikit-learn
smbus2   # Raspberry Pi only
```

### Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdir -p TransProject/models TransProject/scripts/uploads
```

---

## Training

Organize dataset into subfolders (`class_0`, `class_1`, …).  
Run:
```bash
cd TransProject/scripts
python train_model.py
```

- Saves trained model into `../models/traffic_sign_model.h5`.  
- Prints validation accuracy and predictions.  

---

## Running the Inference Server

```bash
cd TransProject/scripts
python car_control.py
```

- Endpoint: `POST /upload` with `image` file.  
- Returns command (`stop`, `left`, `right`).  

---

## Raspberry Pi Client

Edit server URL in `Clinet.py` then run:  
```bash
cd TransProject/scripts/Client
python Clinet.py
```

- Captures frames, posts them to server.  
- Executes returned command with motor & servo.  
- Uses ultrasonic sensor for safety stop.  

---

## Visuals (Traffic Signs)

Example of recognized traffic signs used for training and inference:  

<p align="center">
  <img src="./docs/images/panneau1.png" width="200"/>
  <img src="./docs/images/panneau2.png" width="200"/>
  <img src="./docs/images/panneau3.png" width="200"/>
</p>

Visuals of the Electrical Car :
<p align="center">
  <img src="./docs/images/IMG_9945.png" width="600"/>
  <img src="./docs/images/IMG_9949.png" width="600"/>
</p>
---

## Roadmap

- Lane detection fallback (OpenCV).  
- End-to-end behavioral cloning for driving policy.  
- Real-time telemetry logging (latency, FPS, distances).  

---

## Contribution

Pull requests are welcome. For major changes, open an issue first to discuss.  

---

## License

MIT (to be added).

---

## Author

**Alec Waumans**  
Bachelor’s in Industrial Computer Science – Embedded & AI Systems.  

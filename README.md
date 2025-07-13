# TOBB ETÜ ELE495 - Capstone Project

# Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Hardware](#Hardware)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Acknowledgements](#acknowledgements)

## Introduction
In this project, Turkish spoken natural-language commands are first converted to text through an online Speech-to-Text service. The resulting text is then analyzed by a Large Language Model (LLM), which maps each command—via a dedicated algorithm—to basic motion functions. The action being executed is reported back to the user in real time through an online Text-to-Speech service.

Every stage of this pipeline—speech recognition, LLM processing, motion mapping, and voice feedback—is handled via platform-agnostic application programming interfaces (APIs). The mapped motion functions are executed on the vehicle itself using its onboard DC motors, motor drivers, and sensors.


## Features
List the key features and functionalities of the project.
- Timed movements and angular rotations
- User voice recognition
- PID control for precise motion 
- Real-time obstacle avoidance
- User interface for live command and movement tracking

## Hardware
- Raspberry Pi 5 8 GB
- BNO055 9 DOF Absolute Orientation IMU Fusion Breakout
- 2 x HC-SR04 Ultrasonic Distance Sensor
- L298N Motor Driver
- 4 x 6 V DC Motor
- UGreen 10 Ah Powerbank
- 2 x 18650 3.7 V Battery

## Installation
Before running the project, all mechanical components (such as motors, wheels, sensors, and power connections) must be properly assembled and tested. Once the hardware setup is complete, the main.py script should be executed on the Raspberry Pi. After the script is launched, and the Raspberry Pi is connected to the same Wi-Fi network as the client device, the user can access the web-based interface. From the interface, the system can be started, and the vehicle becomes ready to receive and execute voice commands in real time.

## Usage
To use the project, power on the Raspberry Pi and ensure it is connected to the same local network as the computer or mobile device. Access the web-based user interface by entering the Raspberry Pi's IP address in a browser. Through this interface, users can view the system status in real time and send voice commands, which are processed and executed by the autonomous mini vehicle.

## Screenshots
<img width="1595" height="749" alt="image" src="https://github.com/user-attachments/assets/9323bd37-8db4-4535-8212-ae31ce3dc8ad" />

- Vehicle Icon (top-center) – Rotates in real time to match the issued command, providing full-angle orientation feedback.
- Speech Recognition Output – Displays the spoken commands after they are transcribed to text.
- Commands – Lists, in real time, the motion actions that correspond to each recognized command.
- Task History – Shows the commands that have been successfully completed.
- Real-Time Vehicle Status – Presents the vehicle’s current movement state to the user.


## Acknowledgements
Project Demo:
[Youtube Link](https://youtu.be/RIr8JASv2A8)

Contributors:

- [Şakir Ahmet ARSLAN](https://github.com/Sakirahmet)
- [Ali Murat BÜYÜKAŞIK](https://github.com/alimuratb)
- [Yusuf Kaan ESER]((https://github.com/kaanjr)
- [Güner Toprak KARAMAN](https://github.com/toprakkaraman)
- [İbrahim SARI](https://github.com/ibrahimsari23)

Tools:

- [Google Speech-to-Text (STT)](https://cloud.google.com/speech-to-text)
- [OpenAI GPT-4.0 LLM](https://openai.com/gpt-4)
- [ElevenLabs Text-to-Speech (TTS)](https://www.elevenlabs.io)


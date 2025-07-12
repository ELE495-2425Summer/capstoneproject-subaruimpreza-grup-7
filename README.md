# TOBB ETÜ ELE495 - Capstone Project

# Table of Contents
- [Introduction](#introduction)
- [Features](#features)
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

## Installation
Describe the steps required to install and set up the project. Include any prerequisites, dependencies, and commands needed to get the project running.

```bash
# Example commands
git clone https://github.com/username/project-name.git
cd project-name
```

## Usage
Provide instructions and examples on how to use the project. Include code snippets or screenshots where applicable.

## Screenshots
You can see a sample screenshot of the user interface below.

<img width="1595" height="749" alt="image" src="https://github.com/user-attachments/assets/9323bd37-8db4-4535-8212-ae31ce3dc8ad" />

- Vehicle Icon (top-center) – Rotates in real time to match the issued command, providing full-angle orientation feedback.
- Speech Recognition Output – Displays the spoken commands after they are transcribed to text.
- Commands – Lists, in real time, the motion actions that correspond to each recognized command.
- Task History – Shows the commands that have been successfully completed.
- Real-Time Vehicle Status – Presents the vehicle’s current movement state to the user.


## Acknowledgements
Give credit to those who have contributed to the project or provided inspiration. Include links to any resources or tools used in the project.

[Contributor 1](https://github.com/user1)
[Resource or Tool](https://www.nvidia.com)

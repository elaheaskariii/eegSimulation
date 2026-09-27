Multi-Channel EEG Simulation & Real-Time Visualization

A Python-based prototype for multi-channel EEG signal simulation, synthetic neurological-disorder perturbation, real-time visualization, and webcam-based eye-state interaction.

The project combines synthetic EEG generation with signal perturbation, interactive visualization through Streamlit, and computer-vision-based detection of eye state using MediaPipe.

«Project status: Prototype / Research & Engineering Demonstration
Important: This project currently works with synthetically generated EEG signals and is not a medical diagnostic system.»

---

1. Overview

This project demonstrates an interactive pipeline for generating and visualizing multi-channel EEG-like signals.

The current implementation consists of several main components:

1. Synthetic multi-channel EEG generation
2. Frequency-component selection
3. Synthetic disorder-related signal perturbation
4. Real-time signal visualization
5. Webcam-based eye-state detection
6. Eye-state-dependent alpha activity simulation
7. Facial-motion artifact simulation
8. A preliminary GAN architecture for future EEG signal generation
9. Streamlit-based interactive user interface

The overall purpose is to provide a modular prototype that can later be extended toward more realistic EEG datasets, signal-processing pipelines, generative models, and machine-learning-based analysis.

---

2. System Architecture

User
 │
 ▼
Streamlit Interface
 │
 ├── Select disorder
 ├── Select number of EEG channels
 └── Select frequency
 │
 ▼
Synthetic EEG Generator
 │
 ├── Frequency components
 └── Gaussian noise
 │
 ▼
Synthetic Disorder Perturbation
 │
 ▼
EEG Signal
 │
 ├───────────────┐
 │ │
 ▼ ▼
Real-Time Webcam Input
Plotting │
                  ▼
             MediaPipe
                  │
                  ▼
            Eye-State Detection
                  │
                  ▼
       Alpha Activity Simulation
                  │
                  ▼
             Updated EEG

---

3. EEG Signal Model

The project currently generates synthetic EEG-like signals rather than loading real physiological recordings.

Eight electrode/channel positions are defined:

Fp1
Fp2
T3
T4
O1
O2
P3
P4

The generator can produce up to eight channels.

For each channel, three frequencies are randomly selected from:

Component| Frequency
Delta| 2 Hz
Theta| 5 Hz
Alpha| 10 Hz
Beta| 20 Hz
Gamma| 40 Hz

The synthetic signal is constructed as a sum of sinusoidal components with additive Gaussian noise:

EEG(t) = Σ sin(2π fᵢ t) + Gaussian Noise

Default parameters

Sampling rate: 256 Hz
Duration: 10 seconds
Maximum channels: 8

A 10-second signal sampled at 256 Hz therefore contains:

10 × 256 = 2560 samples/channel

---

4. Electrode Configuration

Channel| Visualization Color
Fp1| Blue
Fp2| Blue
T3| Green
T4| Green
O1| Purple
O2| Purple
P3| Red
P4| Red

---

5. Synthetic Disorder Simulation

The project contains an "apply_disorder()" function for modifying the generated signal according to a selected condition.

Currently, only the "epilepsy" condition has an implemented signal modification.

For the current epilepsy prototype:

Affected channels:
T3
T4

A periodic amplitude perturbation is introduced into these channels.

This is a synthetic signal perturbation for demonstration purposes, not a physiological model of epilepsy.

Available conditions in the interface

Normal
Epilepsy
Alzheimer
Parkinson
Stroke
Schizophrenia
Insomnia
Depression
Anxiety
Autism
Migraine

Only "epilepsy" currently has implemented signal-modification logic. The remaining options are placeholders for future development.

---

6. Webcam and Eye-State Detection

The project uses:

- OpenCV
- MediaPipe Face Mesh

to process webcam frames.

The "detect_eye_state()" function extracts selected facial landmarks around the eyes and uses the distance between selected landmarks as a simple geometric indicator of eye state.

Webcam Frame
      ↓
BGR → RGB
      ↓
MediaPipe Face Mesh
      ↓
Eye Landmarks
      ↓
Landmark Distance
      ↓
Open / Closed State

---

7. Eye-State / EEG Interaction

When the system detects closed eyes, an artificial alpha-frequency component is added to:

O1
O2

The simulated alpha activity uses:

Frequency = 10 Hz

This creates an experimental relationship between webcam-derived eye state and synthetic EEG activity.

This mechanism is intended for demonstration of multimodal interaction, not physiological inference or medical monitoring.

---

8. Motion Artifact Simulation

The prototype contains a simplified artificial artifact model.

With an approximate probability of 10%, additional Gaussian noise is added to:

Fp1
Fp2

This represents a simplified simulation of frontal EEG contamination associated with facial movement or other artifacts.

The current implementation is stochastic and is not derived from measured artifact data.

---

9. GAN Component

A preliminary Generative Adversarial Network architecture is included.

Generator

The generator receives a 100-dimensional latent vector:

100
 ↓
256
 ↓
512
 ↓
3 × 256
 ↓
Reshape
 ↓
(3, 256)

Discriminator

The discriminator receives:

(3, 256)

and uses:

Flatten
 ↓
Dense(256)
 ↓
Dense(1, sigmoid)

with Adam optimization and binary cross-entropy loss.

Current status

The GAN is currently an architectural prototype.

The current project does not include:

- a real EEG training dataset
- a GAN training loop
- trained generator weights
- generated-sample evaluation
- quantitative GAN performance metrics

Therefore, the GAN is currently a foundation for future development rather than the active EEG-generation mechanism.

---

10. User Interface

The application uses Streamlit for interactive visualization.

The interface allows the user to select:

Disorder

Normal
Epilepsy
Alzheimer
Parkinson
Stroke
Schizophrenia
Insomnia
Depression
Anxiety
Autism
Migraine

Number of channels

1–8 channels

Frequency

1–50 Hz

«The frequency control is currently present in the interface but is not yet connected to the EEG generation function.»

---

11. Input

The current system does not require a physiological EEG recording.

The main inputs are:

Number of channels
Selected condition
Frequency parameter
Webcam frames

The EEG signal itself is generated synthetically within the application.

---

12. Output

The prototype produces:

Synthetic EEG signal

A multi-channel signal containing combinations of:

- sinusoidal frequency components
- Gaussian noise
- synthetic condition-related perturbation
- simulated alpha activity
- simulated frontal artifacts

Visualization

The generated signal is displayed through the Streamlit interface as a real-time-style plot.

Data export

The project includes a "Save EEG Data" interface intended to save generated EEG data.

---

13. Technologies

- Python
- TensorFlow
- Keras
- NumPy
- Matplotlib
- Streamlit
- OpenCV
- MediaPipe

---

14. Running the Project

The main Python file is:

eeg.py

Run the Streamlit application with:

streamlit run eeg.py

The application can then be accessed through the Streamlit interface.

---

15. Reproducibility

The EEG generator contains stochastic components, including random frequency selection and Gaussian noise.

Consequently, different executions may produce different synthetic signals.

For experiments requiring deterministic results, a fixed random seed can be introduced in the future.

---

16. Advantages

The current prototype provides:

- Multi-channel EEG simulation
- Configurable channel count
- Multiple synthetic EEG frequency components
- Interactive visualization
- Webcam integration
- Computer-vision-based eye-state detection
- Eye-state-dependent alpha activity simulation
- Synthetic artifact generation
- Preliminary GAN architecture
- Interactive Streamlit interface
- A modular foundation for future EEG research and development

---

17. Limitations

Synthetic EEG

The generated signals are mathematical simulations and are not recordings from human subjects.

Simplified physiology

The current signal model does not reproduce the full physiological complexity of real EEG.

Disorder models

Only the epilepsy option currently modifies the generated signal. Other conditions are placeholders.

No clinical validation

The system has not been clinically validated and must not be used for diagnosis or medical decision-making.

Simplified eye detection

Eye state is estimated using selected facial landmarks and a fixed threshold. Performance may be affected by lighting, camera position, face orientation, and individual differences.

Simplified artifact model

Facial artifacts are simulated using randomly generated noise rather than measured EEG artifacts.

GAN not trained

The GAN architecture is defined but does not currently contain a complete training pipeline or trained weights.

Randomness

Signal generation contains stochastic components, so outputs may vary between executions.

---

18. Development Status

Component| Status
Synthetic EEG generation| Implemented
Multi-channel support| Implemented
Frequency components| Implemented
Synthetic epilepsy perturbation| Prototype implemented
Other disorder models| Planned
Streamlit interface| Implemented
Real-time visualization| Prototype implemented
Webcam integration| Implemented
Eye-state detection| Prototype implemented
Alpha response to closed eyes| Implemented
Artifact simulation| Prototype implemented
GAN architecture| Defined
GAN training| Not implemented
Real EEG dataset| Not integrated
Clinical validation| Not performed

---

19. Future Development

Potential future extensions include:

- Integration of real EEG datasets
- EEG preprocessing and filtering
- Artifact removal
- FFT and time-frequency analysis
- Evidence-based disorder-specific signal modeling
- GAN training using real EEG datasets
- Quantitative evaluation of generated EEG
- Machine-learning-based EEG classification
- More robust eye-state estimation
- Structured EEG data export
- Experiment configuration and reproducibility tools

---

20. Scientific Scope

This repository currently represents a:

«Synthetic EEG simulation and multimodal signal-processing prototype.»

It demonstrates the integration of:

Signal Simulation
       +
Computer Vision
       +
Deep Learning Architecture
       +
Interactive Visualization

The project is intended as an engineering/research prototype rather than a clinically validated EEG analysis or neurological disease detection system.

---

21. Disclaimer

This project is intended for research, educational, and engineering experimentation.

The generated signals are synthetic and should not be interpreted as measurements of actual brain activity.

The system is not intended for diagnosis, treatment, clinical monitoring, or medical decision-making.

---

22. Author

Elaheh AskariZadeh

GitHub:
https://github.com/elaheaskariii

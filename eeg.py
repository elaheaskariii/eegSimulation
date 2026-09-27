
import tensorflow as tf
import keras
from keras import layers
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
import cv2
import mediapipe as mp

# دیکشنری رنگها
channel_colors = {"Fp1": "blue", "Fp2": "blue", "T3": "green", "T4": "green", "O1": "purple", "O2": "purple",
                  "P3": "red", "P4": "red"}

# تولید سیگنال EEG چند کاناله مصنوعی
electrode_positions = ["Fp1", "Fp2", "T3", "T4", "O1", "O2", "P3", "P4"]


def generate_multichannel_eeg(channels=8, duration=10, sampling_rate=256):
    t = np.linspace(0, duration, duration * sampling_rate)
    eeg_data = {}
    eeg_freqs = {"alpha": 10, "beta": 20, "theta": 5, "delta": 2, "gamma": 40}

    for pos in electrode_positions[:channels]:
        freqs = np.random.choice(list(eeg_freqs.values()), size=3, replace=False)
        eeg_signal = np.sum([np.sin(2 * np.pi * f * t) for f in freqs], axis=0)
        eeg_data[pos] = eeg_signal + np.random.normal(0, 0.5, len(eeg_signal))
    return eeg_data


# شبیه‌سازی اختلالات EEG
def apply_disorder(eeg_data, disorder_type="epilepsy"):
    if disorder_type == "epilepsy":
        affected_channels = ["T3", "T4"]
        for channel in affected_channels:
            if channel in eeg_data:
                eeg_data[channel][::128] += 5
    # سایر اختلالات مشابه قبلی
    return eeg_data


# ساخت مدل Generator
def build_generator(latent_dim, channels=3):
    model = keras.Sequential()
    model.add(layers.Dense(256, activation="relu", input_dim=latent_dim))
    model.add(layers.Dense(512, activation="relu"))
    model.add(layers.Dense(channels * 256, activation="tanh"))
    model.add(layers.Reshape((channels, 256)))
    return model


# مدل Discriminator
discriminator = keras.Sequential([
    layers.Input(shape=(3, 256)),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

latent_dim = 100
channels = 3
generator = build_generator(latent_dim, channels)
discriminator.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
discriminator.trainable = False
gan_input = keras.Input(shape=(latent_dim,))
generated_signal = generator(gan_input)
gan_output = discriminator(generated_signal)
gan = keras.Model(gan_input, gan_output)
gan.compile(optimizer="adam", loss="binary_crossentropy")

# پردازش تصویر با MediaPipe برای تشخیص چشم و صورت
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils


def detect_eye_state(frame):
    with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                left_eye = [landmarks.landmark[33], landmarks.landmark[133]]
                right_eye = [landmarks.landmark[362], landmarks.landmark[263]]

                left_eye_open = np.linalg.norm(np.array([left_eye[0].x - left_eye[1].x, left_eye[0].y - left_eye[1].y]))
                right_eye_open = np.linalg.norm(
                    np.array([right_eye[0].x - right_eye[1].x, right_eye[0].y - right_eye[1].y]))

                # اگر فاصله بین چشم‌ها خیلی کوچک باشد، چشم‌ها بسته است
                return left_eye_open > 0.02 and right_eye_open > 0.02
        return False


# GUI با استفاده از Streamlit
st.title("Multi-Channel EEG Simulation")

disorder = st.selectbox("Select Disorder",
                        ["Normal", "Epilepsy", "Alzheimer", "Parkinson", "stroke", "Schizophrenia", "insomnia",
                         "depression", "anxiety", "autism", "migraine"])
num_channels = st.slider("Number of EEG Channels", 1, 8, 3)
frequency = st.slider("Frequency (Hz)", 1, 50, 10)

if st.button("Generate EEG in real-time", key="generate_realtime_button"):
    # وبکم فعال می‌شود
    cap = cv2.VideoCapture(0)

    generated_eeg = generate_multichannel_eeg(num_channels)
    disorder_eeg = apply_disorder(generated_eeg, disorder)

    real_time_plot = st.empty()

fig, ax = plt.subplots(num_channels, 1, figsize=(10, 8))
for i, pos in enumerate(electrode_positions[:num_channels]):
    ax[i].plot(np.arange(2560), np.zeros_like(disorder_eeg[pos]), label=pos, color=channel_colors.get(pos, "black"))

# شروع نمایش سیگنال
for i in range(1, len(disorder_eeg[pos])):
    for j, pos in enumerate(electrode_positions[:num_channels]):
        ax[j].plot(np.arange(i), disorder_eeg[pos][:i], label=pos, color=channel_colors.get(pos, "black"))
    real_time_plot.pyplot(fig)
    time.sleep(0.0000009)

    # دریافت فریم از وبکم و بررسی وضعیت چشم‌ها
    ret, frame = cap.read()
    if not ret:
        break

    # تشخیص وضعیت چشم‌ها
    eyes_closed = detect_eye_state(frame)

    if eyes_closed:
        # چشمان بسته است؛ پالس آلفا روی کانال‌های O1 و O2 اعمال می‌شود
        for channel in ["O1", "O2"]:
            if channel in disorder_eeg:
                disorder_eeg[channel] += np.sin(2 * np.pi * 10 * np.arange(len(disorder_eeg[channel])) / 256) * 2

    # نمایش آرتیفکت حرکت صورت
    if np.random.random() < 0.1:  # فرض می‌کنیم در 10% مواقع آرتیفکت حرکت صورت تولید شود
        for channel in ["Fp1", "Fp2"]:
            if channel in disorder_eeg:
                disorder_eeg[channel] += np.random.normal(0, 0.5, len(disorder_eeg[channel]))

cap.release()

if st.button("Save EEG Data", key="save_button"):
    np.savetxt("generated_eeg.csv", disorder_eeg, delimiter=",")
    st.success("EEG data saved successfully!")
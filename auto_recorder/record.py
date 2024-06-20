import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import pyaudio
import wave
import threading
import time
import subprocess
import mss

def record_video(target_window_title, output_filename, duration, fps=20):
    windows = gw.getWindowsWithTitle(target_window_title)
    if not windows:
        print(f"No window found with title: {target_window_title}")
        return
    
    window = windows[0]
    left, top, right, bottom = window.left, window.top, window.right, window.bottom
    width = right - left
    height = bottom - top

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    sct = mss.mss()
    monitor = {"top": top, "left": left, "width": width, "height": height}

    start_time = time.time()
    while True:
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        out.write(frame)
        if time.time() - start_time > duration:
            break
        time.sleep(1 / fps)
    
    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved as {output_filename}")

def record_audio(output_filename, duration, rate=44100, chunk=1024):
    audio = pyaudio.PyAudio()
    
    # Get the default input device info
    default_device_index = audio.get_default_input_device_info()["index"]
    default_device_channels = audio.get_device_info_by_index(default_device_index)["maxInputChannels"]

    stream = audio.open(format=pyaudio.paInt16, channels=default_device_channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)
    frames = []

    start_time = time.time()
    while time.time() - start_time < duration:
        data = stream.read(chunk)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(default_device_channels)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Audio saved as {output_filename}")

def record_audio_video(target_window_title, video_filename, audio_filename, duration, fps=20):
    video_thread = threading.Thread(target=record_video, args=(target_window_title, video_filename, duration, fps))
    audio_thread = threading.Thread(target=record_audio, args=(audio_filename, duration))
    
    video_thread.start()
    audio_thread.start()
    
    video_thread.join()
    audio_thread.join()
    print("Recording completed.")

def mux_audio_video(video_filename, audio_filename, output_filename):
    command = [
        'ffmpeg.exe',
        '-y',  # Overwrite output files without asking
        '-i', video_filename,
        '-i', audio_filename,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_filename
    ]
    subprocess.run(command)
    print(f"Muxed video saved as {output_filename}")

# Example usage
if __name__ == '__main__':
    target_window_title = "Discord"  # Change this to your target window title
    video_filename = "output.avi"
    audio_filename = "output.wav"
    muxed_filename = "output_muxed.mp4"
    duration = 10  # Duration in seconds
    
    record_audio_video(target_window_title, video_filename, audio_filename, duration)
    mux_audio_video(video_filename, audio_filename, muxed_filename)
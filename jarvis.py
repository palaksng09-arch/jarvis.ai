import speech_recognition as sr
import webbrowser
import subprocess
import time
import musiclibrary  # Ensure musiclibrary.py is in the same folder!

def speak(text):
    command = f'Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Speak("{text}")'
    # Using .communicate() forces Python to wait until the speech is 100% finished
    p = subprocess.Popen(['powershell', '-Command', command])
    p.communicate() 

def processcommand(c):
    command_clean = c.lower().strip()
    print(f"[Processing Command]: {command_clean}")
    
    # Using 'in' instead of '==' makes it much more forgiving if it catches extra words
    if "google" in command_clean:
        speak("Opening Google")
        # Explicitly forcing Windows to open the URL via the default system handler
        webbrowser.open_new_tab("https://www.google.com")
    elif "youtube" in command_clean:
        speak("Opening Youtube")
        webbrowser.open_new_tab("https://www.youtube.com")
    elif "facebook" in command_clean:
        speak("Opening Facebook")
        webbrowser.open_new_tab("https://www.facebook.com")
    elif "github" in command_clean:
        speak("Opening Github")
        webbrowser.open_new_tab("https://www.github.com")
    elif "play" in command_clean:
        song = command_clean.replace("play", "").strip()
        print(f"[Target Song]: '{song}'")
        
        if song in musiclibrary.music:
            speak(f"Playing {song}")
            webbrowser.open_new_tab(musiclibrary.music[song])
        else:
            speak("Song not found in your music library")

if __name__ == "__main__":
    r = sr.Recognizer()
    
    print("Adjusting for background noise... Please stand by.")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)
    
    speak("Jarvis is online and ready.")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("\nListening for wake word 'Jarvis'...")
                audio = r.listen(source, timeout=None, phrase_time_limit=4)
            
            word = r.recognize_google(audio).lower().strip()
            print(f"Heard: {word}")
            
            if "jarvis" in word:
                speak("Yes, how can I help you?")
                
                # A micro-pause to let the microphone settle down after the audio output stops
                time.sleep(0.3) 
                
                with sr.Microphone() as source:
                    print("Jarvis is listening for your command...")
                    audio = r.listen(source, timeout=6, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    print(f"Command recognized: {command}")
                    
                    processcommand(command)
                    
        except sr.UnknownValueError:
            pass
        except sr.WaitTimeoutError:
            print("[System] Command timeout. Resetting back to wake-word mode.")
            pass
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
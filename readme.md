# Audio Processing (DSP) Learning Platform 
A convenient and interactive platform designed for Digital Signal Processing (DSP) training and learning, with a strong emphasis on Audio Processing. Whether you're a beginner looking to understand the basics or an experienced developer aiming to refine your skills, this platform offers the tools and flexibility you need to explore and optimize audio effects.
<br/>


![image](https://github.com/user-attachments/assets/bb07354b-8b03-4e8e-b9b5-6f009b5f9cf5)



## Features
* **WAV File Handling**: Easily select and load WAV files, which are processed and played back as NumPy ndarray streams.
* **Effect Chain Management**: Add, remove, and manage a chain of audio effects to modify your sound in real-time.
* **Custom Effect Development**: Implement your own audio effects by adhering to a predefined interface, update the effects map, and integrate your effects seamlessly into the platform.
* **Iterative Optimization**: Continuously edit and improve your custom effects to achieve the desired audio results.
* **Spectrum Analyzer**: Visualize the frequency spectrum of your audio in real-time, helping you understand the impact of your changes and optimize your effects effectively.

## DAW Usage
1. Select a WAV File: Use the file selector on the main screen to choose a WAV file you wish to process.
2. Play Audio: Click the play button to start streaming and listening to the audio as a NumPy ndarray.
3. Add Effects: Navigate to the effects section to add desired effects to your audio chain and Use predefined effects or build your own custom effects.
4. Visualize with Spectrum Analyzer: Observe the real-time frequency spectrum of your audio to understand how your effects influence the sound.

## How to create my own Effect?
to make your own effect, first taje a look at the `AudioEffect` directory, it's a special directory where all the effects are written into, the program knows to read all the new files, to adjust all the system itself by only this directory!
1. create new `.py` file inside AudioEffects (lower case ane '_' between every word), for example `my_effect.py` (later will be showen in the program as "MyEffect").
2. inherente from `EffectInterface` class -> this class represents all the requiered features needed: `process()` and `get_effect_arguments()` (!) without these functions the system wont work!
3. inside `AudioEffect/effect_object_map.py`, add your new effet to the `effect_class_map` dict.  
4. run the program and test your DSP creation!    

## Dependencies
1. [Install Python 3.10 or higher](https://www.python.org/downloads/)
2. [Install Pip](https://pip.pypa.io/en/stable/installation/)
3. Install Rust
4. more py libs: librosa, sounddevice, matplotlib, tkinter

## Install and run
* run "python3 update.py" to run theupdate script (if you want to use the Rust libs)
* run "python3 app.py"

## resources

![image](https://github.com/user-attachments/assets/c756104d-dda5-4cdf-949f-2b1d08ad706f)



# Audio Manager

For real-time analysis, the window size (number of samples) is often chosen to balance between frequency resolution and time resolution. Common choices are powers of two because FFT algorithms are most efficient with such sizes.

* Window Size of 1024 samples gives a frequency resolution of: 44,100/1024 ~= 43.07 Hz 
* Window Size of 2048 samples gives a frequency resolution of: 44,100/2048 ~= 21.53 Hz 
* Window Size of 4096  samples gives a frequency resolution of: 44,100/4096  ~= 10.77 Hz 

(quick reminder that 1 Hz is one event per second)
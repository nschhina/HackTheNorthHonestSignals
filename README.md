# Voirate

This is an incomplete Hack the North 2017 project. Our initial idea was to create a web app which could help people perfect their presentation skills. In a perfect world, our app would have taken a presentation support file (PowerPoint, PDF), and, once the user would have been ready, would have started recording the presentation's audio content. The audio file would have then been processed by our python code using mathematical and statistical analysis of the peaks and creases in the soundwaves. These very specific and noticeable signs, which our called honest signals, can be used to determine how well a person is doing in a public speaking context.

The python file is fully functional. In order to use it, simply pass a .wav file through the scipy.io.wavfile.read function

i.e.: our_audio_file = scipy.io.wavfile.read(filename)

and let the magic happen. The code will return 3 values: Clarity (which evaluates your capicity at speaking clearly and loudly), Rhythmicity (which measures the pace of your speech and ensures that you don't go too fast, or too slow), and Emphasis/Tone (which evaluates the degree at which the high spikes in your voice volume differ from one another (marking emphasis and tone)). A clarity score of 75 and over is considered good. A Rhythmicity score above 50 is good. An Emphasis/Tone score above 40 is good.

The problems that lead to the demise of the full project were related to backend and frontend link. None of us were qualified to undertake the challenges offered by the project, and were therefore left disappointed once we understood that our project probably wouldn't come to life.

Regardless, we had fun, and are all happy to have met one another this weekend. We'd like to thank the entire organizational team.

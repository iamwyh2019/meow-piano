# meow-piano
 Code for the project "meow-piano" at RevolutionUC 2022

Try it out [at this link](https://meow-piano.tech/), but we recommend you build your own service, as our server runs too slow :(



## Introduction

Everyone loves cats, and everyone loves music. We hope to build an automated model to convert piano clips into cat singings, to produce very cute and interesting songs!

Introduction video: [youtube](https://www.youtube.com/watch?v=vgveh-92Aog)

Project link: [DevPost](https://devpost.com/software/meow-piano)



## Deployment

### Deploy the backend

First you need to have Python. Then, install the following dependencies:



1. PyTorch. Check out https://pytorch.org/
2. install `piano_transcription_inference` using pip or conda
3. download the model from the release (~120M), and put it at the folder `~/piano_transcription_inference_data/` (you may need to create it). `~` refers to your home directory. On Linux, it is usually `/home/<your-username>`; on Windows, it is usually `C:\Users\<your-username>`.
4. install `flask, flask_cors, gevent` using pip or conda
5. install `librosa` using pip or conda. Also make sure you have **ffmpeg** installed on your system.



Finally, enter the flask-backend folder, open a command prompt, and run `python main.py`.

If there's no graphic card on your device or if CUDA is not installed, change line 25 of main.py into `device='cpu'`. This could be two times slower than using CUDA.



### Deploy the frontend

If you are deploying on a server, just put the frontend-d3 folder on your www root.

If you are deploying locally, then:

1. Make sure node.js is installed. Check out https://nodejs.org/en/
2. Make sure **anywhere** is installed. To install, open a command prompt, type `npm install -g anywhere`
3. Enter the frontend-d3 folder, open a command prompt, and run `anywhere`

Also, please change the first line of `js/ui.js` to the correct backend address.




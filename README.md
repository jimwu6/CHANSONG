<h1 align="center">
  <br>
  PROJECT NAME
  <br>
</h1>

<p align="center">
  <a href="#background">Background</a> •
  <a href="#features">Features</a> •
  <a href="#acknowledgements">Acknowledgements</a> •
  <a href="#authors">Authors</a> •
  <a href="#license">License</a>
</p>

## Background
Recurrent Neural Networks are a ubiquitous tool used in NLP tasks. 

## Features
Site screenshots/description of parameters?

## Web App Usage
There is a small (functional) React app with a Flask backend, which will be moved to an actual site in the near future. To run the frontend, found in the folder rnn-genius-app, instlall the necessary packages using `npm install` and run `npm start`. To run the backend, found in the folder backend, set the `FLASK_APP` variable to `main.py` (on Unix, it is `export FLASK_APP=main.py`) and run it with `flask run`. 

## Acknowledgements
**PROJECT NAME** was built with:
* [TensorFlow 2.0](https://www.tensorflow.org/guide/keras/rnn)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [React](https://reactjs.org/)

**PROJECT NAME** is inspired by Andrej Karpathy's [blog post](http://karpathy.github.io/2015/05/21/rnn-effectiveness/?fbclid=IwAR2jDIjSieoc9ZtG_7FLN03Q3LZcUUtkw7V_4mnW0pNrelXoi6PAQsO2ffQ) on the effectiveness of recurrent neural networks.

Models were trained on a lyrics dataset scraped using the [Genius API](https://docs.genius.com/), and the (mostly) cleaned files are found [here](https://github.com/jimwu6/rnn-genius/tree/master/scraping). Some files may have non-lyric portions because Genius has text from media other than songs (e.g. interviews, concert lists). All the files have at most 84 unique characters to keep consistent while training on different datasets. 

## Authors
Made by [Jim](https://github.com/jimwu6) and [Ryan](https://github.com/ryli123). We don't know what's going on.


## License
MIT © [Jim Wu](https://github.com/jimwu6/rnn-genius/blob/master/LICENSE.md)


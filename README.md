
<div align="center">
<h1 align="center">
<p align="center">
    <img width=100% src="https://github.com/SFYLL/TweetYourClippings/blob/main/public/example.jpeg">
</p><br>
TweetYourClippings
</h1>
<h3>◦ Tweet your favorite quotes, clip by clip.</h3>
<h3>◦ Developed with the software and tools listed below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=for-the-badge&logo=GNU-Bash&logoColor=white" alt="GNU%20Bash" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="Python" />
</p>
</div>

---

## 📚 Table of Contents
- [📚 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📂 Project Structure](#-project-structure)
- [🧩 Modules](#-modules)
- [🚀 Getting Started](#-getting-started)

---


## 📍 Overview


The TweetYourClippings project allows users to easily extract and organize highlights and notes from their Kindle, convert them to various formats, and then automatically generate and tweet a random clipping image to Twitter. The project's core functionality lies in its ability to integrate several technologies (Bash, Python, PGPy, Tweepy) to automate and simplify the process of sharing reading highlights on social media. This value proposition offers a convenient solution for avid readers who want to share their favorite book quotes with their followers.

---

## 📂 Project Structure


```bash
TweetYourClippings
├── LICENSE.txt
├── README.md
├── makeclippings.sh
├── public
│   └── wallpaper.jpeg
├── requirements.txt
├── src
│   ├── ImageBuilder.py
│   ├── KindleClippings.py
│   ├── TwitterHandler.py
│   ├── encryptor.py
│   └── main.py
├── ttf
│   └── Death Note.ttf
└── tweetclippings.sh

4 directories, 12 files
```

---

## 🧩 Modules

<details closed><summary>Root</summary>

| File              | Summary                                                                                                                                                                                                                                                                                            | Module            |
|:------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------|
| tweetclippings.sh | This code snippet is a Bash script that activates a virtual environment and executes a Python script "main" with specific arguments. The Python script "main" logs data to a designated file and runs in loop of length pre-defined seconds, creating and posting tweets at each interval. | tweetclippings.sh |
| makeclippings.sh  | This Bash script has two cases: if the argument is `-d` or `--daemon`, it runs the script as a daemon and exits; otherwise, it sources a virtual environment and runs a Python script called `KindleClippings.py` with the argument `-source` directing to a Kindle documents folder. KindleClippings extracts and format your clippings, storing them in the desired location.              | makeclippings.sh  |

</details>

<details closed><summary>Src</summary>

| File               | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Module                 |
|:-------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------|
| ImageBuilder.py    | The provided code snippet defines two classes-ClippingData and ImageBuilder. ClippingData stores the data related to Kindle clippings, while ImageBuilder uses this data to generate a PNG image. The image is created using a specified font, a background image, and a randomly selected clipping from the available data. The generated image is then saved and checked against a list of previously tweeted clipping hashes to avoid duplication.                              | src/ImageBuilder.py    |
| KindleClippings.py | The provided code snippet is a Python script that extracts highlights and notes from a Kindle and organizes them into individual text files per book. It includes functions for stripping special characters from the highlights to create valid file names, converting the text files to PDF or DOCX formats, and printing the list of exported file names. The script takes command-line arguments for the source file path, destination directory, encoding, and output format. | src/KindleClippings.py |
| TwitterHandler.py  | The code includes a TwitterHandler class that handles Twitter API authentication and tweeting of images using Tweepy library. It uses an encrypted data file for secure storage of API keys, loads a private key for decryption, authenticates the user through OAuth 1.0a, and finally uploads images and creates tweets. The class takes in a ClippingData object to generate the tweet's image with a book_title.                                                               | src/TwitterHandler.py  |
| main.py            | The code snippet is a Python script that tweets generated clipping data from an image builder using the Twitter API. It uses argparse to accept command-line arguments such as seconds, key, and log file. The script sets up logging and runs periodically based on the number of seconds passed as an argument until stopped by a signal.                                                                                                                                        | src/main.py            |
| encryptor.py       | The code provides functions for encrypting and decrypting data using the PGPy library, creating PGP keys with user IDs and preferences, and writing encrypted data to files. It also includes functions for retrieving and modifying encrypted data in files using a provided password and PGP key. The main function creates a PGP key if one is not found, adds Twitter API keys to an encrypted file, and demonstrates encryption and decryption of data.                       | src/encryptor.py       |

</details>

---

## 🚀 Getting Started

### 🖥 Installation

1. Clone the TweetYourClippings repository:
```sh
git clone https://github.com/SFYLL/TweetYourClippings
```

2. Change to the project directory:
```sh
cd TweetYourClippings
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🤖 Using TweetYourClippings

```sh
python3 -m src.main
```

---
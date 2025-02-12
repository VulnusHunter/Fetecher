# Fetecher
Fetcher is a tool that extracts metadata from images and searches for social media usernames across multiple platforms. It provides both a command-line interface (CLI) and a graphical user interface (GUI) for ease of use.

Features

Extract metadata (EXIF) from images

Search for usernames on popular social media sites

Multi-threaded username crawling for faster results

Export metadata in JSON or CSV format

Simple and user-friendly GUI (Tkinter)

Installation

Clone this repository:

git clone https://github.com/VulnusHunter/fetcher.git
cd fetcher

Install the required dependencies:

pip install -r requirements.txt

Usage

CLI Mode

Run Fetcher from the command line:

python src/fetcher.py --image path/to/image.jpg

To check a username:

python src/fetcher.py --username example_user

GUI Mode

Launch the graphical interface:

python gui/gui.py

Exporting Metadata

You can export metadata in JSON or CSV format using the GUI.

Supported Platforms for Username Search

Twitter

Instagram

GitHub

Reddit

soon i will update other socials later

License

This project is licensed under the MIT License.

Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.


from urllib.request import urlopen
import os

if __name__ == "__main__":
	url = input("gimme dat newz ")
	os.system("python html_to_text.py " + url)
	
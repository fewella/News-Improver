from urllib.request import urlopen

if __name__ == "__main__":
	url = input("gimme dat newz ")
	content = urlopen(url)
	raw_html = content.read()
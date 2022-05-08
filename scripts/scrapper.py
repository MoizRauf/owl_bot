from urllib.request import urlopen
from bs4 import BeautifulSoup

def load(url):
	page = urlopen(url)
	html_bytes = page.read()
	html = html_bytes.decode("utf-8")
	soup = BeautifulSoup(html, 'html.parser')

	
	print(html)
	return html

def extract_jobs(file_name):
	with open(file_name) as fp:
		soup = BeautifulSoup(fp, 'html.parser')

		for job in soup.find_all("img", attrs={"class" : "kunden-logo"}):
			print(str(job).split("src=")[1].split("/")[-2].split(".")[0])

if __name__ == '__main__':
	extract_jobs("aboutus.html")
	quit()
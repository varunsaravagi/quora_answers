from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pdfcrowd
from selenium.webdriver.common.keys import Keys

def get_browser_html(url):
	browser = webdriver.Chrome()
	browser.get(url)
	time.sleep(3)
	body = browser.find_element_by_tag_name("body")
	#Get total answers for the question"
	#for example: 116 Answers would return 116
	total_answers = int(browser.find_element_by_class_name("answer_count").text.split(" ")[0])
	print "Total answers : ", total_answers
	loaded_answers_length = len(browser.find_elements_by_class_name("pagedlist_item"))
	#Load all the answers first.
	count = 0
	print "Loading all answers..."
	while True:		
		body.send_keys(Keys.END)
		time.sleep(3)
		loaded_answers_length_new = len(browser.find_elements_by_class_name("pagedlist_item"))
		if loaded_answers_length == loaded_answers_length_new:
			count += 1
			if count == 3:
				break
		else:
			loaded_answers_length = loaded_answers_length_new
	time.sleep(3)
	print "All answers loaded "
	html_source = browser.page_source
	return html_source,browser

urls =  ["http://www.quora.com/What-are-the-best-Python-scripts-youve-ever-written", 
	"http://www.quora.com/What-are-the-very-best-answers-on-Quora-as-chosen-by-the-Top-Writers-who-wrote-them",
	"http://www.quora.com/How-many-times-can-you-interview-with-Google-1",
	"http://www.quora.com/Im-writing-a-school-thesis-about-TDD-applied-to-web-applications-What-type-of-project-would-be-best-for-showcasing-TDD"
	]
url = urls[3]
html,browser = get_browser_html(url)
client = pdfcrowd.Client("username", "token")
file_name = url.split('/')[-1]+'.pdf'
output_file = open(file_name,'wb')
print "Converting to pdf..."
client.enableJavaScript(False)
pdf = client.convertHtml(html,output_file)
output_file.close()
print "File ", file_name, "created"
browser.close()




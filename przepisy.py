from bs4 import BeautifulSoup
from string import Template
import requests
import cherrypy

class RecipeScraper(object):

	@cherrypy.expose
	def index(self):
		return """<html>
          <head></head>
          <body>
            <form method="get" action="result">
              <input type="text" name="query" />
              <button type="submit">Szukaj!</button>
            </form>
			</body>
			</html>"""
			
	@cherrypy.expose
	def result(self, query):
	#to nie hula
	#co jest parametrem funkcji przekazywanej jako parametr?
		def is_recipe_box(tag):
			#if tag['class'][0:9] == "recipe-box":
			#	return tag
			#else:
			#	return False
			return tag['class'][0:10] == 'recipe-box' 

		url = "https://www.przepisy.pl/przepisy/szukaj/"+query
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		
		template = open("template.html", 'r').read()
		
		recipes = '<table border=1 >'
		for recipe in soup.find_all('div', class_ = 'recipe-box-5'):
			img = recipe.find('img')
			img_url = img['data-src']
			img_alt = img['alt']
			img_html = '<img src=\"' + img_url + '\"/>'
			
			title = recipe.find('span', class_ = 'title').text
			
			
			recipes += '<tr><td>' +  img_html + '</td><td>' + title + '</td></tr>'
			
		
		return template.format(content = recipes + '</table>')
		

if __name__ == '__main__':
    cherrypy.quickstart(RecipeScraper())
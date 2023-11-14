#Extraer título y descripción de preguntas recientes de Stackoverflow
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

headers = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36" 
}

url = 'https://stackoverflow.com/questions/'

respuesta = requests.get(url,headers=headers)

#BeautifulSoup al igual que html, es un parser, recibe un string de un HTML
soup = BeautifulSoup(respuesta.text)

#Primero obtengo el contenedor de las preguntas por su id
question_div : Tag = soup.find(id='questions')
#Podemos reutilizar la variable del div para hacer búsquedas relativas, la función find_all nos trae más de un elemento
#y se le puede pasar como parámetro el tipo de etiqueta que quiero que busque para ser mas precisos
divs = question_div.find_all('div',class_='s-post-summary--content')
for div in divs:
    h3 = div.find('h3').text 
    content = div.find(class_='s-post-summary--content-excerpt').text 
    content = content.replace('\n','').replace('\r','').strip() #Text beautiful
    print('\n\nPregunta:')
    print(h3)
    print(content)


#Una ventaja de utilizar este parser es que podemos encontrar elementos mediante posisiones, aquí encontramos el contenido
#moviendonos al siguiente tag que está al lado del títutlo

"""
for div in divs:
    h3_element : Tag = div.find('h3')
    h3_text = h3_element.text

    desc_element = h3_element.find_next_sibling('div') #Le decimos que encuentre el siguiente primo que sea div
    desc_text = desc_element.text
    desc_text = desc_text.replace('\n','').replace('\r','').strip()
    
    print('\n\nPregunta:')
    print(h3_text)
    print(desc_text)
"""

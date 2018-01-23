import _thread, queue, time, requests
from bs4 import BeautifulSoup
import re
import nltk
pages = set()


def getLinks(articleUrl):
    # todas las webs de wikipedia tienen la misma raiz (el artículo que queremos analizar lo pasaremos como parámetro)
    html = requests.get("http://en.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html.text, "html.parser")

    # se buscan los enlaces qde wikipedia con ayuda de una expresión regular
    links = bsObj.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

    # C) El hilo procesa la URL con BeautifulSoup y extrae nuevos links.
    for link in links:

        if "href" in link.attrs:

            # si no hemos visitado aún ese link
            if link.attrs["href"] not in pages:
                # se recoge el fragmento que nos interesa
                newPage = link.attrs["href"]

                print(newPage)

                # se añade el link a la cola
                q.put(newPage)

                # añadimos el link al conjunto de links que ya se han visitado
                pages.add(newPage)

                # se escribe en el fichero el resultado de la concatenacion de una url y su contenido
                f.write('URL-------->'+newPage+' CONTENIDO HTML-------->'+bsObj.prettify() )
                # volvemos a llamar a la función por si esta web tuviera a su vez más links
                _thread.start_new_thread(getLinks(newPage))

                time.sleep(0.5)


# se crea el fichero en que se almacenará lo obtenido en el scrapeo
f = open('resultadoMotorBusqueda.txt','w')

# se crea una cola de 100 posiciones
q = queue.Queue(100)

# "inicializamos" la cola con el primer elemento
q.put("/wiki/Wikipedia:Portada")


while not q.empty():
    # A) El programa principal extrae de la cola un link anteriormente almacenado.
    current_url = q.get()

    # B) El programa principal crea y lanza un nuevo hilo
    _thread.start_new_thread(getLinks(current_url))

    #duerme medio segundo
    time.sleep(0.5)

f.close()




# --Librerías básicas para la implementación de esta herramienta:
# from bs4 import BeautifulSoup
# import _thread, queue, time, requests
# Para crear un hilo:
# _thread.start_new_thread(<método a ejecutar>)
#  Para dormir el proceso principal medio segundo mientras se
#  ejecuta un hilo:
#  time.sleep(0.5)
#  Para crear una cola de 100:
#  q = queue.Queue(100)
#  Para añadir una URL a la cola:
#  q.put(new_url)
#  Para extraer una URL de la cola:
#  current_url = q.get()

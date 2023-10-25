from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pandas as pd
import matplotlib.pyplot as plt

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://sme.easme-web.eu/")

time.sleep(5) # aqui subir con el tiempo que necesite LOADING
# Pulsar el boton filter
element = driver.find_element('xpath', '//*[@title="Filters"]')
driver.execute_script("arguments[0].click();", element)

time.sleep(5) # no importa
# Poner texto en input
#driver.find_element('xpath','//*[@id="lookup"]').send_keys('Bio')
#driver.find_element('xpath','//*[@id="lookup"]').send_keys(Keys.RETURN)

time.sleep(3) # espera para que filtre
# Click en mostrar datos
element = driver.find_element('xpath','//*[@id="plugin-control"]/*[1]')
driver.execute_script("arguments[0].click();", element)

time.sleep(1)

# Click en descargar
element = driver.find_element('xpath', '//*[@id="button-list-dl"]')
driver.execute_script("arguments[0].click();", element)

time.sleep(5) # wait to download
#driver.close() # si ves que tarda mas en descargar, quita esta linea
#### Parte de pandas
FILE_NAME = "easme_data.csv"
df = pd.read_csv(os.environ['USERPROFILE']+"\\"+"Downloads\\"+FILE_NAME, sep=';')
df1 = df1 = df[['Country', 'Project budget']]
gk = df1.groupby('Country')
print(gk.sum()) # la suma en pantalla
# por aqui si se puede plot
#df1['Project budget'].hist()
#plt.show()
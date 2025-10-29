from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# 1. Configurar o serviço do Chrome (ele baixa e usa o driver automaticamente)
servico = Service(ChromeDriverManager().install())

# 2. Abrir o navegador Chrome
driver = webdriver.Chrome(service=servico)
driver.maximize_window() # Opcional: maximiza a janela

# 3. Acessar a URL:
driver.get("https://www.google.com")

# 4. Encontrar o campo de busca (pesquisando pelo atributo 'name="q"')
# Explicação: Inspecione o elemento da barra de busca do Google e você verá que ele tem o atributo 'name' com valor 'q'.
campo_busca = driver.find_element(By.NAME, "q")

# 5. Digitar o texto "Selenium"
campo_busca.send_keys("Selenium")

# 6. Pressionar a tecla ENTER (para pesquisar)
campo_busca.send_keys(Keys.ENTER)

# 7. (Opcional) Pausar para ver o resultado (remover em testes reais)
# O robô faz tudo muito rápido. Vamos esperar um pouco para você ver:
import time
time.sleep(5)

# 8. Fechar o navegador
driver.quit()

print("Teste de busca do Google concluído com sucesso!")
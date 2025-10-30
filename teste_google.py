from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options # NOVA IMPORTAÇÃO
import time

# --- FUNÇÃO DE TESTE RECONHECIDA PELO PYTEST ---
def test_busca_google(): 
    
    # Adicionar as opções HEADLESS para o CI/CD rodar no GitHub (sem tela)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 1. Configurar o serviço do Chrome
    # Passamos as opções de headless para o driver
    servico = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servico, options=chrome_options) # OPÇÕES ADICIONADAS
    driver.maximize_window() # Opcional: maximiza a janela

    # 3. Acessar a URL:
    driver.get("https://www.google.com")

    # 4. Encontrar o campo de busca
    campo_busca = driver.find_element(By.NAME, "q")

    # 5. Digitar o texto
    campo_busca.send_keys("Automação de Testes")

    # 6. Pressionar a tecla ENTER
    campo_busca.send_keys(Keys.ENTER)

    # 7. (Opcional) Pausar para ver o resultado (remover em testes reais)
    time.sleep(5)

    # 8. Fechar o navegador
    driver.quit()

    # O Pytest espera que o teste termine sem exceções. Não precisa de print de sucesso.
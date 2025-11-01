from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- FUNÇÃO DE TESTE RECONHECIDA PELO PYTEST ---
def test_busca_duckduckgo(): 
    
    # 1. Configurações Headless (para rodar no GitHub Actions)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1920,1080") # Garante tamanho da janela

    # 2. Configurar o serviço do Chrome
    servico = Service(ChromeDriverManager().install())
    
    # 3. Abrir o navegador Chrome
    driver = webdriver.Chrome(service=servico, options=chrome_options) 
    
    # 4. Bloco try/finally para garantir que o driver feche
    try:
        # 5. Acessar a URL do DuckDuckGo
        driver.get("https://duckduckgo.com")
        
        # 6. Lidar com o pop-up de privacidade (clicar em 'Aceitar')
        # Esperamos o botão ser clicável e clicamos nele
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "va-dialog-accept"))
        ).click()
        
        texto_busca = "Automação de Testes"

        # 7. Encontrar o campo de busca (pelo ID)
        campo_busca = driver.find_element(By.ID, "search_form_input_homepage")

        # 8. Digitar o texto
        campo_busca.send_keys(texto_busca)

        # 9. Pressionar a tecla ENTER
        campo_busca.send_keys(Keys.ENTER)
        
        # 10. Esperar pelo resultado na página de título
        # O teste espera até 10s para o título conter o texto buscado
        WebDriverWait(driver, 10).until(
            EC.title_contains(texto_busca)
        )
        
        # 11. Asserção final (Verificação de QA)
        assert texto_busca in driver.title

    finally:
        # 12. Fechar o navegador (sempre)
        # Este passo é executado mesmo se o 'assert' falhar
        driver.quit()
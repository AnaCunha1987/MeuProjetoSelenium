from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Importamos o TimeoutException para poder "capturá-lo"
from selenium.common.exceptions import TimeoutException

# --- FUNÇÃO DE TESTE RECONHECIDA PELO PYTEST ---
def test_busca_duckduckgo_passar(): 
    
    # 1. Configurações Headless
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1920,1080")

    # 2. Configurar o serviço do Chrome
    servico = Service(ChromeDriverManager().install())
    
    # 3. Abrir o navegador Chrome
    driver = webdriver.Chrome(service=servico, options=chrome_options) 
    
    try:
        # 4. Acessar a URL
        driver.get("https://duckduckgo.com")
        
        # --- 5. CORREÇÃO: TENTAR CLICAR NO POP-UP DE PRIVACIDADE ---
        try:
            # Tenta por APENAS 5 segundos encontrar o botão
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "va-dialog-accept"))
            ).click()
            print("INFO: Pop-up de privacidade encontrado e clicado.")
        except TimeoutException:
            # Se não encontrar em 5s, não faz nada e continua
            print("INFO: Pop-up de privacidade não encontrado. Continuando...")
        
        texto_busca = "Automação de Testes"

        # 6. Encontrar o campo de busca (agora deve funcionar)
        # Esperamos que a barra esteja clicável
        campo_busca = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "search_form_input_homepage"))
        )

        # 7. Digitar o texto
        campo_busca.send_keys(texto_busca)

        # 8. Pressionar a tecla ENTER
        campo_busca.send_keys(Keys.ENTER)
        
        # 9. Esperar pelo resultado na página de título
        WebDriverWait(driver, 10).until(
            EC.title_contains(texto_busca)
        )
        
        # 10. Asserção final
        assert texto_busca in driver.title
        print("SUCESSO: Título da página verificado.")

    finally:
        # 11. Fechar o navegador (sempre)
        driver.quit()
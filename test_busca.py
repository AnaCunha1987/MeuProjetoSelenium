from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- IMPORT CRÍTICO PARA O DEBUG ---
from selenium.common.exceptions import TimeoutException

# --- FUNÇÃO DE TESTE RECONHECIDA PELO PYTEST ---
def test_busca_duckduckgo(): 
    
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
        # 4. Acessar a nova URL
        driver.get("https://duckduckgo.com")
        
        texto_busca = "Automação de Testes"

        # --- PONTO DE FALHA 1: ESPERAR PELO BOTÃO DE COOKIE ---
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "va-dialog-accept"))
            ).click()
        except TimeoutException:
            print("ERRO DE DEBUG: Timeout ao esperar pelo BOTAO DE COOKIE (By.ID, 'va-dialog-accept')")
            driver.save_screenshot("debug_falha_botao_cookie.png")
            raise # Força o teste a falhar aqui
        
        # 7. Encontrar o campo de busca
        campo_busca = driver.find_element(By.ID, "search_form_input_homepage")

        # 8. Digitar o texto
        campo_busca.send_keys(texto_busca)

        # 9. Pressionar a tecla ENTER
        campo_busca.send_keys(Keys.ENTER)
        
        # --- PONTO DE FALHA 2: ESPERAR PELO TÍTULO ---
        try:
            WebDriverWait(driver, 10).until(
                EC.title_contains(texto_busca)
            )
        except TimeoutException:
            print(f"ERRO DE DEBUG: Timeout ao esperar pelo TÍTULO '{texto_busca}'")
            print(f"DEBUG: Título atual é: '{driver.title}'") 
            driver.save_screenshot("debug_falha_titulo_duck.png")
            raise # Força o teste a falhar aqui
        
        # 11. Asserção final
        assert texto_busca in driver.title

    finally:
        # 12. Fechar o navegador (sempre)
        driver.quit()
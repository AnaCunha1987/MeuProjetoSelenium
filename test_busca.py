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
# Renomeei para ficar claro que é a versão de debug
def test_busca_duckduckgo_debug(): 
    
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
        
        # 5. TENTAR CLICAR NO POP-UP DE PRIVACIDADE (Já está correto)
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "va-dialog-accept"))
            ).click()
            print("INFO: Pop-up de privacidade encontrado e clicado.")
        except TimeoutException:
            print("INFO: Pop-up de privacidade não encontrado. Continuando...")
        
        texto_busca = "Automação de Testes"

        # --- PONTO DE FALHA 1: ESPERAR PELA BARRA DE BUSCA ---
        try:
            campo_busca = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "search_form_input_homepage"))
            )
        except TimeoutException:
            print("ERRO DE DEBUG: Timeout ao esperar pela BARRA DE BUSCA (search_form_input_homepage)")
            driver.save_screenshot("debug_falha_barra_busca.png")
            raise # Força o teste a falhar aqui

        # 7. Digitar o texto
        campo_busca.send_keys(texto_busca)

        # 8. Pressionar a tecla ENTER
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
        
        # 10. Asserção final
        assert texto_busca in driver.title
        print("SUCESSO: Título da página verificado.")

    finally:
        # 11. Fechar o navegador (sempre)
        driver.quit()
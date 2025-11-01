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
def test_busca_google(): 
    
    # 1. Configurações Headless
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--window-size=1920,1080") # Definir um tamanho de janela

    # 2. Configurar o serviço do Chrome
    servico = Service(ChromeDriverManager().install())
    
    # 3. Abrir o navegador Chrome
    driver = webdriver.Chrome(service=servico, options=chrome_options) 
    
    try:
        # 4. Acessar, adicionar cookie e recarregar (como antes)
        driver.get("https://www.google.com")
        driver.add_cookie({
            "name": "CONSENT",
            "value": "YES+cb.20240101-01-p0.pt+FX+111"
        })
        driver.get("https://www.google.com")
        
        texto_busca = "Automação de Testes"

        # --- PONTO DE FALHA 1: ESPERAR PELA BARRA DE BUSCA ---
        try:
            campo_busca = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
        except TimeoutException:
            print("ERRO DE DEBUG: Timeout ao esperar pelo CAMPO DE BUSCA (By.NAME, 'q')")
            driver.save_screenshot("debug_falha_campo_busca.png")
            raise # Força o teste a falhar aqui

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
            print(f"DEBUG: Título atual é: '{driver.title}'") # Imprime o título que ele encontrou
            driver.save_screenshot("debug_falha_titulo.png")
            raise # Força o teste a falhar aqui
        
        # 11. Asserção final
        assert texto_busca in driver.title

    finally:
        # 12. Fechar o navegador (sempre)
        driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- Imports da Espera Explícita (você já tem) ---
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- FUNÇÃO DE TESTE RECONHECIDA PELO PYTEST ---
def test_busca_google(): 
    
    # 1. Configurações Headless
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")

    # 2. Configurar o serviço do Chrome
    servico = Service(ChromeDriverManager().install())
    
    # 3. Abrir o navegador Chrome
    driver = webdriver.Chrome(service=servico, options=chrome_options) 
    
    try:
        # --- INÍCIO DA CORREÇÃO DO POP-UP DE COOKIES ---
        
        # 4. Acessamos a URL primeiro (para o driver "saber" o domínio)
        driver.get("https://www.google.com")

        # 5. Adicionamos o cookie de consentimento (Isso pula o pop-up)
        # Este é um valor de consentimento genérico que diz "SIM" para o Google.
        driver.add_cookie({
            "name": "CONSENT",
            "value": "YES+cb.20240101-01-p0.pt+FX+111"
        })

        # 6. Recarregamos a página. Agora, com o cookie, o pop-up não aparecerá.
        driver.get("https://www.google.com")
        
        # --- FIM DA CORREÇÃO ---

        # 7. Encontrar o campo de busca (agora com segurança)
        # Adicionamos uma espera para garantir que a barra de busca está clicável
        campo_busca = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )

        # 8. Digitar o texto
        texto_busca = "Automação de Testes"
        campo_busca.send_keys(texto_busca)

        # 9. Pressionar a tecla ENTER
        campo_busca.send_keys(Keys.ENTER)
        
        # 10. Esperar pelo resultado (como você já fazia)
        # Agora o título VAI mudar, pois a busca funcionou
        WebDriverWait(driver, 10).until(
            EC.title_contains(texto_busca)
        )
        
        # 11. Asserção final
        assert texto_busca in driver.title

    finally:
        # 12. Fechar o navegador (sempre)
        driver.quit()
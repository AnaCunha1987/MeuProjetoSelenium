from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- IMPORTS ADICIONADOS PARA A ESPERA EXPLÍCITA ---
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# ----------------------------------------------------

# --- FUNÇÃO DE TESTE RECONHECIDA PELO PYTEST ---
def test_busca_google(): 
    
    # 1. Configurações Headless (Essenciais para o CI rodar no Ubuntu)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox") # Essencial no Linux
    chrome_options.add_argument("--disable-dev-shm-usage") # Essencial no Linux
    chrome_options.add_argument("--ignore-certificate-errors") # Adicional para estabilidade

    # 2. Configurar o serviço do Chrome
    servico = Service(ChromeDriverManager().install())
    
    # 3. Abrir o navegador Chrome
    driver = webdriver.Chrome(service=servico, options=chrome_options) 
    
    # --- MELHORIA: GARANTIR QUE O NAVEGADOR FECHE ---
    # Usamos um try/finally para garantir que o driver.quit()
    # seja chamado MESMO SE o teste falhar. Isso evita
    # que processos do Chrome fiquem "presos" no GitHub Actions.
    try:
        # 4. Acessar a URL:
        driver.get("https://www.google.com")

        # 5. Encontrar o campo de busca
        campo_busca = driver.find_element(By.NAME, "q")

        # 6. Digitar o texto
        texto_busca = "Automação de Testes"
        campo_busca.send_keys(texto_busca)

        # 7. Pressionar a tecla ENTER
        campo_busca.send_keys(Keys.ENTER)
        
        # 8. (VERIFICAÇÃO DE QA) SUBSTITUÍDA POR ESPERA EXPLÍCITA
        # Em vez de 'assert texto_busca in driver.title' (que falha se demorar)
        # Esperamos ATÉ 10 segundos para que o título contenha o texto.
        # Se não aparecer em 10s, o teste falha automaticamente.
        WebDriverWait(driver, 10).until(
            EC.title_contains(texto_busca)
        )
        
        # 9. Asserção final (opcional, mas boa prática)
        # Se a espera acima passou, o teste já é um sucesso.
        # Mas podemos manter a asserção para clareza.
        assert texto_busca in driver.title

    finally:
        # 10. Fechar o navegador
        # Este passo SEMPRE será executado, não importa o que 
        # aconteça no bloco 'try' (sucesso, falha no assert, falha na espera).
        driver.quit()
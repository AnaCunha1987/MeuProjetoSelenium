from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
# O 'import time' e o 'time.sleep' foram removidos para não atrasar o CI.

# --- FUNÇÃO DE TESTE RECONHECIDA PELO PYTEST ---
def test_busca_google(): 
    
    # 1. Configurações Headless (Essenciais para o CI rodar no Ubuntu)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox") # Essencial no Linux
    chrome_options.add_argument("--disable-dev-shm-usage") # Essencial no Linux
    chrome_options.add_argument("--ignore-certificate-errors") # Adicional para estabilidade

    # 2. Configurar o serviço do Chrome
    # Mantemos o webdriver_manager, mas se esta execução falhar,
    # significa que teremos que remover o webdriver_manager e usar um caminho estático.
    servico = Service(ChromeDriverManager().install())
    
    # 3. Abrir o navegador Chrome
    # O driver.maximize_window() foi removido, pois é desnecessário e pode falhar no headless
    driver = webdriver.Chrome(service=servico, options=chrome_options) 
    
    # 4. Acessar a URL:
    driver.get("https://www.google.com")

    # 5. Encontrar o campo de busca
    campo_busca = driver.find_element(By.NAME, "q")

    # 6. Digitar o texto
    texto_busca = "Automação de Testes"
    campo_busca.send_keys(texto_busca)

    # 7. Pressionar a tecla ENTER
    campo_busca.send_keys(Keys.ENTER)
    
    # 8. (VERIFICAÇÃO DE QA) ADIÇÃO CRÍTICA!
    # O teste SÓ passa se o título da página, após a busca, contiver o texto pesquisado.
    assert texto_busca in driver.title
    
    # 9. Fechar o navegador
    driver.quit()
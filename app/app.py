import os
import time
from platform import platform
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

class GoogleSearchBot:
    def __init__(self):
        self.retries = 5
        self.retry_delay = 5  # Segundos
        self.usuario = '45049074'
        self.clave = 'Data2025.**'
        self.Navegador = 'Chrome'  # Cambiado a Chrome por defecto

        if 'Windows' in platform():
            # self.download_folder = os.path.join(f'C:\\Users\\prueba\\Downloads')
            self.download_folder = os.path.join(f'C:\\Users\\1070968663\\Downloads')
        else:
            # Para sistemas basados en Unix (Linux, macOS)
            self.download_folder = './Downloads'

    def get_chrome_options(self):

        if self.Navegador == 'Opera':
            from selenium.webdriver.opera.options import Options as OperaOptions
            
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--start-maximized')
            options.browser_name = "opera"  # Especifica el nombre del navegador como "opera"
            _options = options
            return _options

        else:
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            
            # Configurar las preferencias de descarga
            options.add_experimental_option("prefs", {
                "download.default_directory": '/home/seluser/Downloads',   # Directorio de descarga
                "download.prompt_for_download": False,  # No preguntar por la ubicación de descarga
                "download.directory_upgrade": True,  # Actualizar el directorio de descarga si cambia
                "safebrowsing.enabled": True,  # Habilitar la navegación segura
                "safebrowsing.disable_download_protection": True,  # Deshabilitar protección de descarga
                "profile.default_content_settings.popups": 0,  # Bloquear ventanas emergentes
                "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,  # Permitir descargas automáticas
                "profile.default_content_setting_values.automatic_downloads": 1,  # Permitir descargas múltiples
            })
            _options = options

        return _options
    
    def connect_to_selenium(self):
        if 'Windows' in platform():
            self.Navegador = 'Opera'  # Cambiado a Chrome por defecto

            if self.Navegador == 'Opera':
                from selenium.webdriver.opera.options import Options as OperaOptions
                opera_options = OperaOptions()
                opera_options.binary_location = r'%s\AppData\Local\Programs\Opera\opera.exe' % os.path.expanduser('~')
                opera_options.add_argument('--start-maximized')
                self.driver = webdriver.Opera(executable_path=r'C:\dchrome\operadriver.exe', options=opera_options)
            else:
                # Use Service class for Chrome (modern approach)
                self.driver = webdriver.Chrome(executable_path=r"C:\dchrome\chromedriver.exe", options=self.get_chrome_options())

                # service = ChromeService(executable_path=r"C:\dchrome\chromedriver.exe")
                # self.driver = webdriver.Chrome(service=service, options=self.get_chrome_options())

        else:
            time.sleep(10)
            chrome_host = os.getenv('CHROME_HOST', 'localhost')
            print('este es el navegador: ',chrome_host)
            for _ in range(self.retries):
                try:
                    self.driver = webdriver.Remote(
                        command_executor=f'http://{chrome_host}:4444/wd/hub',
                        options=self.get_chrome_options()
                    )
                    return
                except Exception as e:
                    print(f"Error al conectar con Selenium: {e}")
                    print(f"Reintentando en {self.retry_delay} segundos...")
                    time.sleep(self.retry_delay)
            raise Exception("No se pudo conectar con el servidor Selenium")
    
    def login_wf(self):
        try:
            # Navigate to the login page
            self.driver.get("https://amx-res-co.etadirect.com/")
            
            # Wait for the login form to be present
            wait = WebDriverWait(self.driver, 60)
            
            # Function to perform login
            def perform_login():
                username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
                username_field.clear()
                username_field.send_keys(self.usuario)
                
                password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
                password_field.clear()
                password_field.send_keys(self.clave)
                
                # Click login button
                self.driver.execute_script('document.querySelector("#sign-in > div").click()')
            
            # Perform initial login
            perform_login()
            
            # Check for different scenarios
            max_attempts = 10
            attempt = 0
            
            while attempt < max_attempts:
                current_title = self.driver.title
                wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[@id="wait"]//div[@class="loading-animated-icon big jbf-init-loading-indicator"]')))
                attempt += 1
                time.sleep(2)
                
                # Scenario 1: Direct login successful
                if current_title == "Consola de despacho - Oracle Field Service":
                    print("entro en el if 1: ",current_title)
                    return True
                
                # Scenario 2: Existing session
                if current_title == "Oracle Field Service":
                    print("entro en el if 2: ",current_title)
                    try:
                        # Find and click the checkbox for new session
                        checkbox = wait.until(EC.presence_of_element_located((By.ID, 'delsession')))
                        checkbox.click()
                        perform_login()
                    except Exception as e:
                        print(f"Error handling existing session: {str(e)}")
                
                # Scenario 3: Password change required
                if current_title == "Cambiar contraseña - Oracle Field Service":
                    print("Error login - Cambio de contraseña requerido")
                    return False
                
                # Scenario 4: Application load error
                if current_title == "The application could not load.":
                
                    try:
                        time.sleep(2)
                        reload_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@class='user-confirm-button submit' and contains(text(),'Reload')]"))
                        )
                        reload_button.click()
                        print("Botón Reload clickeado exitosamente")
                        time.sleep(1)
                        continue
                    except Exception as e:
                        print(f"Error al hacer clic en el botón: {e}")
        
            if attempt >= 10:
                print("Error login")
                return False
            
        except Exception as e:
            error_msg = f"Error en login: {str(e)}"
            print(error_msg)
            return False

    def archivos_descargados(self, region, date_str):

        archivos_presentes = os.listdir(self.download_folder)
        encontrado = False
        # print(archivos_presentes)

        for archivo in archivos_presentes:
            print('Buscando archivo: ', archivo)
            archivo_base, extension = os.path.splitext(archivo)
            print(archivo_base)
            if extension == '.opdownload':
                archivo = archivo_base  # Elimina la extensión

            if archivo.startswith(f"Actividades-{region}") and archivo.endswith(f"{date_str}.xlsx"):
                encontrado = True
                # self.files.append(archivo)
                print(f"Archivo encontrado: {archivo}")
                break

        if not encontrado:
            return False
        return True

    def get_date_format(self, offset_days):
        """Obtiene la fecha en formato DD_MM_YY con un offset de días"""
        date = datetime.now() + timedelta(days=offset_days)
        return date.strftime("%d_%m_%y")

    def search_tree(self):

        vista_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Vista' and @aria-label='Vista']"))
        )
        # Haz clic en el botón "Vista"
        self.driver.save_screenshot('./screenshot.png')
        vista_button.click()

        checkbox = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[26]/div/div/div/div[1]/form/div/div[3]/oj-checkboxset'))
        )
        self.driver.save_screenshot('./screenshot.png')
        checkbox.click()

        # Encuentra el contenedor principal
        container = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[26]/div/div/div/div[2]'))
        )

        self.driver.save_screenshot('./screenshot.png')
        container.click()

        if 'Windows' in platform():
            button = container.find_element_by_css_selector(".app-button--cta")  # Target the 'Aplicar' button
        else:
            button = container.find_element(By.CSS_SELECTOR, ".app-button--cta")  # Target the 'Aplicar' button
            
        self.driver.save_screenshot('./screenshot.png')
        button.click()
        print("Successfully clicked the 'Aplicar' button!")

        container = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="manage-content"]/div/div[2]/div[3]/div/div[1]/table/tbody/tr[2]/td[1]/div/div/div[1]'))
        )

        list = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="manage-content"]/div/div[2]/div[2]/div/div[2]/div[3]'))
        )
        
        lista_regiones = [
            "R4-Tabasco CENTRO"
        ]
        cont = 0

        for i in [8,15,17,18,20]:
            try:
                path = f'//*[@id="manage-content"]/div/div[2]/div[2]/div/div[2]/div[3]/div[{i}]/div[1]/button[3]/span[1]'
                apply_button = WebDriverWait(list, 10).until(
                    EC.presence_of_element_located((By.XPATH, path))
                )
                region_text = apply_button.text
                self.driver.save_screenshot('./screenshot.png')

                if region_text in lista_regiones:
                    apply_button.click()
                    wait_title = 0

                    while wait_title < 5:
                        wait_title +=1
                        titulo = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, '//div[@class="page-header-description page-header-description--text"]'))
                        )

                        title_text = titulo.get_attribute('innerText')
                        if title_text == region_text:
                            print('ir a descargar')

                            for i in range(9):

                                # Calcular el offset de días: -1 para ayer, 0 para hoy, 1 para mañana, etc.
                                day_offset = i - 1
                                date_str = self.get_date_format(day_offset)

                                label = "Anterior" if i == 0 else "Siguiente"
                                button = WebDriverWait(self.driver, 30).until(
                                    EC.element_to_be_clickable((By.XPATH, f"//button[@title='{label}' and @aria-label='{label}']"))
                                )
                                button.click()
                                time.sleep(3)
                                
                                while True:
                                    acciones_button = WebDriverWait(self.driver, 30).until(
                                        EC.element_to_be_clickable((By.XPATH, "//button[@title='Acciones' and @aria-label='Acciones']"))
                                    )
                                    self.driver.save_screenshot('./screenshot.png')
                                    acciones_button.click()

                                    exportar = WebDriverWait(self.driver, 30).until(
                                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[26]/div/div/button[2]'))
                                    )
                                    self.driver.save_screenshot('./screenshot.png')
                                    exportar.click()
                                    attempts = 0
                                    while not self.archivos_descargados(region_text, date_str):
                                        print('entra a buscar...')
                                        attempts += 1
                                        if attempts > 60 : return False
                                        # self.driver.save_screenshot('./screenshot.png')
                                        time.sleep(1)
                                    break

                            break
                        time.sleep(2)

                    cont += 1
                    if cont == len(lista_regiones):
                        break

            except Exception as e:
                print(e)
                return False

        print('listo.!')
        self.TearDown()
        return True

    def TearDown(self):
        try:
            wait = WebDriverWait(self.driver, 5)
            user_menu = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'user-menu')]"))
            )
            user_menu.click()
        except Exception as e:
            return False

        time.sleep(1)
        try:
            # Intentar con el selector de clase del span que contiene el texto
            logout_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'item-caption--logout') and text()='Cerrar sesión']"))
            )
            logout_button.click()
            return True
        except Exception as e:
            print(f"Error al hacer click en cerrar sesión: {str(e)}")
            return False

    def clean_download_folder(self):
        try:
            # Verificar si la carpeta existe
            if os.path.exists(self.download_folder):
                # Listar todos los archivos en la carpeta
                for filename in os.listdir(self.download_folder):
                    # Solo procesar archivos .xlsx
                    if filename.endswith('.xlsx'):
                        file_path = os.path.join(self.download_folder, filename)
                        try:
                            # Eliminar el archivo
                            os.unlink(file_path)
                            print(f"Archivo eliminado: {filename}")
                        except Exception as e:
                            print(f'Error al eliminar {filename}: {e}')
                print("Carpeta de descargas limpiada exitosamente")
            else:
                print("La carpeta de descargas no existe")
        except Exception as e:
            print(f"Error al limpiar la carpeta de descargas: {e}")

    def validate_downloaded_files(self):
        try:
            archivos_presentes = os.listdir(self.download_folder)
            archivos_requeridos = 10
            archivos_encontrados = 0
            
            for archivo in archivos_presentes:
                if archivo.endswith('.xlsx'):
                    archivos_encontrados += 1
            
            if archivos_encontrados == archivos_requeridos:
                print(f"✅ Se encontraron los {archivos_requeridos} archivos requeridos")
                return True
            else:
                print(f"❌ Solo se encontraron {archivos_encontrados} de {archivos_requeridos} archivos requeridos")
                return False
        except Exception as e:
            print(f"Error al validar archivos: {e}")
            return False

    def save_execution_log(self, status):
        try:
            import json
            from datetime import datetime
            
            log_file = os.path.join(self.download_folder, "process_log.json")
            
            # Crear nuevo registro
            log_data = {
                "fecha_ejecucion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "estado": status,
                "usuario": self.usuario,
                "archivos_descargados": self.validate_downloaded_files()
            }
            
            # Sobrescribir el archivo con el nuevo registro
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=4)
            
            print(f"Log actualizado en: {log_file}")
            return True
        except Exception as e:
            print(f"Error al guardar el log: {e}")
            return False

    def run(self):
        max_attempt = 5
        current_attempt = 1

        # Guardar log inicial
        self.save_execution_log("EN_PROCESO")

        while current_attempt <= max_attempt:
            try:
                print(f"\n=== Intento {current_attempt} de {max_attempt} ===")
                
                self.connect_to_selenium()
                
                if not self.login_wf():
                    print('Error login - Finalizando ejecución')
                    self.save_execution_log("ERROR_LOGIN")
                    self.driver.quit()
                    return False
                
                # Limpiar la carpeta de descargas antes de comenzar
                self.clean_download_folder()
                    
                if not self.search_tree():
                    print(f'Error en la búsqueda - Intento {current_attempt}')
                    if current_attempt == max_attempt:
                        self.save_execution_log("ERROR_BUSQUEDA")
                        self.driver.quit()
                        return False
                    current_attempt += 1
                    continue
                
                # Validar archivos descargados
                if not self.validate_downloaded_files():
                    print(f'Error en la validación de archivos - Intento {current_attempt}')
                    if current_attempt == max_attempt:
                        self.save_execution_log("ERROR_VALIDACION")
                        self.driver.quit()
                        return False
                    current_attempt += 1
                    continue
                
                print('Listo termino')
                self.save_execution_log("EXITOSO")
                self.driver.quit()
                return True
                
            except Exception as e:
                print(f"Error en la ejecución - Intento {current_attempt}: {e}")
                if current_attempt == max_attempt:
                    self.save_execution_log("ERROR_GENERAL")
                    self.driver.quit()
                    return False
                current_attempt += 1
                continue

        self.driver.quit()
        return False

if __name__ == "__main__":
    bot = GoogleSearchBot()
    bot.run()
# DescargarBaseWF

Este proyecto automatiza la descarga de reportes desde Oracle Field Service (OFS) utilizando Selenium.

## Descripción

El script automatiza el proceso de:
- Login en Oracle Field Service
- Navegación a la sección de reportes
- Descarga de archivos Excel para diferentes regiones
- Validación de archivos descargados
- Registro de ejecución en archivo JSON

## Requisitos

- Python 3.x
- Selenium
- Chrome/Opera WebDriver
- Navegador Chrome u Opera instalado

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd DescargarBaseWF
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar las credenciales en `app/app.py`:
```python
self.usuario = 'TU_USUARIO'
self.clave = 'TU_CONTRASEÑA'
```

4. Configurar la ruta de descargas en `app/app.py`:
```python
self.download_folder = os.path.join(f'C:\\Users\\TU_USUARIO\\Downloads')
```

## Uso

### Ejecución Manual
```bash
python app/app.py
```

### Ejecución Automática
El script está configurado para ejecutarse cada hora mediante cron:
```
0 * * * * /scripts/script.sh
```

## Estructura del Proyecto

```
DescargarBaseWF/
├── app/
│   └── app.py           # Script principal
├── scripts/
│   ├── script.sh        # Script de ejecución
│   └── crontab.txt      # Configuración de cron
├── .gitignore
└── README.md
```

## Logs

El script genera un archivo `process_log.json` en la carpeta de descargas con el siguiente formato:
```json
{
    "fecha_ejecucion": "YYYY-MM-DD HH:MM:SS",
    "estado": "EN_PROCESO|EXITOSO|ERROR_*",
    "usuario": "USUARIO",
    "archivos_descargados": true/false
}
```

## Estados del Proceso

- `EN_PROCESO`: El proceso está en ejecución
- `EXITOSO`: El proceso se completó correctamente
- `ERROR_LOGIN`: Error en el inicio de sesión
- `ERROR_BUSQUEDA`: Error en la búsqueda de reportes
- `ERROR_VALIDACION`: Error en la validación de archivos
- `ERROR_GENERAL`: Error general en el proceso

## Notas

- El script intentará la ejecución hasta 5 veces en caso de error
- Se limpian automáticamente los archivos .xlsx antiguos antes de cada ejecución
- Se mantiene un registro de la última ejecución en process_log.json 
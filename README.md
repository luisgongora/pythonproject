# README - Script de Recopilación de Datos de Divisas desde TWS

Este script de Python te permite conectarte a la plataforma Interactive Brokers TWS (Trader Workstation) y recopilar datos de divisas en diferentes marcos de tiempo. Los datos se guardarán en un archivo Excel para su posterior análisis.

## Requisitos previos

1. TWS (Trader Workstation): Asegúrate de tener una cuenta activa en Interactive Brokers y haber descargado e instalado la plataforma TWS en tu computadora. Puedes descargar TWS desde el sitio web oficial de Interactive Brokers.

2. Python: Asegúrate de tener Python 3 instalado en tu computadora. Puedes descargar la última versión de Python desde el sitio web oficial de Python.

## Configuración de TWS

Antes de ejecutar el script, debes realizar algunos pasos de configuración en TWS:

1. Conexión a TWS: Abre TWS e inicia sesión con tu cuenta de Interactive Brokers.

2. Configuración de la conexión: Ve a la pestaña "Configuración global" en TWS y asegúrate de que esté seleccionada la opción "Configuración del sistema". En la sección "Conexion" asegúrate de tener la opción "Permitir conexiones locales" habilitada.

3. Configuración del complemento API: Ve a la sección "API" en la configuración de TWS y habilita la opción "Activar la API de TWS". Asegúrate de que el puerto de conexión sea el mismo que se especifica en el código del script (por defecto, el puerto es 7497). También, activa la opción "Leer la configuración de la API".

4. Configuración de permisos de acceso: En la sección "Permisos de API", asegúrate de que la casilla "Permitir órdenes y verificación de cuentas" esté habilitada.

## Instalación de bibliotecas requeridas

Antes de ejecutar el script, debes asegurarte de tener las bibliotecas requeridas instaladas en tu entorno de Python. Puedes instalar las bibliotecas necesarias utilizando el administrador de paquetes `pip`. Ejecuta el siguiente comando en la terminal:

```
pip install pandas ibapi
```

## Ejecución del script

Para ejecutar el script en tu entorno local, sigue estos pasos:

1. Clona este repositorio o descarga el archivo `script.py` en tu computadora.

2. Abre el archivo `script.py` en un editor de texto y revisa la configuración en la sección "Configuración del script". Asegúrate de ajustar la dirección IP y el número de puerto en `app.connect()` según la configuración de tu instancia de TWS.

3. Abre una terminal y navega hasta el directorio donde se encuentra el archivo `script.py`.

4. Ejecuta el siguiente comando para iniciar el script:

   ```
   python script.py
   ```

5. El script se conectará a TWS, realizará las suscripciones a los pares de divisas y marcos de tiempo especificados, y recopilará los datos históricos. Los datos se guardarán en un archivo Excel llamado "precios_divisas.xlsx" en el mismo directorio

.

6. El script continuará recopilando datos de forma continua, actualizando los precios cada vez que haya nuevos datos disponibles. Puedes detener la ejecución del script presionando `Ctrl+C` en la terminal.

## Soporte y contribuciones

Si tienes alguna pregunta o problema relacionado con el script, puedes crear un problema en el repositorio de GitHub o contactar al desarrollador por correo electrónico.

También, se aceptan contribuciones al código para mejorar el script. Si deseas contribuir, puedes crear un fork del repositorio, implementar tus cambios y enviar una solicitud de extracción.

## Descargo de responsabilidad

Este script se proporciona "tal cual", sin garantías de ningún tipo. El uso de este script es responsabilidad del usuario. El desarrollador no se hace responsable de ningún problema o pérdida relacionada con el uso de este script.

## Licencia

Este script se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para obtener más información.

Es importante tener en cuenta que este README es solo un ejemplo y puedes adaptarlo según tus necesidades y la estructura de tu proyecto. Asegúrate de proporcionar instrucciones claras y concisas para que otros usuarios puedan utilizar y comprender tu script correctamente.

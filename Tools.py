import pandas as pd
from notion_client import Client
from datetime import datetime
import numpy as np
import re
import emoji
import tkinter as tk
from tkinter import filedialog


TYPE = "pepito"

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# INPUT_TOOLS
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------
# Construir un bloque Callout.

def Callout(Texto, Emoji = '🏛️', Color = 'gray'):
    """
    Crea un bloque de tipo "callout" para utilizar en Notion.

    Esta función genera un diccionario que representa un bloque de tipo "callout", 
    que es un tipo de bloque utilizado en Notion para resaltar información importante. 
    Los "callouts" se caracterizan por un ícono (usualmente un emoji) al lado del texto 
    y un fondo de color que resalta el contenido del bloque.

    Parámetros:
    ----------
    Texto : str
        El texto que se mostrará dentro del bloque callout. Puede contener cualquier 
        contenido que se desee resaltar en Notion.

    Emoji : str
        Un string que representa el emoji que se mostrará al lado del texto dentro del 
        callout. Debe ser un carácter de emoji válido (por ejemplo, '📌', '⚠️', etc.). 
        Este ícono ayuda a captar la atención y a darle un contexto visual al contenido 
        del callout.

    Color : str
        Un string que especifica el color de fondo del callout. Notion acepta varios colores 
        como 'blue_background', 'pink_background', 'yellow_background', etc. Este color 
        ayuda a resaltar visualmente el callout dentro de la página.

    Retorno:
    -------
    dict
        Un diccionario que representa el bloque callout listo para ser usado en Notion. 
        Este diccionario contiene todos los elementos necesarios para definir un callout, 
        incluyendo el tipo de bloque, el texto, el ícono y el color de fondo.

    Ejemplo de uso:
    ---------------
    # Crear un callout con un texto específico, un emoji de advertencia, y un fondo amarillo:
    bloque = Callout("Este es un mensaje importante", "⚠️", "yellow_background")

    # El resultado será un diccionario que se puede enviar a la API de Notion para crear un bloque callout.
    # {
    #     "object": "block",
    #     "type": "callout",
    #     "callout": {
    #         "rich_text": [
    #             {
    #                 "type": "text",
    #                 "text": {
    #                     "content": "Este es un mensaje importante"
    #                 }
    #             }
    #         ],
    #         "icon": {
    #             "type": "emoji",
    #             "emoji": "⚠️"
    #         },
    #         "color": "yellow_background"
    #     }
    # }

    Notas:
    ------
    - El parámetro `Color` debe ser un valor válido aceptado por Notion para los colores 
      de fondo de callouts. Si se usa un valor no válido, puede que el bloque no se 
      renderice correctamente en Notion.
    - Asegúrate de usar emojis que sean visualmente claros y que transmitan la intención 
      correcta del callout para mejorar la legibilidad y la efectividad visual del bloque.

    """
    
    Bloque_Callout = {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": Texto
                    }
                }
            ],
            "icon": {
                "type": "emoji",
                "emoji": Emoji  # Cambiar el ícono por el que prefieras.
            },
            "color": f'{Color}_background'  # Cambiar el color según tus preferencias (e.g., 'blue', 'pink').
        }
    }

    return Bloque_Callout


# -----------------------------------------------------------
# Función para agregar un bloque dentro de un bloque padre (usando Key: la clave de integración para usar la API).

def Agregar_A_Notion(Key, ID_Padre, Bloque_Hijo):
    """
    Agrega un bloque hijo a un bloque padre en una página de Notion utilizando la API.

    Esta función utiliza el cliente de la API de Notion para agregar un bloque hijo a un bloque padre
    especificado. Es útil para estructurar contenido dentro de Notion, permitiendo la creación de una
    jerarquía de bloques donde los bloques hijos se anidan bajo un bloque padre.

    Parámetros:
    ----------
    Key : object
        El cliente de la API de Notion (por ejemplo, un objeto de tipo `Client` de la librería `notion`).
        Este objeto debe estar autenticado y autorizado para realizar operaciones en Notion.

    ID_Padre : str
        El identificador del bloque padre al que se quiere agregar el bloque hijo. Este ID es único para 
        cada bloque en Notion y se obtiene a través de otras operaciones de la API (como la obtención de 
        bloques de una página).

    Bloque_Hijo : dict
        Un diccionario que representa el bloque hijo que se desea agregar al bloque padre. Este diccionario 
        debe estar en el formato esperado por la API de Notion para bloques, como el que se crea mediante la 
        función `Callout` o cualquier otro tipo de bloque que se desea insertar.

    Retorno:
    -------
    dict
        La respuesta de la API de Notion después de intentar agregar el bloque hijo. La respuesta puede contener 
        detalles sobre la operación realizada y el estado actual del bloque padre, incluyendo los bloques hijos 
        ahora asociados a él.

    Ejemplo de uso:
    ---------------
    # Crear un bloque hijo (por ejemplo, un callout)
    bloque_hijo = {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Este es un bloque hijo"
                    }
                }
            ],
            "icon": {
                "type": "emoji",
                "emoji": "📌"
            },
            "color": "blue_background"
        }
    }

    # Agregar el bloque hijo al bloque padre con un ID específico
    respuesta = Agregar_A_Notion(client, "id_del_bloque_padre", bloque_hijo)

    # Imprimir la respuesta de la API
    print(respuesta)

    Notas:
    ------
    - Asegúrate de que `Key` esté correctamente autenticado y tenga permisos para modificar el contenido de Notion.
    - El ID del bloque padre debe ser un identificador válido y existente en Notion. Si el ID es incorrecto, 
      la operación fallará.
    - El bloque hijo debe estar en un formato que sea compatible con la API de Notion. Si el formato es incorrecto, 
      la API puede devolver un error.
    - La función `append` de la API de Notion puede devolver una respuesta detallada que puede incluir información 
      sobre el nuevo estado del bloque padre y los bloques hijos. Es útil revisar esta respuesta para verificar 
      que la operación se realizó correctamente.

    """
    Respuesta = Key.blocks.children.append(
        block_id=ID_Padre,
        children=[Bloque_Hijo]
    )

    return Respuesta



# -----------------------------------------------------------
# Función para agregar un bloque de texto dentro de un bloque padre.

def Bloque_Texto(Texto, Color):
    """
    Crea un bloque de tipo "paragraph" para utilizar en Notion.

    Esta función genera un diccionario que representa un bloque de tipo "paragraph" 
    para ser usado en Notion. Los bloques de párrafo son utilizados para agregar texto 
    plano a una página en Notion. Se puede personalizar el color del texto para resaltar 
    el contenido según sea necesario.

    Parámetros:
    ----------
    Texto : str
        El contenido textual que se mostrará en el bloque de párrafo. Este texto será 
        el cuerpo principal del bloque y puede ser cualquier cadena de caracteres que 
        desees mostrar en Notion.

    Color : str
        Un string que especifica el color del texto en el bloque de párrafo. Notion acepta 
        varios valores de color como 'blue_background', 'pink_background', 'yellow_background', 
        etc. Este color se aplicará como fondo del bloque de texto, permitiendo resaltar el 
        contenido del párrafo de manera visual.

    Retorno:
    -------
    dict
        Un diccionario que representa el bloque de párrafo listo para ser usado en Notion. 
        Este diccionario contiene todos los elementos necesarios para definir un bloque de 
        párrafo, incluyendo el texto y el color de fondo.

    Ejemplo de uso:
    ---------------
    # Crear un bloque de párrafo con un texto específico y un color de fondo azul:
    bloque = Bloque_Texto("Este es un párrafo importante.", "blue_background")

    # El resultado será un diccionario que se puede enviar a la API de Notion para crear un bloque de párrafo.
    # {
    #     "object": "block",
    #     "type": "paragraph",
    #     "paragraph": {
    #         "rich_text": [
    #             {
    #                 "type": "text",
    #                 "text": {
    #                     "content": "Este es un párrafo importante."
    #                 }
    #             }
    #         ],
    #         "color": "blue_background"
    #     }
    # }

    Notas:
    ------
    - El parámetro `Color` debe ser un valor válido aceptado por Notion para los colores de fondo de texto. 
      Si se usa un valor no válido, el color puede no aplicarse correctamente en Notion.
    - Asegúrate de que el `Texto` no contenga caracteres especiales que puedan causar problemas de codificación 
      al interactuar con la API de Notion.

    """
    Bloque = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": Texto
                    }
                }
            ],
            "color": Color  # Cambiar el color según tus preferencias (e.g., 'blue_background', 'pink_background').
        }
    }

    return Bloque


# -----------------------------------------------------------
# Función para obtener los bloques de la página

def Obtener_Bloques(Token, ID_Pagina):

    """
    Obtiene todos los bloques de una página en Notion, incluyendo la paginación si es necesario.

    Esta función utiliza el cliente de la API de Notion para recuperar todos los bloques hijos de una 
    página específica en Notion. La función maneja la paginación automáticamente para asegurarse de que 
    se obtengan todos los bloques, incluso si la respuesta de la API está dividida en varias páginas de 
    resultados.

    Parámetros:
    ----------
    Token : object
        El cliente de la API de Notion (por ejemplo, un objeto de tipo `Client` de la librería `notion`).
        Este objeto debe estar autenticado y autorizado para acceder a los bloques en Notion.

    ID_Pagina : str
        El identificador de la página de Notion de la cual se desean obtener los bloques. Este ID es único 
        para cada página en Notion y se obtiene a través de otras operaciones de la API (como la obtención 
        de páginas o la navegación en el espacio de trabajo).

    Retorno:
    -------
    list
        Una lista de diccionarios, donde cada diccionario representa un bloque en Notion. Cada bloque contiene 
        información sobre su tipo, contenido, y otros metadatos. La lista incluirá todos los bloques hijos 
        de la página especificada, independientemente de la cantidad de resultados.

    Ejemplo de uso:
    ---------------
    # Obtener todos los bloques de una página con un ID específico
    bloques = Obtener_Bloques(client, "id_de_la_pagina")

    # Imprimir los bloques obtenidos
    for bloque in bloques:
        print(bloque)

    Notas:
    ------
    - La función maneja la paginación automáticamente. Si la respuesta de la API contiene un cursor para 
      obtener más resultados (`has_more` y `next_cursor`), la función seguirá solicitando más bloques hasta 
      que se obtengan todos.
    - Asegúrate de que `Token` esté correctamente autenticado y tenga permisos para acceder a los bloques de 
      la página especificada.
    - La función `extend` se utiliza para añadir los resultados obtenidos a la lista `Resultados`, asegurando 
      que todos los bloques se recopilen en una sola lista.

    """
    Resultados = []
    Respuesta = Token.blocks.children.list(block_id=ID_Pagina)
    Resultados.extend(Respuesta['results'])

    # Mientras haya más bloques, sigue paginando
    while Respuesta.get('has_more'):
        Respuesta = Token.blocks.children.list(
            block_id=ID_Pagina,
            start_cursor=Respuesta['next_cursor']
        )
        Resultados.extend(Respuesta['results'])

    return Resultados


# -----------------------------------------------------------
# Función para obtener los ID y texto de los bloques de la página

def Obtener_ID_Mas_Texto_Bloques(Token, ID_Pagina, Recursivo = False, Prefijo=""):
   """
   Esta función obtiene y muestra los identificadores (IDs) y el contenido textual de los bloques de una página de Notion.
   Puede manejar de forma recursiva los bloques que tienen hijos, numerándolos de manera jerárquica.

   Parámetros:
   - Token (str): Token de autenticación para acceder a los datos de Notion.
   - ID_Pagina (str): Identificador de la página de Notion cuyos bloques se quieren procesar.
   - Recursivo (bool, opcional): Define si la función debe procesar los bloques hijos de manera recursiva. 
   Por defecto es False. Si se activa, la función llamará a sí misma para procesar los hijos de cada bloque.
   - Prefijo (str, opcional): Un prefijo utilizado para numerar los bloques de manera jerárquica (ej., '1', '1.1'). 
   Se utiliza para mantener el seguimiento de los bloques padres e hijos.

   Descripción del proceso:
   1. Obtener los bloques de la página de Notion:
      La función utiliza 'nt.Obtener_Bloques(Token, ID_Pagina)' para obtener los bloques de contenido de la página indicada.

   2. Definir los tipos de bloques que contienen texto:
      Se establece una lista llamada 'Tipos_De_Bloques_Con_texto', que incluye los tipos de bloques que se espera 
      contengan texto significativo. Ejemplos de estos bloques son `heading_1`, `paragraph`, `bulleted_list_item`, 
      entre otros.

   3. Iterar sobre todos los bloques:
      La función recorre cada bloque de la lista obtenida de Notion. Para cada bloque, se extrae su tipo, su ID y 
      se verifica si tiene hijos o no, asignando "Si" o "No" en consecuencia.

   4. Generar el prefijo para el bloque actual:
      El prefijo se usa para numerar los bloques de manera ordenada y jerárquica. Comienza con el índice del bloque 
      (iniciado en 1 para más claridad), y se concatena en caso de bloques hijos (ej. "1.1", "1.2", etc.).

   5. Verificar si el bloque contiene texto y extraer el contenido:
      Si el tipo del bloque está en `Tipos_De_Bloques_Con_texto`, se intenta extraer su contenido textual de manera segura:
      - Se accede a los elementos `rich_text` del bloque.
      - Se inicializa una lista `Contenido` para almacenar los textos encontrados.
      - Para cada elemento en `rich_text`, se verifica si contiene texto (`text`) y contenido (`content`), agregándolo a `Contenido`.
      - Si el contenido está en `plain_text`, también se agrega.
      - Los textos extraídos se combinan en una sola cadena `Contenido_Final`.

   6. Imprimir la información del bloque:
      Se imprime el ID del bloque, su tipo, el contenido textual combinado y si tiene hijos.

   7. Procesar bloques hijos de manera recursiva si aplica:
      Si `Recursivo` está habilitado y el bloque tiene hijos (`Tiene_Hijos == 'Si'`), la función llama a sí misma para 
      procesar los bloques hijos, utilizando un prefijo actualizado para reflejar la jerarquía.

   8. Manejo de errores:
      Se utilizan excepciones para capturar y manejar errores comunes (KeyError, IndexError, TypeError) que pueden ocurrir 
      durante la extracción de contenido, lo que ayuda a evitar que la función se detenga inesperadamente.

   Ejemplo de uso:
   - Para obtener e imprimir todos los bloques de una página de Notion y sus hijos de forma recursiva:
   Obtener_ID_Mas_Texto_Bloques('mi_token', 'id_de_pagina', Recursivo=True)

   La función es especialmente útil para extraer y analizar la estructura y el contenido de páginas de Notion 
   de forma automatizada y organizada.
   """
        
   # Suponiendo que nt.Obtener_Bloques es una función que devuelve los bloques de una página
   Diccionario_Bloques = Obtener_Bloques(Token, ID_Pagina)

   # Lista de tipos de bloques que se espera tengan texto.
   Tipos_De_Bloques_Con_texto = ['heading_1', 'heading_2', 'heading_3', 'paragraph', 'bulleted_list_item', 'numbered_list_item', 'callout']

   # Iterar sobre todos los bloques.
   for i in range(len(Diccionario_Bloques)):
      Bloque = Diccionario_Bloques[i]
      Tipo_Contenido = Bloque["type"]
      ID_Bloque = Bloque['id']

      # Generar el prefijo para el bloque actual
      Prefijo_Actual = f"{Prefijo}{i + 1}"  # El +1 es para empezar en 1 en lugar de 0

      if Bloque['has_children'] == True:
         Tiene_Hijos = 'Si'
      else:
         Tiene_Hijos = 'No'

      # Verificar si el tipo del bloque está en la lista de tipos esperados.
      if Tipo_Contenido in Tipos_De_Bloques_Con_texto:
         # Intentar extraer el Contenido de texto de manera segura.
         try:
               # Obtener los Elementos rich_text del bloque
               Rich_Text_Elementos = Bloque[Tipo_Contenido].get('rich_text', [])

               # Inicializar variable para almacenar el Contenido de texto
               Contenido = []

               # Extraer Contenido de texto de cada elemento rich_text
               for Elemento in Rich_Text_Elementos:
                  if 'text' in Elemento and 'content' in Elemento['text']:
                     Contenido.append(Elemento['text']['content'])
                  # Manejar otros posibles tipos de Contenido textual, si los hay
                  elif 'plain_text' in Elemento:
                     Contenido.append(Elemento['plain_text'])

               # Unir todos los contenidos extraídos en un solo texto
               Contenido_Final = ' '.join(Contenido)

               # Imprimir el Contenido del bloque actual
               print(f'Bloque {Prefijo_Actual}:')
               print(f"ID: {Bloque['id']}")
               print(f"Tipo: {Bloque['type']}")
               print(f"Contenido: {Contenido_Final}")
               print(f"Tiene hijos: {Tiene_Hijos}")
               print('\n')

               # Si el bloque tiene hijos, llamar recursivamente a la función para procesarlos
               if Tiene_Hijos == 'Si' and Recursivo == True:
                  # Llamar recursivamente a la función para procesar los bloques hijos
                  Obtener_ID_Mas_Texto_Bloques(Token, ID_Bloque, Prefijo=f"{Prefijo_Actual}.")

         except (KeyError, IndexError, TypeError) as e:
               print(f"Error al procesar el bloque con ID {Bloque['id']}: {e}")

      else:
         print(f"El bloque con ID {Bloque['id']} no es de un tipo con Contenido de texto esperado.")


# -----------------------------------------------------------
# Función para verificar los permisos del token en la página que se quiere operar.

def Verificar_Permisos_Cliente(Token, ID_Pagina):
    """
    Verifica si el cliente tiene permisos para operar sobre una página específica en Notion y permite 
    al usuario gestionar permisos si es necesario.

    Parámetros:
    ----------
    Token : object
        El cliente de la API de Notion (por ejemplo, un objeto de tipo `Client` de la librería `notion`).
        Este objeto debe estar autenticado y autorizado para acceder a Notion.

    ID_Pagina : str
        El identificador de la página de Notion que se desea verificar. Este ID es único para cada página 
        en Notion.

    Retorno:
    -------
    bool
        Retorna `True` si el cliente tiene permisos para operar sobre la página, `False` en caso contrario.

    Ejemplo de uso:
    ---------------
    # Verificar si el cliente puede operar sobre una página con un ID específico
    tiene_permisos = Verificar_Permisos_Cliente(client, "id_de_la_pagina")

    # Imprimir resultado
    if tiene_permisos:
        print("El cliente puede operar sobre la página.")
    else:
        print("El cliente NO puede operar sobre la página.")

    Notas:
    ------
    - La función realiza una solicitud simple para verificar permisos. Si el cliente tiene problemas para 
      acceder a la página, se asumirá que no tiene permisos.
    - La función solicita al usuario que confirme si el cliente tiene permisos, basado en la operación 
      de lectura que se intenta realizar.
    """

    try:
        # Intentar obtener información de la página para verificar acceso
        Respuesta = Token.pages.retrieve(page_id=ID_Pagina)
        return True
    
    except Exception as e:
        # Si ocurre un error (como un permiso denegado), informar al usuario
        print(f"Error al intentar acceder a la página: \n {e}")        
        return False

# -----------------------------------------------------------
# Función para extraer las propiedades de una página a partir de un .

def Extraer_Propiedades_Pagina(Diccionario_Pagina, Datos = ['Titulo']):
        
    """
    Procesa un elemento de tipo página en una base de datos de Notion y extrae las propiedades 
    solicitadas según la lista proporcionada.

    Esta función toma un diccionario que representa un elemento de tipo página en Notion y extrae 
    los datos específicos basados en las propiedades indicadas en el parámetro `Datos`. La extracción 
    se realiza solo para aquellas propiedades presentes en la lista `Datos`. El resultado es un 
    diccionario que contiene las claves correspondientes a las propiedades solicitadas con sus 
    respectivos valores extraídos del elemento.

    Parámetros:
    - Diccionario_Pagina (dict): Un diccionario que representa un elemento de tipo página dentro de 
    una base de datos de Notion. Este diccionario debe tener la estructura esperada, incluyendo las 
    propiedades como 'Name', 'Created', 'Tags', 'Emoji' y 'url'.
    - Datos (list): Una lista de cadenas que especifica qué propiedades del elemento de la página se 
    deben extraer. Las opciones disponibles incluyen:
        - 'Titulo': El título de la página.
        - 'ID': El identificador único del elemento de la página.
        - 'Fecha_Creacion': La fecha de creación de la página.
        - 'Tags': Los tags asociados a la página.
        - 'Link': El enlace URL a la página.
        - 'Emoji': El emoji asociado a la página.
      La lista `Datos` determina qué información se extrae y se almacena en el diccionario resultante. 
      Por defecto, la función extrae solo el 'Titulo'.

    Retorna:
    - dict: Un diccionario (`Datos_Elemento`) que contiene los datos extraídos del elemento de la página. 
    Las claves del diccionario corresponden a las propiedades solicitadas en la lista `Datos`, y los 
    valores son los datos obtenidos del elemento de la página. Si una propiedad solicitada no está presente 
    en el elemento, esa clave no se incluirá en el diccionario resultante. Las propiedades se agregan al 
    diccionario solo si están presentes en la lista `Datos`.

    Comportamiento:
    - Si `Datos` contiene 'Titulo', se extrae el título de la página. Si no se encuentra el título, se asigna 
    el valor 'Sin Título'.
    - Si `Datos` contiene 'ID', se extrae el identificador único de la página.
    - Si `Datos` contiene 'Fecha_Creacion', se extrae la fecha de creación de la página. Si la fecha de 
    creación no está disponible, se asigna el valor 'Desconocido'.
    - Si `Datos` contiene 'Tags', se extraen los tags asociados a la página. Los tags se devuelven como 
    una lista de nombres.
    - Si `Datos` contiene 'Link', se extrae el enlace URL de la página.
    - Si `Datos` contiene 'Emoji', se extrae el emoji asociado a la página.

    Ejemplo:
    Si `Datos` es `['Titulo', 'ID', 'Fecha_Creacion', 'Tags', 'Link', 'Emoji']` y el `Diccionario_Pagina` tiene 
    las propiedades correspondientes, la función retornará un diccionario con las claves 'Titulo', 'ID', 
    'Fecha_Creacion', 'Tags', 'Link' y 'Emoji', cada una con su respectivo valor extraído. Si alguno de estos 
    datos no está presente en el `Diccionario_Pagina`, esa clave no estará en el diccionario final.

    Excepciones:
    - La función asume que el `Diccionario_Pagina` tiene la estructura adecuada y que las propiedades solicitadas 
    están correctamente especificadas en la lista `Datos`. Si el `Diccionario_Pagina` no sigue la estructura 
    esperada o contiene valores no estándar, la función puede no comportarse como se espera.

    Ejemplo:
    Supongamos que `Diccionario_Pagina` es el siguiente diccionario:
    
    {
        'id': 'abc123',
        'properties': {
            'Name': {'title': [{'plain_text': 'Mi Título'}]},
            'Created': {'created_time': '2024-01-01T00:00:00Z'},
            'Tags': {'multi_select': [{'name': 'Tag1'}, {'name': 'Tag2'}]},
            'Emoji': {'rich_text': [{'text': {'content': '😊'}}]},
        },
        'url': 'https://www.notion.so/abc123'
    }
    
    Y `Datos` es `['Titulo', 'ID', 'Fecha_Creacion', 'Tags', 'Link', 'Emoji']`. La función retornará el siguiente 
    diccionario:
    
    {
        'Titulo': 'Mi Título',
        'ID': 'abc123',
        'Fecha_Creacion': {'Dia': 1, 'Mes': 1, 'Año': 2024, 'Hora': 15, 'Minuto': 45},
        'Tags': ['Tag1', 'Tag2'],
        'Link': 'https://www.notion.so/abc123',
        'Emoji': '😊'
    }

    Si `Datos` solo incluyera `['Titulo', 'ID']`, el diccionario retornado sería:

    {
        'Titulo': 'Mi Título',
        'ID': 'abc123'
    }

    """

    Datos_Elemento = {}

    # Para el título.
    if 'Titulo' in Datos:
        Titulo_Propiedad = Diccionario_Pagina['properties'].get('Name', {}).get('title', [])
        Titulo = Titulo_Propiedad[0]['plain_text'] if Titulo_Propiedad else 'Sin Título'
        Datos_Elemento['Titulo'] = Titulo
    
    # Para el ID.
    if 'ID' in Datos:
        Datos_Elemento['ID'] = Diccionario_Pagina['id']

    # Para la fecha.
    # Devuelve un diccionario con día, mes, año, hora y minuto.
    if 'Fecha_Creacion' in Datos:
        Fecha_Creacion = Diccionario_Pagina['properties'].get('Created', {}).get('created_time', 'Desconocido')

        if Fecha_Creacion != 'Desconocido':
            try:
                # Convertir la fecha a un objeto datetime.
                Fecha_Formato_Datetime = datetime.fromisoformat(Fecha_Creacion.replace('Z', '+00:00'))

                # Extraer los componentes de la fecha.
                Datos_Elemento['Fecha_Creacion'] = {
                    'Dia': Fecha_Formato_Datetime.day,
                    'Mes': Fecha_Formato_Datetime.month,
                    'Año': Fecha_Formato_Datetime.year,
                    'Hora': Fecha_Formato_Datetime.hour,
                    'Minuto': Fecha_Formato_Datetime.minute
                }

            except ValueError:
                Datos_Elemento['Fecha_Creacion'] = 'Desconocido'

        else:
            Datos_Elemento['Fecha_Creacion'] = 'Desconocido'

    # Para los tags.
    # Devuelve una lista de tags.
    if 'Tags' in Datos:
        Tags = Diccionario_Pagina['properties'].get('Tags', {}).get('multi_select', [])
        Nombres_Tags = [Tag['name'] for Tag in Tags]
        Datos_Elemento['Tags'] = Nombres_Tags

    # Para el link.
    if 'Link' in Datos:
        Link = Diccionario_Pagina['url']
        Datos_Elemento['Link'] = Link

    # Para el emoji.
    if 'Emoji' in Datos:
        Icono = Diccionario_Pagina.get('icon', {})
        if Icono.get('type') == 'emoji':
            Emoji = Icono.get('emoji', 'Sin Emoji')
            Datos_Elemento['Emoji'] = f.Limpiar_Texto_Emoji(Emoji)
        else:
            Datos_Elemento['Emoji'] = 'Sin Emoji'
    
    return Datos_Elemento


# -----------------------------------------------------------
# Función para extraer las propiedades de un elemento.

def Extraer_Propiedades_Elemento(Diccionario_Propiedades, Datos):

    """
    Extrae las propiedades especificadas de un diccionario de propiedades basado en una lista de claves solicitadas.

    Esta función toma un diccionario de propiedades y una lista de claves, y extrae los valores correspondientes 
    de acuerdo con el tipo de cada propiedad. El resultado es un diccionario que contiene las propiedades solicitadas 
    con sus valores extraídos.

    Parámetros:
    - Diccionario_Propiedades (dict): Un diccionario que contiene las propiedades de un elemento en Notion. Cada 
    propiedad tiene una clave que indica su tipo y un valor asociado.
    - Datos (list): Una lista de claves que especifica qué propiedades del diccionario de propiedades deben extraerse. 
    Las claves corresponden a los nombres de las propiedades que se buscan.

    Retorna:
    - dict: Un diccionario con las propiedades solicitadas y sus valores extraídos. Si una clave en `Datos` no 
    está presente en `Diccionario_Propiedades`, esa clave no se incluirá en el diccionario resultante.

    Ejemplo:
    Supongamos que `Diccionario_Propiedades` es el siguiente diccionario:
    ```python
    {
        'Title': {'type': 'rich_text', 'rich_text': [{'plain_text': 'Sample Title'}]},
        'Age': {'type': 'number', 'number': 30},
        'Status': {'type': 'select', 'select': {'name': 'Active'}},
        'Tags': {'type': 'multi_select', 'multi_select': [{'name': 'Tag1'}, {'name': 'Tag2'}]},
        'Date': {'type': 'date', 'date': {'start': '2024-01-01'}},
        'IsActive': {'type': 'checkbox', 'checkbox': True},
        'Website': {'type': 'url', 'url': 'https://example.com'},
        'Email': {'type': 'email', 'email': 'example@example.com'}
    }
    ```
    Y `Datos` es `['Title', 'Age', 'Tags']`. La función retornará el siguiente diccionario:
    ```python
    {
        'Title': 'Sample Title',
        'Age': 30,
        'Tags': ['Tag1', 'Tag2']
    }
    ```
    Si `Datos` incluyera `['Title', 'Email']`, el diccionario retornado sería:
    ```python
    {
        'Title': 'Sample Title',
        'Email': 'example@example.com'
    }

    """
    
    Datos_Elemento = {}

    for Clave in Datos:
        Valor = Diccionario_Propiedades.get(Clave, {})
        Tipo = Valor.get('type')
        Nombre_Clave = 'Valor'
        
        if Tipo == 'rich_text':
            Texto = Valor.get('rich_text', [{}])[0].get('plain_text', 'Sin Texto')
            Datos_Elemento[Nombre_Clave] = Texto

        elif Tipo == 'number':
            Numero = Valor.get('number', 'Sin Número')
            Datos_Elemento[Nombre_Clave] = Numero

        elif Tipo == 'select':
            Seleccion = Valor.get('select', {}).get('name', 'Sin Selección')
            Datos_Elemento[Nombre_Clave] = Seleccion

        elif Tipo == 'multi_select':
            Seleccion_Multiple = [Opcion['name'] for Opcion in Valor.get('multi_select', [])]
            Datos_Elemento[Nombre_Clave] = Seleccion_Multiple

        elif Tipo == 'date':
            Fecha = Valor.get('date', {}).get('start', 'Sin Fecha')
            Datos_Elemento[Nombre_Clave] = Fecha

        elif Tipo == 'checkbox':
            Checkbox = Valor.get('checkbox', False)
            Datos_Elemento[Nombre_Clave] = Checkbox

        elif Tipo == 'url':
            URL = Valor.get('url', 'Sin URL')
            Datos_Elemento[Nombre_Clave] = URL

        elif Tipo == 'email':
            Email = Valor.get('email', 'Sin Email')
            Datos_Elemento[Nombre_Clave] = Email

    return Datos_Elemento


# -----------------------------------------------------------
# Función para extraer datos de bases de datos (o tablas) de Notion.

def Extraer_Datos_Base_Datos_Notion(Token, ID_Base, Datos = ['Titulo']):

    """
    Extrae información de una base de datos en Notion y la devuelve en forma de una lista de diccionarios.
    
    Esta función consulta una base de datos de Notion utilizando la API de Notion y extrae datos basados en las propiedades 
    especificadas en el parámetro `Datos`. La función maneja diferentes tipos de datos y propiedades, y puede extraer información 
    de páginas y bases de datos.

    Parámetros:
    - Token (str): El token de autenticación para acceder a la API de Notion.
    - ID_Base (str): El ID de la base de datos de Notion desde la que se extraerán los datos.
    - Datos (list): Una lista de cadenas que especifica qué propiedades de los elementos se deben extraer. Las opciones incluyen 
    'Titulo', 'ID', 'Fecha_Creacion', 'Tags', y 'Link'. Por defecto, se extrae el 'Titulo'.

    Retorna:
    - list: Una lista de diccionarios, donde cada diccionario representa un elemento de la base de datos y contiene las propiedades 
    solicitadas. Cada diccionario tiene como claves los nombres de las propiedades solicitadas y sus valores correspondientes.

    Manejo de Tipos de Datos:
    - La función maneja varios tipos de propiedades de Notion, incluyendo:
        - 'rich_text': Texto enriquecido.
        - 'number': Números.
        - 'select': Selección única.
        - 'multi_select': Selección múltiple.
        - 'date': Fechas.
        - 'checkbox': Casillas de verificación.
        - 'url': URLs.
        - 'email': Correos electrónicos.

    Excepciones:
    - En caso de error al acceder a la base de datos, la función captura la excepción y muestra un mensaje de error.

    Ejemplo:

    - Código:
    Extraer_Datos_Base_Datos_Notion('mi_token', '1234567890abcdef', Datos=['Titulo', 'Link'])

    - Resultado:
    [{'Titulo': 'Página 1', 'Link': 'https://notion.so/pagina1'}, {'Titulo': 'Página 2', 'Link': 'https://notion.so/pagina2'}]

    """

    try:
        # Lista vacía para almacenar los diccionarios de datos.
        Lista_Datos = []
        Cursor_Inicial = None

        # Continuar solicitando mientras haya más elementos.
        while True:

            # Consultar los elementos dentro de la base de datos con paginación.
            Info_Base = Token.databases.query(
                database_id= ID_Base,
                start_cursor= Cursor_Inicial,
                page_size= 100  # Tamaño máximo de resultados por solicitud.
            )

            # Iterar sobre los resultados para acceder a los elementos hijos.
            for Elemento in Info_Base['results']:
                # Diccionario para almacenar los datos de la página actual.
                Datos_Elemento = {}
                # Propiedades del elemento.
                Propiedades = Elemento.get('properties', {})

                # Manejar los diferentes tipos de elementos.

                # Si el elemento es una página.
                if Elemento['object'] == 'page':
                    # Extrae los datos de la página en formato diccionario.
                    Datos_Elemento = Extraer_Propiedades_Pagina(Elemento, Datos)
                else:
                    # Agregar más propiedades de acuerdo a los tipos de datos.
                    Datos_Elemento = Extraer_Propiedades_Elemento(Propiedades, Datos)

                # Solo agregar el diccionario si contiene alguna clave.
                if Datos_Elemento:
                    Lista_Datos.append(Datos_Elemento)

            # Revisar si hay más resultados para obtener.
            if not Info_Base['has_more']:
                break
            Cursor_Inicial = Info_Base['next_cursor']

        return Lista_Datos     

    except Exception as e:
        print("Error al intentar acceder a la base de datos:", e)


# -----------------------------------------------------------
# Función para matchear nombre de las notas con el ID de Notion donde se debe insertar.

def Matcheo_Notas_Con_Base_Notion(Token, Lista_Autores, ID_Pagina, Base_Previa_Matcheo):

    """
    Matchea nombres de autores de Notion con una lista de autores de notas y actualiza una base de datos previa que
    vincula un autor tal como aparece en los recortes con un ID de Notion donde se tiene que insertar cada nota de él.

    PRECAUCIÓN Y LIMITACIÓN:
    - Solo funciona en el caso de una base de datos en Notion con los apellidos como última palabra.
    - Lo mismo con cómo aparecen los autores en la lista de autores. 

    Esta función compara los nombres de autores extraídos de una página de Notion con una lista de autores dada y actualiza
    una base de datos previa de coincidencias. Para realizar la comparación, extrae los apellidos de los autores tanto desde
    Notion como desde la lista de notas, eliminando acentos y otras variaciones ortográficas para facilitar el matcheo.

    Parámetros:
    - Token (str): El token de autenticación necesario para acceder a la API de Notion.
    - Lista_Autores (list): Una lista de nombres de autores en formato de cadena. Esta lista se comparará con los autores en Notion.
    - ID_Pagina (str): El ID de la página de Notion desde la cual se extraerán los nombres de los autores.
    - Base_Previa_Matcheo (list): Una lista de diccionarios que contiene datos de autores y sus respctivos ID donde deben
    pegarse sus notas. Esta base se actualiza con nuevas coincidencias.

    Retorna:
    - list: La lista actualizada de coincidencias entre autores de Notion y la lista de ID donde deben pegarse sus notas.

    Funcionamiento:
    1. Extrae los títulos de los bloques en la página de Notion, que corresponden a los nombres de los autores.
    2. Extrae los apellidos de los autores desde Notion y desde la lista de autores, eliminando acentos y limpiando espacios.
    3. Compara los apellidos de Notion con los apellidos de la lista y actualiza la base previa solo si el autor
       de Notion no ha sido ya listado. 
    4. Devuelve la base de datos actualizada.

    Ejemplos:
    1. Matchear autores desde Notion con una lista de autores:

        Token = 'mi_token'
        Lista_Autores = ['Gabriel García Márquez', 'Mario Vargas Llosa']
        ID_Pagina = '1234567890abcdef'
        Base_Previa_Matcheo = [{'Notion': 'Jorge Luis Borges', 'ID': '123456789dddff0abcdef'}]
        Matcheo_Notas_Con_Base_Notion(Token, Lista_Autores, ID_Pagina, Base_Previa_Matcheo)
        [{'Notion': 'Jorge Luis Borges', 'ID': '123456789dddff0abcdef'},
         {'Notion': 'Gabriel García Márquez', 'ID': '1234563523789ddgfsdgdddff0abcdef'},
         {'Notion': 'Mario Vargas Llosa', 'ID': '123456d2234789sadgsddddff0abcdef'}]

    2. Cuando no hay coincidencias, la base previa se mantiene igual:

        Lista_Autores = ['Pablo Neruda']
        Matcheo_Notas_Con_Base_Notion(Token, Lista_Autores, ID_Pagina, Base_Previa_Matcheo)
        [{'Notion': 'Jorge Luis Borges', 'ID': '123456789dddff0abcdef'}]

    3. Matchear con autores ya listados:

        Lista_Autores = ['Jorge Luis Borges']
        Matcheo_Notas_Con_Base_Notion(Token, Lista_Autores, ID_Pagina, Base_Previa_Matcheo)
        [{'Notion': 'Jorge Luis Borges', 'ID': '123456789dddff0abcdef'}]

    Consideraciones:
    - La función solo actualizará la base de coincidencias si un autor de Notion no está previamente listado.
    - Se espera que los nombres en Notion y en la lista sean similares en formato para un matcheo efectivo.
    - El manejo de nombres con acentos y variantes es clave para evitar errores en las coincidencias.

    """
    
    # Extraer títulos de los bloques de la página con el nombre que tienen, que son los autores, en este caso.
    # Queda una lista de diccionarios del tipo: 
    # Lista = [{'Titulo': Autor}]

    Titulos = Extraer_Datos_Base_Datos_Notion(Token, ID_Pagina, Datos = ['Titulo', 'ID'])

    # Extraemos la lista de autores que ya están listados.
    if Base_Previa_Matcheo != []:
        Autores_Ya_Listados = f.Extraer_Valores_Segun_Clave(Base_Previa_Matcheo, 'Notas')
    else:
        Autores_Ya_Listados = []

    # Crear lista con los apellidos de los autores tal como aparecen en Notion.
    Lista_Apellidos_Notion = []
    for i in range (0, len(Titulos)):
        Nombre = Titulos[i]['Titulo']
        Nombre = f.Eliminar_Acentos(Titulos[i]['Titulo'])
        Nombre = f.Obtener_Palabras(Nombre, -1).strip()
        Lista_Apellidos_Notion.append(Nombre)

    # Crear lista con los apellidos de los autores tal como aparecen en la lista.
    Lista_Apellidos_Lista = []
    for i in range (0, len(Lista_Autores)):
        Nombre = Lista_Autores[i]
        Nombre = f.Eliminar_Acentos(Lista_Autores[i])
        Nombre = f.Obtener_Palabras(Nombre, -1).strip()
        Lista_Apellidos_Lista.append(Nombre)

    # Matcheo.

    # Iterar sobre los apellidos de Notion.
    for i in range(0, len(Lista_Apellidos_Notion)):

        # Donde se va a linkear el nombre completo de Notion y el de la lista de autores.
        Diccionario_Matcheo = {}

        # Iterar sobre los apellidos de la lista de autores hasta encontrar coincidencia.
        k = 0
        while k < len(Lista_Apellidos_Lista):
            if Lista_Apellidos_Notion[i] == Lista_Apellidos_Lista[k]:

                # Los extraemos de las listas originales.
                Autor_ID_Final = Titulos[i]['ID']
                Autor_Lista_Final = Lista_Autores[k]

                # Los agregamos al diccionario.
                Diccionario_Matcheo['Autor'] = Autor_Lista_Final
                Diccionario_Matcheo['ID'] = Autor_ID_Final

                # Adicionamos a la base de datos de matcheo previa.
                if Autor_Lista_Final not in Autores_Ya_Listados:
                    Base_Previa_Matcheo.append(Diccionario_Matcheo)
            k = k + 1        

    return Base_Previa_Matcheo


# -----------------------------------------------------------
# Función para extraer el contenido de cada bloque basado en su tipo.

def Extraer_Contenido(Bloque, Nulos='Sin_Nulos'):
    # Inicializar un diccionario con el ID del Bloque
    Datos_Bloque = {'ID': Bloque['id'], 'Contenido': ''}

    # Identificar y extraer contenido relevante basado en el tipo de bloque.
    Tipo = Bloque['type']
    Tipos = ['paragraph', 'heading_1', 'heading_2', 'heading_3', 'bulleted_list_item', 'numbered_list_item']

    if Tipo in Tipos:
        Datos_Bloque['Contenido'] = ' '.join([Text['plain_text'] for Text in Bloque[Tipo]['rich_text']])
    # Puedes añadir más tipos de bloques aquí si es necesario.

    # Solo añadir el bloque a los resultados si el contenido no es nulo o vacío
    if Nulos == 'Sin_Nulos' and Datos_Bloque['Contenido'].strip():  # Verifica si el contenido no está vacío
        return Datos_Bloque
    elif Nulos == 'Con_Nulos': 
        return Datos_Bloque


# -----------------------------------------------------------
# Función para extraer ID y contenido de bloques de una página y formar df.

def Obtener_IDs_y_Contenido_Bloques(Token, ID_Pagina):   
     
    """
    Obtiene los IDs y el contenido (título, texto, etc.) de los bloques hijos de una página en Notion.
    Elimina automáticamente los bloques con contenido nulo o vacío.

    Parámetros:
    ----------
    Token : object
        El cliente de la API de Notion (por ejemplo, un objeto de tipo `Client` de la librería `notion`).
        Este objeto debe estar autenticado y autorizado para acceder a los bloques en Notion.

    ID_Pagina : str
        El identificador de la página de Notion de la cual se desean obtener los bloques.

    Retorno:
    -------
    pd.DataFrame
        Un DataFrame de Pandas que contiene dos columnas: 'ID' y 'Contenido'. Cada fila del DataFrame representa
        un bloque hijo de la página especificada. Los bloques con contenido nulo o vacío se excluyen del DataFrame.

    Ejemplo de uso:
    ---------------
    ids_y_contenido = Obtener_IDs_y_Contenido_Bloques(client, "id_de_la_pagina")
    for index, row in ids_y_contenido.iterrows():
        print(f"ID: {row['ID']}, Contenido: {row['Contenido']}")

    Notas:
    ------
    - La función maneja la paginación automáticamente. Si la respuesta de la API contiene un cursor para obtener
      más resultados (`has_more` y `next_cursor`), la función continuará solicitando más bloques hasta que se obtengan todos.
    - Asegúrate de que `Token` esté correctamente autenticado y tenga permisos para acceder a los bloques de la página especificada.
    - La función `Extraer_Contenido` es utilizada para obtener el contenido relevante de cada bloque y eliminar bloques con contenido vacío o nulo.
    """

    Resultados = []

    # Extraer IDs y contenido de los bloques iniciales
    Respuesta = Token.blocks.children.list(block_id=ID_Pagina)
    for Bloque in Respuesta['results']:
        Contenido = Extraer_Contenido(Bloque, Nulos='Sin_Nulos')
        if Contenido is not None:
            Resultados.append(Contenido)

    # Mientras haya más bloques, sigue paginando
    while Respuesta.get('has_more'):
        Respuesta = Token.blocks.children.list(
            block_id=ID_Pagina,
            start_cursor=Respuesta['next_cursor']
        )
        for Bloque in Respuesta['results']:
            Contenido = Extraer_Contenido(Bloque, Nulos='Sin_Nulos')
            if Contenido is not None:
                Resultados.append(Contenido)
    
    df = pd.DataFrame(Resultados)

    return df




# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# INPUT_TOOLS
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------

# Función para seleccionar una opción de una lista.

def Choose_Option(Options_List = ['Opción 1', 'Opción 2', 'Opción 3'], 
                  Prompt_Message = 'Seleccione su preferencia:', 
                  Choice_Message = 'Escriba el número de su elección:', 
                  Option_Message = 'Opción seleccionada:',
                  Invalid_Option_Message = 'Default',
                  Invalid_Input_Message = 'La opción seleccionada es inválida.',
                  First_Index = 1):
    
    print(Prompt_Message)

    for Index_Option, Option in enumerate(Options_List, First_Index):
        print(f"{Index_Option}. {Option}")

    Choice = input(Choice_Message)

    try:
        Choice = int(Choice)
        if 1 <= Choice <= len(Options_List):
            Option = Options_List[Choice - 1]
            print(f"{Option_Message} {Option}")
            return Option
        else:
            if Invalid_Option_Message == 'Default':
                print(f'La opción ingresada es inválida. Debe ser un número entre {First_Index} y {len(Options_List)}')
            else:
                print(Invalid_Input_Message)
            return Choose_Option(Options_List, Prompt_Message, Choice_Message, Option_Message, Invalid_Option_Message, Invalid_Input_Message, First_Index)  
        # Volver a pedir la elección
        
    except ValueError:
        print(Invalid_Input_Message)
        return Choose_Option(Options_List, Prompt_Message, Choice_Message, Option_Message, Invalid_Option_Message, Invalid_Input_Message, First_Index)  
    # Volver a pedir la elección
    

# Función para seleccionar una opción de una lista.

def Select_File(Explorer_Title = 'Seleccionar un archivo',
                Filetypes_Text = [("Todos los archivos", "*.*")]):    # Lista de tuplas: [("Descripción de archivo", ".extensión")]

    # Crea la ventana principal.
    Principal_Window = tk.Tk()

    # Ocultar la ventana principal.
    Principal_Window.withdraw()  

    # Asegurarse de que la ventana esté al frente.
    Principal_Window.wm_attributes('-topmost', 1)

    # Abrir el diálogo de selección de archivos de manera modal.
    File_Selected_Path = filedialog.askopenfilename(
        title= Explorer_Title,
        filetypes=Filetypes_Text       
    )
    
    # Cerrar la ventana principal después de que se selecciona el archivo
    Principal_Window.destroy()

    if File_Selected_Path:
        print(f"Selected file: {File_Selected_Path}")
        return File_Selected_Path


# Función para seleccionar una carpeta.

def Select_Directory(Explorer_Title='Seleccionar una carpeta',
                     Message_Selected_Directory = 'Selected directory:',
                     Message_Not_Selected_Directory = 'No directory selected'):

    # Crear la ventana principal.
    Principal_Window = tk.Tk()

    # Ocultar la ventana principal.
    Principal_Window.withdraw()  

    # Asegurarse de que la ventana esté al frente.
    Principal_Window.wm_attributes('-topmost', 1)

    # Abrir el diálogo de selección de carpetas de manera modal.
    Directory_Selected_Path = filedialog.askdirectory(
        title=Explorer_Title
    )
    
    # Cerrar la ventana principal después de que se selecciona la carpeta.
    Principal_Window.destroy()

    if Directory_Selected_Path:
        print(f"{Message_Selected_Directory} {Directory_Selected_Path}")
        return Directory_Selected_Path
    else:
        print(Message_Not_Selected_Directory)
        return None


# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# OTHER_TOOLS
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------

def Eliminar_Texto_Entre_Caracteres(Texto, Primer_Caracter, Segundo_Caracter):

    # Crear el patrón de expresión regular.
    Patron = rf'\{Primer_Caracter}.*?\{Segundo_Caracter}'

    # Reemplazar el texto entre los caracteres por un espacio, incluyendo los caracteres mismos.
    return re.sub(Patron, '', Texto)

# -----------------------------------------------------------
# Función para borrar texto dentro de otro texto.

def Borrar_En_String(Texto, Texto_A_Borrar):
    if Texto_A_Borrar in Texto:
        Texto = Texto.replace(Texto_A_Borrar, "")
    
    return Texto

def Borrar_En_String(Texto, Caracteres):
    for Caracter in Caracteres:
        Texto = Texto.replace(Caracter, '')
    return Texto

# -----------------------------------------------------------
# Función para editar el texto del highlight. Hay que tunearla.

def Procesar_Texto(Texto, Borrar_Caracteres = True): 

    # Borrar caracteres numéricos y otros caracteres no deseados
    if Borrar_Caracteres == True:
        Caracteres_A_Borrar = '0123456789«»[]'
        Texto = Borrar_En_String(Texto, Caracteres_A_Borrar)

    # Mayúscula en el primer carácter
    Texto = Texto[0].upper() + Texto[1:]

    # Mayúscula en el segundo carácter si el primero es '¿' o '¡'
    Comun_First_Character = ['¿', '¡', f'"', f"'", '«', '-', '_', '—', '.', ',', ':', '(', ')', '?', '!']

    # Verifica si el texto comienza con uno de los caracteres especiales.
    if Texto and Texto[0] in Comun_First_Character:
        if len(Texto) > 1:
            # Capitaliza el segundo carácter
            Texto = Texto[0] + Texto[1].upper() + Texto[2:]

    # Eliminar espacios al principio y al final
    Texto = Texto.strip()

    # Eliminar espacios internos adicionales.
    Texto = re.sub(r'\s+', ' ', Texto)

    # Eliminar el último carácter si termina en ':' o ';'
    if Texto.endswith((':', ';', ',')):
        Texto = Texto[:-1]

    # Agregar punto final si el texto no termina en . ? !
    if not Texto.endswith(('.', '?', '!')):
        Texto += '.'
    
    # Convertir a mayúsculas el primer carácter después de "? " o "! "
    Texto = re.sub(r'([? !]\s)([a-z])', lambda m: m.group(1) + m.group(2).upper(), Texto)
    
    return Texto

# -----------------------------------------------------------
# Función para encontrar la posición del último carácter de un texto dentro de otro texto.

def Posicion_Ultimo_Caracter(Cadena, Subcadena):
    return Cadena.find(Subcadena) + len(Subcadena)


# -----------------------------------------------------------
# Función para extraer el autor de la línea.

def Extraer_Autor(Linea):
    i = 0
    while Linea[i] != "(":
        i = i + 1
    Autor = Linea[i+1:len(Linea)-1]
    return Autor

# -----------------------------------------------------------
# Función para extraer el autor de la línea.

def Extraer_Libro(Linea):
    Linea = Borrar_En_String(Linea, '\ufeff')
    i = 0
    while Linea[i] != "(":
        i = i + 1
    Libro = Linea[:i-1]
    return Libro

# -----------------------------------------------------------
# Función para extraer la página de la línea.

def Extraer_Pagina(Linea):

    Texto = '- Tu subrayado en la página '

    # Encontrar posición del primer dígito de la página.
    Primer_Digito = Posicion_Ultimo_Caracter(Linea, Texto)

    # Encontrar posición del último dígito de la página.
    # find() encuentra la primera posición del texto posterior.
    Ultimo_Digito = Linea.find(' | posición ') - 1

    Pagina = Linea[Primer_Digito:Ultimo_Digito]

    return Pagina

# -----------------------------------------------------------
# Función para extraer el día de la semana de la línea.

def Extraer_Dia_Semana(Linea):

    Dia_Semana = ''

    Texto = ' | Añadido el '

    # Encontrar posición de la primer letra del día.
    Primera_Letra = Posicion_Ultimo_Caracter(Linea, Texto)
    Segunda_Letra = Primera_Letra + 1
    Dos_Letras = Linea[Primera_Letra] + Linea[Segunda_Letra]

    if Dos_Letras == 'lu':
        Dia_Semana = 'Lunes'
    elif Dos_Letras == 'ma':
        Dia_Semana = 'Martes'
    elif Dos_Letras == 'mi':
        Dia_Semana = 'Miércoles'
    elif Dos_Letras == 'ju':
        Dia_Semana = 'Jueves'
    elif Dos_Letras == 'vi':
        Dia_Semana = 'Viernes'
    elif Dos_Letras == 'sa':
        Dia_Semana = 'Sábado'
    elif Dos_Letras == 'do':
        Dia_Semana = 'domingo'
        
    return Dia_Semana

# -----------------------------------------------------------
# Función para extraer el día de la línea.

def Extraer_Dia(Linea):
    # Extraer día en minúsculas.
    Dia = Extraer_Dia_Semana(Linea).lower()

    # Encontrar posición de la primer letra del día.
    Primer_Digito = Posicion_Ultimo_Caracter(Linea, Dia) + 2

    # Encontrar posición del último dígito de la página.
    # find() encuentra la primera posición del texto posterior.
    Ultimo_Digito = Linea.find(' de ')

    Dia = Linea[Primer_Digito:Ultimo_Digito]

    return Dia

# -----------------------------------------------------------
# Función para extraer el mes de la línea.

def Extraer_Mes(Linea):
    Meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    for Mes in Meses:
        if Mes in Linea:
            Mes_Final = Mes

    Mes_Final = Mes_Final.capitalize()

    return Mes_Final

# -----------------------------------------------------------
# Función para extraer el año de la línea.

def Extraer_Ano(Linea):
    Anos = np.arange(1900,2100)
    Anos = Anos.tolist()

    for i in range (0, len(Anos)):
        Ano = str(Anos[i])
        if Ano in Linea:
            Ano_Final = Ano
    return Ano_Final

# -----------------------------------------------------------
# Función para extraer la hora de la línea.

def Extraer_Hora(Linea):
    Texto = ':'

    # Encontrar posición de los digitos de la hora.
    Primer_Digito = Posicion_Ultimo_Caracter(Linea, Texto) - 3

    # En el caso de que solo tenga un dígito la hora.
    if Linea[Primer_Digito] == ' ':
        Primer_Digito = Posicion_Ultimo_Caracter(Linea, Texto) - 2

    Ultimo_Digito = Posicion_Ultimo_Caracter(Linea, Texto) + 2

    Hora = Linea[Primer_Digito:Ultimo_Digito]

    return Hora

# -----------------------------------------------------------
# Función para armar la nota.

def Armar_Nota(Lista_Lineas):
    Separacion = '=========='
    Lista_Notas = []

    i = 0
    while i < len(Lista_Lineas):
        Diccionario = {}    
        Diccionario['Autor'] = Extraer_Autor(Lista_Lineas[i])
        Diccionario['Libro'] = Extraer_Libro(Lista_Lineas[i])
        Diccionario['Pagina'] = Extraer_Pagina(Lista_Lineas[i + 1])
        Diccionario['Dia de la semana'] = Extraer_Dia_Semana(Lista_Lineas[i + 1])
        Diccionario['Dia'] = Extraer_Dia(Lista_Lineas[i + 1])
        Diccionario['Mes'] = Extraer_Mes(Lista_Lineas[i + 1])
        Diccionario['Año'] = Extraer_Ano(Lista_Lineas[i + 1])
        Diccionario['Hora'] = Extraer_Hora(Lista_Lineas[i + 1])
        i = i + 3

        Lista_Lineas_Highlight = []

        while Lista_Lineas[i] != Separacion:
            Lista_Lineas_Highlight.append(Lista_Lineas[i])
            i = i + 1
        
        # Convertir a string con comas como separador
        Highlight = ' '.join(map(str, Lista_Lineas_Highlight))
        
        # Guardar highlight en diccionario.
        Diccionario['Highlight'] = Highlight
        
        Lista_Notas.append(Diccionario)
        i = i + 1
    
    return Lista_Notas


# -----------------------------------------------------------
# Función para eliminar emojis de un texto.

def Limpiar_Texto_Emoji(Texto_Emoji, Condicion = 'Mantener'):
    """
    Procesa un texto para mantener solo los emojis o eliminar todos los emojis, según la condición especificada.

    La función utiliza expresiones regulares para identificar emojis dentro del texto y permite dos opciones de 
    procesamiento basado en el parámetro `Condicion`. Puede mantener solo los emojis presentes en el texto o 
    eliminar todos los emojis, dejando solo los caracteres no emoji.

    Parámetros:
    - Texto_Emoji (str): Una cadena de texto que contiene emojis y otros caracteres. Esta cadena será procesada 
      según la condición especificada para extraer o eliminar los emojis.
    - Condicion (str, opcional): Define el comportamiento de la función. Puede ser uno de los siguientes valores:
      - 'Mantener': Solo se conservarán los emojis en el texto. El resto de los caracteres serán eliminados.
      - 'Borrar': Todos los emojis serán eliminados del texto, dejando solo los caracteres no emoji. Por defecto, 
        se establece en 'Mantener'.

    Retorna:
    - str: Una cadena de texto resultante después de aplicar la condición especificada. Dependiendo del valor de 
      `Condicion`, el resultado contendrá solo emojis o estará libre de emojis.

    Comportamiento:
    - Si `Condicion` es 'Mantener':
      - El texto original se limpia de los caracteres especiales `♀️` y `♂️`, ya que estos son combinaciones de emoji que 
        pueden no ser correctamente identificadas por la expresión regular.
      - Se busca y extrae solo los emojis presentes en el texto utilizando la expresión regular `Textos_Emojis`. Todos 
        los caracteres no emoji se eliminan.
      - El resultado es una cadena que contiene únicamente los emojis encontrados en el texto original.

    - Si `Condicion` es 'Borrar':
      - Se utilizan las funciones de la expresión regular para reemplazar todos los emojis en el texto con una cadena vacía.
      - El resultado es una cadena que contiene solo los caracteres no emoji, ya que los emojis han sido eliminados.

    Ejemplo:
    - Si `Texto_Emoji` es 'Hola 🌍! Cómo estás? 🤔' y `Condicion` es 'Mantener', la función devolverá '🌍🤔'.
    - Si `Texto_Emoji` es 'Hola 🌍! Cómo estás? 🤔' y `Condicion` es 'Borrar', la función devolverá 'Hola ! Cómo estás? '.

    Excepciones:
    - La función asume que el parámetro `Condicion` será una cadena válida ('Mantener' o 'Borrar'). Valores diferentes 
      a estos pueden provocar comportamientos inesperados.
    - El código no maneja casos en los que el texto puede contener emojis complejos o combinaciones especiales que no 
      están cubiertas por la expresión regular proporcionada.

    """

    # Expresión regular para emojis.
    Textos_Emojis = re.compile(
        "["  # Empezar con
        "\U0001F600-\U0001F64F"  # Emoticonos
        "\U0001F300-\U0001F5FF"  # Símbolos y pictogramas
        "\U0001F680-\U0001F6FF"  # Transporte y mapas
        "\U0001F700-\U0001F77F"  # Símbolos de alquimia
        "\U0001F780-\U0001F7FF"  # Geometría
        "\U0001F800-\U0001F8FF"  # Símbolos de utilidad
        "\U0001F900-\U0001F9FF"  # Símbolos adicionales
        "\U0001FA00-\U0001FA6F"  # Símbolos adicionales
        "\U0001FA70-\U0001FAFF"  # Símbolos adicionales
        "\U00002702-\U000027B0"  # Símbolos de mejora
        "\U000024C2-\U0001F251"  # Símbolos adicionales
        "]+", 
        flags=re.UNICODE)

    if Condicion == 'Mantener':
        # Buscar todos los emojis en el texto y unirlos en una sola cadena
        Texto_Emoji = Texto_Emoji.replace("♀️", "").replace("♂️", "")
        return ''.join(Textos_Emojis.findall(Texto_Emoji))
    
    elif Condicion == 'Borrar':
        # Reemplazar el emoji y borrarlo.
        return Textos_Emojis.sub('', Texto_Emoji)
    
    else:
        return print(f"El segundo parámetro deben ser las cadenas de texto 'Mantener' o 'Borrar'")
    

# -----------------------------------------------------------
# Función para extraer autores o libros de la nota.

def Extraer_Datos_Nota(Ruta_Archivo, Dato_A_Extraer = 'Autores'):

    """
    Esta función procesa un archivo de texto para extraer datos específicos.
    Dependiendo del parámetro `Dato_A_Extraer`, devuelve autores, libros o ambos.

    Parámetros:
    ----------
    Ruta_Archivo : str
        Ruta completa del archivo de texto que contiene la información.
        Debe estar en formato de texto y utilizar codificación UTF-8.

    Dato_A_Extraer : str, opcional, por defecto 'Autores'
        Tipo de datos a extraer:
        - 'Autores': Devuelve una lista de autores únicos.
        - 'Libros': Devuelve una lista de libros únicos.
        - 'Ambos': Devuelve una lista de diccionarios con pares autor-libro.

    Retorna:
    -------
    list
        - Si `Dato_A_Extraer` es 'Autores': Lista de autores únicos.
        - Si `Dato_A_Extraer` es 'Libros': Lista de libros únicos.
        - Si `Dato_A_Extraer` es 'Ambos': Lista de diccionarios con autor y libro.

    Errores:
    -------
    FileNotFoundError
        - Imprime un mensaje si el archivo no se encuentra en la ruta proporcionada y devuelve una lista vacía.
    Exception
        - Imprime un mensaje si ocurre un problema durante el procesamiento y devuelve una lista vacía.

    Ejemplo:
    --------
    Supongamos que tenés un archivo de texto llamado 'datos.txt' con el siguiente contenido:
    
    Autor: Gabriel García Márquez
    Libro: Cien años de soledad
    Nota

    Autor: Jorge Luis Borges
    Libro: El Aleph
    Nota

    Autor: Gabriel García Márquez
    Libro: El otoño del patriarca
    Nota

    Llamada a la función:
    ---------------------
    Extraer_Datos_Nota('datos.txt', 'Autores')
    Devuelve:
    ['Gabriel García Márquez', 'Jorge Luis Borges']

    Extraer_Datos_Nota('datos.txt', 'Libros')
    Devuelve:
    ['Cien años de soledad', 'El Aleph', 'El otoño del patriarca']

    Extraer_Datos_Nota('datos.txt', 'Ambos')
    Devuelve:
    [{'Autor': 'Gabriel García Márquez', 'Libro': 'Cien años de soledad'},
     {'Autor': 'Jorge Luis Borges', 'Libro': 'El Aleph'},
     {'Autor': 'Gabriel García Márquez', 'Libro': 'El otoño del patriarca'}]

    """

    try:
        # Abre el archivo de texto en modo lectura con codificación UTF-8.
        with open(Ruta_Archivo, 'r', encoding='utf-8') as Archivo:
            # Lee todo el contenido del archivo.
            Contenido = Archivo.read()

        # Divide el contenido en una lista de líneas.
        Lista_Lineas = Contenido.splitlines()

        # Procesa las líneas del archivo para extraer notas y datos.
        Notas = Armar_Nota(Lista_Lineas)

        # Crea un DataFrame de pandas a partir de los datos procesados.
        df = pd.DataFrame(Notas)

        # Extracción de datos.

        # Si se quieren extraer autores.
        if Dato_A_Extraer == 'Autores':
            # Extrae los nombres de los autores únicos de la columna 'Autor'.
            Autores = df['Autor'].unique()

            # Devuelve la lista de autores únicos.
            return Autores.tolist()
        
        # Si se quieren extraer libros.
        if Dato_A_Extraer == 'Libros':
            # Extrae los nombres de los libros únicos de la columna 'Libro'.
            Libros = df['Libro'].unique()

            # Devuelve la lista de libros únicos.
            return Libros.tolist()
        
        # Si se quieren extraer ambos.
        if Dato_A_Extraer == 'Ambos':

            # Lista vacía donde se van a almacenar diccionarios del tipo: 
            # {Autor: ---, 
            # Libro: ----}
            Lista_Libros_Autores = []

            # Extrae los nombres de los libros únicos de la columna 'Libro'.
            Libros = df['Libro'].unique()

            # Iteramos por cada libro.
            for i in range(0, len(Libros)):
                
                # Diccionario vacío que va a tener los dos datos.
                Diccionario = {}
                k = 0

                # Mientras el elemento de la columna 'Libro' del df sea distinto al primer libro de la lista, itera.
                while df['Libro'][k] != Libros[i]:
                    k = k + 1
                
                # Al encontrar la posición primera, generamos un diccionario con ese libro y ese autor.
                Diccionario['Autor'] = df['Autor'][k]
                Diccionario['Libro'] = df['Libro'][k]
                Lista_Libros_Autores.append(Diccionario)
            
            return Lista_Libros_Autores

    except FileNotFoundError:
        print(f"Error: \n",
              f"El archivo en la ruta '{Ruta_Archivo}' no fue encontrado.")
        return []
    except Exception as e:
        print(f"Error: \n",
              f"Ocurrió un problema al procesar el archivo. {e}")
        return []
    

# -----------------------------------------------------------
# Función para eliminar acentos.

def Eliminar_Acentos(Texto):

    """
    Esta función elimina los acentos de las letras en una cadena de texto.

    Parámetros:
    ----------
    Texto : str
        La cadena de texto de entrada en la que se eliminarán los acentos.

    Retorna:
    -------
    str
        La cadena de texto con los acentos eliminados.

    Descripción:
    ------------
    La función toma un texto y reemplaza las vocales acentuadas por sus versiones sin acento:
    - 'á' se convierte en 'a'
    - 'é' se convierte en 'e'
    - 'í' se convierte en 'i'
    - 'ó' se convierte en 'o'
    - 'ú' se convierte en 'u'

    La función utiliza el método `replace` de las cadenas de texto para realizar los reemplazos
    uno por uno. Cada llamada a `replace` busca todas las ocurrencias de una vocal acentuada
    específica y las reemplaza por la versión sin acento.

    Ejemplo:
    --------
    Si se tiene el siguiente texto de entrada:
    
    Texto: "Café con leche y té."

    Llamada a la función:
    ---------------------
    Eliminar_Acentos("Café con leche y té.")

    Resultado:
    ----------
    "Cafe con leche y te."

    Nota:
    -----
    Esta función solo elimina los acentos de las vocales acentuadas especificadas. No maneja
    otros caracteres acentuados ni diacríticos que podrían estar presentes en otros idiomas
    o extensiones de la codificación Unicode.

    """
        
    Texto = Texto.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

    return Texto


# -----------------------------------------------------------
# Función para obtener una palabra específica de un texto, especificando posición.

def Obtener_Palabras(Texto, Posicion_Base = 0, Cantidad_Palabras = 1, Hacia_La = 'Derecha'):

    """
    Extrae una cantidad específica de palabras de un texto, comenzando desde una 
    posición dada, y permite elegir la dirección de extracción (hacia la derecha o 
    hacia la izquierda).

    Parámetros:
    - Texto (str): El texto del cual se extraerán las palabras.
    - Posicion_Base (int): La posición inicial (basada en 1) desde la cual empezar 
      la extracción de palabras. Se ajusta internamente para indexación basada en 0.
      Puede ser un número negativo, es decir, si es -1, sería la última posición, y así.
    - Cantidad_Palabras (int): El número de palabras a extraer, comenzando desde 
      la posición base.
    - Hacia_La (str): La dirección de la extracción. Puede ser 'Derecha' o 'Izquierda'. 
      Por defecto es 'Derecha'.

    Retorna:
    - list: Una lista con las palabras extraídas del texto, o una lista vacía si 
      la posición base está fuera del rango permitido o si ocurre algún error.

    Ejemplos:
    1. Obtener_Palabras("Python es un lenguaje de programación", 2, 3, 'Derecha')
       -> ['es', 'un', 'lenguaje']
    
    2. Obtener_Palabras("Python es un lenguaje de programación", 4, 2, 'Izquierda')
       -> ['un', 'es']

    Comportamiento:
    - La posición base ingresada por el usuario se ajusta restando 1 para la 
      indexación basada en 0 de Python.
    - Si la dirección es 'Derecha', se extraen las palabras desde la posición base 
      hacia adelante.
    - Si la dirección es 'Izquierda', se extraen las palabras hacia atrás desde 
      la posición base.
    - Las posiciones se ajustan para evitar que se extraigan más palabras de las 
      disponibles en el texto.

    Manejo de Errores:
    - Si la posición base es mayor que el número de palabras disponibles, se imprime 
      un mensaje de error y se retorna una lista vacía.
    - Se ajustan las posiciones iniciales y finales para evitar índices fuera de rango.

    """

    # Dividir el texto en palabras usando espacios como delimitadores.
    Palabras = Texto.split()
    
    # El usuario va a elegir entre una lista y no va a contar a partir de 0, sino de 1. Lo arreglamos.
    if Posicion_Base < 0:
        Posicion_Base = len(Palabras) + Posicion_Base
    else:
        Posicion_Base = Posicion_Base - 1

    # Excepción por si la posición inicial es incorrecta.
    if Posicion_Base > len(Palabras):
        print(f"Error: \n",
              f"La cantidad de palabras es {len(Palabras) + 1} y la posición que pusiste es {Posicion_Base + 1}. \n",
              "Está por fuera de lo permitido.")
        return []  
    
    # Excepciones por si se quiere extraer por fuera de lo permitido.
    if Hacia_La == 'Derecha':
        Posicion_Inicial = Posicion_Base
        Posicion_Final = Posicion_Base + Cantidad_Palabras

        # Si se excede del largo, la posición final es la última.
        if Posicion_Final > len(Palabras):
            Posicion_Final = len(Palabras)+1
            
    elif Hacia_La == 'Izquierda':
        Posicion_Inicial = Posicion_Base - Cantidad_Palabras + 1
        Posicion_Final = Posicion_Base

        # Si se excede del largo, la posición inicial es la primera.
        if Posicion_Inicial < 0:
            Posicion_Inicial = 0
    
    # Devolver la palabra de la posición especificada.

    # Si se piden varias palabras.
    if Cantidad_Palabras > 1:
        Extraccion_Palabras = Palabras[Posicion_Inicial:(Posicion_Final+1)]

    # Si se pide solo una palabra.
    elif Cantidad_Palabras == 1:
        Extraccion_Palabras = Palabras[Posicion_Base]

    return Extraccion_Palabras


# -----------------------------------------------------------
# Función para extraer valores de una lista de diccionarios de una clave determinada.

def Extraer_Valores_Segun_Clave(Lista_Diccionarios, Clave):
    
    """
    Extrae los valores asociados a una clave específica de una lista de diccionarios.

    Esta función recorre una lista de diccionarios y extrae los valores correspondientes
    a una clave específica dada. Devuelve una lista con los valores extraídos en el mismo
    orden en el que aparecen en la lista original de diccionarios.

    Parámetros:
    - Lista_Diccionarios (list): Una lista que contiene diccionarios. Cada diccionario debe
      contener la clave especificada en el parámetro `Clave`.
    - Clave (str): Una cadena que representa la clave cuyo valor se desea extraer de cada
      diccionario en la lista.

    Retorna:
    - list: Una lista de valores extraídos de los diccionarios basados en la clave dada.

    Manejo de Errores:
    - Si la clave especificada no existe en alguno de los diccionarios, se lanzará una
      excepción `KeyError`. Es importante asegurarse de que todos los diccionarios en
      `Lista_Diccionarios` contengan la clave especificada antes de ejecutar la función.

    Ejemplos:
    1. Extracción de valores de una lista de diccionarios con una clave existente:
    
        Lista_Diccionarios = [{'Nombre': 'Ana', 'Edad': 25}, {'Nombre': 'Luis', 'Edad': 30}]
        Extraer_Valores_Segun_Clave(Lista_Diccionarios, 'Nombre')
        ['Ana', 'Luis']
    
    2. Extracción de valores numéricos:

        Lista_Diccionarios = [{'ID': 101, 'Puntuacion': 89}, {'ID': 102, 'Puntuacion': 92}]
        Extraer_Valores_Segun_Clave(Lista_Diccionarios, 'Puntuacion')
        [89, 92]

    3. Manejo de excepción `KeyError` cuando la clave no está presente:

        Lista_Diccionarios = [{'A': 1, 'B': 2}, {'A': 3}]
        Extraer_Valores_Segun_Clave(Lista_Diccionarios, 'B')
        Traceback (most recent call last):
            ...
        KeyError: 'B'

    Consideraciones:
    - Antes de usar esta función, es recomendable verificar que todos los diccionarios en la lista contengan la clave deseada para evitar errores.
    - La función no maneja claves inexistentes de forma interna, por lo que el usuario debe prever esta situación si es necesario.

    """

    Lista = []
    for Diccionario in Lista_Diccionarios:
        Lista.append(Diccionario[Clave])
    
    return Lista


# -----------------------------------------------------------
# Función para armar un df final a partir de un recorte.

def df_Nota(Ruta_Archivo):

    # Abre el archivo de texto en modo lectura con codificación UTF-8.
    with open(Ruta_Archivo, 'r', encoding='utf-8') as Archivo:
        # Lee todo el contenido del archivo.
        Contenido = Archivo.read()

    # Divide el contenido en una lista de líneas.
    Lista_Lineas = Contenido.splitlines()

    # Procesa las líneas del archivo para extraer notas y datos.
    Notas = Armar_Nota(Lista_Lineas)

    # Crea un DataFrame de pandas a partir de los datos procesados.
    df = pd.DataFrame(Notas)

    return df

# -----------------------------------------------------------
# Función para armar una lista de diccionarios.
def Lista_De_Diccionarios_Por_Elemento_Padre(df, Lista, Elemento_Padre, Lista_Hijos):
    Resultado = []

    for Elemento in Lista:
        Datos_Por_Elemento = [f'{Elemento}']

        for i in range(0, len(df)):
            Diccionario = {}
            if Elemento == df[Elemento_Padre][i]:
                for Hijo in Lista_Hijos:
                    Diccionario[f'{Hijo}'] = df[Hijo][i]
                Datos_Por_Elemento.append(Diccionario)
        
        Resultado.append(Datos_Por_Elemento)
    
    return Resultado

# -----------------------------------------------------------
# Función que copia valores de un df a otro.

def Comparar_Df_y_Copiar(df1, df2, ColumnaA, ColumnaB, ColumnaC, ColumnaD):

    # Renombrar temporalmente las columnas si tienen el mismo nombre.
    if ColumnaA == ColumnaC:
        df2 = df2.rename(columns={ColumnaC: f"{ColumnaC}_R"})
        ColumnaC = f"{ColumnaC}_R"
    if ColumnaB == ColumnaD:
        df2 = df2.rename(columns={ColumnaD: f"{ColumnaD}_R"})
        ColumnaD = f"{ColumnaD}_R"
    
    for i in range(0, len(df1)):
        Elemento_Comparado_1 = df1[ColumnaA][i]
        
        for k in range(0, len(df2)):
            Elemento_Comparado_2 = df2[ColumnaC][k]

            if Elemento_Comparado_1 == Elemento_Comparado_2:
                # Pegamos el valor en el df1.
                df1.at[i, ColumnaB] = df2.at[k, ColumnaD]
    
    return df1
# Principales.

Dicotomic_Options = [True, False]
Message_Request_Number = "Introducí el número de tu elección:"
Message_Selected_Option = "Opción seleccionada:"
Message_Invalid_Option = "Opción no válida. La elección debe ser un valor entre 1 y"
Message_Invalid_Input = "Entrada no válida. Por favor introduce un número."

# Seleccionar File.

Explorer_Input_Title = 'Seleccioná el recorte con tus notas'
Filetypes_Description_Input = ['Archivos TXT']
Filetypes_Extension_Input = ['txt']

Filetypes_Tuples_Input = []

# Crear tuplas.
for Index, Filetype in enumerate(Filetypes_Description_Input):
    Tuple = (Filetype, f'*.{Filetypes_Extension_Input[Index]}*')
    Filetypes_Tuples_Input.append(Tuple)

# Usar output por defecto o no.
Default_Output_Format_Options = Dicotomic_Options
Default_Output_Format_Messages = ["¿Querés usar la configuración de salida por defecto?",
                                Message_Request_Number,
                                Message_Selected_Option,
                                f"{Message_Invalid_Option} {len(Default_Output_Format_Options)}.",
                                Message_Invalid_Input] 

# Formato del output.
Output_Format_Options = ['pdf', 'docx', 'doc', 'odt', 'csv', 'xlsx', 'xls', 'txt', 'Exportar a Notion', 'Exportar a Evernote']
Output_Format_Messages = ["Elegí el formato de salida:",
                          Message_Request_Number,
                          Message_Selected_Option,
                          f"{Message_Invalid_Option} {len(Output_Format_Options)}.",
                          Message_Invalid_Input] 

# Partición del output.
Output_Partition_Options = Dicotomic_Options
Output_Partition_Messages = ["¿Querés que salgan varios archivos de salida?",
                                Message_Request_Number,
                                Message_Selected_Option,
                                f"{Message_Invalid_Option} {len(Output_Partition_Options)}.",
                                Message_Invalid_Input] 

# Partición por defecto.
Default_Output_Partition_Options = Dicotomic_Options
Default_Output_Partition_Messages = ["¿Querés usar la configuración de partición del archivo de salida por defecto?",
                                Message_Request_Number,
                                Message_Selected_Option,
                                f"{Message_Invalid_Option} {len(Default_Output_Partition_Options)}.",
                                Message_Invalid_Input] 

# Criterio de partición.
Output_Partition_Criterion_Options = ['Por autor', 'Por libro', 'Por año', 'Por mes', 'Por día']
Output_Partition_Criterion_Messages = ["Elegí el criterio de partición de archivos:",
                          Message_Request_Number,
                          Message_Selected_Option,
                          f"{Message_Invalid_Option} {len(Output_Partition_Criterion_Options)}.",
                          Message_Invalid_Input] 

# Ubicación de guardado por defecto.
Default_Output_Path_Options = Dicotomic_Options
Default_Output_Path_Messages = ["¿Querés usar la configuración de guardado del archivo de salida por defecto?",
                                Message_Request_Number,
                                Message_Selected_Option,
                                f"{Message_Invalid_Option} {len(Default_Output_Path_Options)}.",
                                Message_Invalid_Input] 

# Seleccionar carpeta de guardado.
Explorer_Output_Title = 'Seleccioná la carpeta y el nombre del archivo final'
Filetypes_Description_Output = ['Archivos PDF', 'Archivos Word', 'Archivos Word', 'Archivos LibreOffice Writer', 'Archivos CSV', 'Archivos Excel', 'Archivos Excel', 'Archivos TXT']
Filetypes_Extension_Output = ['pdf', 'docx', 'doc', 'odt', 'csv', 'xlsx', 'xls', 'txt']

Filetypes_Tuples_Output = []

# Crear tuplas.
for Index, Filetype in enumerate(Filetypes_Description_Output):
    Tuple = (Filetype, f'*.{Filetypes_Extension_Output[Index]}*')
    Filetypes_Tuples_Output.append(Tuple)

# Matchs por defecto.
Default_Match_Options = Dicotomic_Options
Default_Match_Messages = ["¿Querés usar la configuración de matchs y agrupamiento de highlights por defecto?",
                                Message_Request_Number,
                                Message_Selected_Option,
                                f"{Message_Invalid_Option} {len(Default_Match_Options)}.",
                                Message_Invalid_Input] 

# Proccesing por defecto.
Default_Processing_Options = Dicotomic_Options
Default_Processing_Messages = ["¿Querés usar la configuración de procesamiento de los highlights por defecto?",
                                Message_Request_Number,
                                Message_Selected_Option,
                                f"{Message_Invalid_Option} {len(Default_Processing_Options)}.",
                                Message_Invalid_Input] 

# Estilo de los Blocks por defecto.
Default_Block_Style_Options = Dicotomic_Options
Default_Block_Style_Messages = ["¿Querés usar la configuración de estilo de los highlights por defecto?",
                                Message_Request_Number,
                                Message_Selected_Option,
                                f"{Message_Invalid_Option} {len(Default_Block_Style_Options)}.",
                                Message_Invalid_Input] 

# Estilo de los Blocks.
Block_Style_Options = [1, 2, 3, 4, 5, 6]
Block_Style_Messages = ["Elegí el estilo y la fuente de cada bloque:",
                          Message_Request_Number,
                          Message_Selected_Option,
                          f"{Message_Invalid_Option} {len(Block_Style_Options)}.",
                          Message_Invalid_Input] 

# Estilo de fuente del Highlight.
Highlight_Font_Style_Options = ['Normal', 'Negrita', 'Cursiva', 'Negrita y cursiva']
Highlight_Font_Style_Messages = ["Elegí el estilo de los highlights:",
                          Message_Request_Number,
                          Message_Selected_Option,
                          f"{Message_Invalid_Option} {len(Highlight_Font_Style_Options)}.",
                          Message_Invalid_Input] 

# Estilo de fuente de la Subline.
Subline_Font_Style_Options = ['Normal', 'Negrita', 'Cursiva', 'Negrita y cursiva']
Subline_Font_Style_Messages = ["Elegí el estilo de las sublines:",
                          Message_Request_Number,
                          Message_Selected_Option,
                          f"{Message_Invalid_Option} {len(Subline_Font_Style_Options)}.",
                          Message_Invalid_Input] 

# Fuente del Highlight.
# Esta tiene que ser una lista personalizada de fuentes. 
# Supongo se hace en la parte front.

Highlight_Font_Message = 'Ingresá la fuente del highlight.'

# Fuente de la Subline.
# Esta tiene que ser una lista personalizada de fuentes. 
# Supongo se hace en la parte front.

Subline_Font_Message = 'Ingresá la fuente de la subline:'

# Color de fuente del Highlight.
# Esta tiene que ser una lista personalizada de colores. 
# Supongo se hace en la parte front.

Highlight_Color_Message = 'Ingresá el color del texto de la subline:'

# Color de fuente de la Subline.
# Esta tiene que ser una lista personalizada de colores. 
# Supongo se hace en la parte front.

Subline_Color_Message = 'Ingresá el color del texto de la subline:'

# Tamaño de fuente del Highlight.
# Lo ingresa numéricamente el usuario.
Highlight_Font_Size_Message = 'Ingresá el tamaño del texto del highlight:'

# Tamaño de fuente de la Subline.
# Lo ingresa numéricamente el usuario.
Subline_Font_Size_Message = 'Ingresá el tamaño del texto de la subline:'

# Alineación del Highlight.
Highlight_Align_Options = ['Izquierda', 'Derecha', 'Centro', 'Justificada']
Highlight_Align_Messages = ["Elegí la alineación de los highlights:",
                          Message_Request_Number,
                          Message_Selected_Option,
                          f"{Message_Invalid_Option} {len(Highlight_Align_Options)}.",
                          Message_Invalid_Input] 

# Alineación de la Subline.
Subline_Align_Options = ['Izquierda', 'Derecha', 'Centro', 'Justificada']
Subline_Align_Messages = ["Elegí la alineación de las sublines:",
                          Message_Request_Number,
                          Message_Selected_Option,
                          f"{Message_Invalid_Option} {len(Subline_Align_Options)}.",
                          Message_Invalid_Input] 

# Nombre del archivo por defecto.
Default_Naming_Options = Dicotomic_Options
Default_Naming_Messages = ["¿Querés usar la configuración de nombrado de archivos por defecto?",
                                Message_Request_Number,
                                Message_Selected_Option,
                                f"{Message_Invalid_Option} {len(Default_Naming_Options)}.",
                                Message_Invalid_Input] 

# Nombrar archivo.
# Lo ingresa el usuario.
Naming_Message = 'Ingresá el nombre del archivo final que se guardará en la carpeta seleccionada:'


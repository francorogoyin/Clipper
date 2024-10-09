# Textos de formularios.
from Formulario import Explorer_Input_Title, Filetypes_Tuples_Input

# Herramientas.
import Tools as t


def P_Start(All = False):

    # Seleccionar el File.
    File_Path = t.Select_File(Explorer_Input_Title, Filetypes_Tuples_Input)

    if All:   

        # Usario/Externo.
        # Hay que definir el procedimiento de esto.
        User = True 

        # Seleccionar idioma.
        # Hay que definir el procedimiento de esto.
        Language = 'Spanish'


        # Procesamiento del File.
        # Hay que definir esto en una función en Tools.

        # if File_Language:
            # File_Proccesed = t.Proccess_File(File_Path, File_Language)

            # if File_Proccesed = False:
            #    return File_Invalid_Alert


        # Seleccionar formato del Output.
        if User:
            Default_Output_Format = t.Choose_Option(Default_Output_Format_Options, 
                                            Default_Output_Format_Messages[0],
                                            Default_Output_Format_Messages[1],
                                            Default_Output_Format_Messages[2],
                                            Default_Output_Format_Messages[3])
            
            if Default_Output_Format:
                Output_Format = 'pdf'

        if User == False or Default_Output_Format == False:
            Output_Format = t.Choose_Option(Output_Format_Options, 
                                            Output_Format_Messages[0],
                                            Output_Format_Messages[1],
                                            Output_Format_Messages[2],
                                            Output_Format_Messages[3])   


        # ¿Son formateables los bloques?
        Block_Formateable = ('pdf' in Output_Format or 'docx' in Output_Format or 'doc' in Output_Format)


        # Seleccionar la partición del Output.
        if User:
            Default_Output_Partition = t.Choose_Option(Default_Output_Partition_Options, 
                                                    Default_Output_Partition_Messages[0],
                                                    Default_Output_Partition_Messages[1],
                                                    Default_Output_Partition_Messages[2],
                                                    Default_Output_Partition_Messages[3])
            
            if Default_Output_Partition:
                Output_Partition = True

        if User == False or Default_Output_Partition == False:
            Output_Partition = t.Choose_Option(Output_Partition_Options, 
                                            Output_Partition_Messages[0],
                                            Output_Partition_Messages[1],
                                            Output_Partition_Messages[2],
                                            Output_Partition_Messages[3])

        if Output_Partition:
            Output_Partition_Criterion = t.Choose_Option(Output_Partition_Criterion_Options, 
                                            Output_Partition_Criterion_Messages[0],
                                            Output_Partition_Criterion_Messages[1],
                                            Output_Partition_Criterion_Messages[2],
                                            Output_Partition_Criterion_Messages[3])


        # Seleccionar Path del Output.
        if User:
            Default_Output_Path = t.Choose_Option(Default_Output_Path_Options, 
                                                    Default_Output_Path_Messages[0],
                                                    Default_Output_Path_Messages[1],
                                                    Default_Output_Path_Messages[2],
                                                    Default_Output_Path_Messages[3])
            
            if Default_Output_Path:
                Output_Path = 'c:/Users/tomas/Documents/Programación/Universidad/Patricionog/Highlights/'

        if User == False or Default_Output_Path == False:
            Output_Path = t.Select_Directory(Explorer_Output_Title)


        # ¿Usar Matchs por defecto?
        if User:
            Default_Match = t.Choose_Option(Default_Match_Options, 
                                            Default_Match_Messages[0],
                                            Default_Match_Messages[1],
                                            Default_Match_Messages[2],
                                            Default_Match_Messages[3])

        # Agregar opciones por si no es usuario o si es pero no elige por defecto.


        # ¿Usar Processing por defecto?
        if User:
            Default_Proccesing = t.Choose_Option(Default_Processing_Options, 
                                                Default_Processing_Messages[0],
                                                Default_Processing_Messages[1],
                                                Default_Processing_Messages[2],
                                                Default_Processing_Messages[3])

        # Agregar opciones por si no es usuario o si es pero no elige por defecto.


        # Seleccionar estilo del Block.
        if User and Block_Formateable:
            Default_Block_Style = t.Choose_Option(Default_Block_Style_Options, 
                                                Default_Block_Style_Messages[0],
                                                Default_Block_Style_Messages[1],
                                                Default_Block_Style_Messages[2],
                                                Default_Block_Style_Messages[3])
            
            Default_Naming = t.Choose_Option(Default_Naming_Options, 
                                                Default_Naming_Messages[0],
                                                Default_Naming_Messages[1],
                                                Default_Naming_Messages[2],
                                                Default_Naming_Messages[3])
            

        if (User == False or Default_Block_Style == False) and Block_Formateable:
            
            Block_Style = t.Choose_Option(Block_Style_Options, 
                                            Block_Style_Messages[0],
                                            Block_Style_Messages[1],
                                            Block_Style_Messages[2],
                                            Block_Style_Messages[3])
            
            Highlight_Font_Style = t.Choose_Option(Highlight_Font_Style_Options, 
                                                Highlight_Font_Style_Messages[0],
                                                Highlight_Font_Style_Messages[1],
                                                Highlight_Font_Style_Messages[2],
                                                Highlight_Font_Style_Messages[3])

            # Highlight_Font = show_message("Fuente de Resaltado", Highlight_Font_Message)
            
            Subline_Font_Style = t.Choose_Option(Subline_Font_Style_Options, 
                                            Subline_Font_Style_Messages[0],
                                            Subline_Font_Style_Messages[1],
                                            Subline_Font_Style_Messages[2],
                                            Subline_Font_Style_Messages[3])
            
            Highlight_Font = input(Highlight_Font_Message)
            Subline_Font = input(Subline_Font_Message)

            Highlight_Color = input(Highlight_Color_Message)
            Subline_Color = input(Subline_Color_Message)

            Highlight_Font_Size = input(Highlight_Font_Size_Message)
            Subline_Font_Size = input(Subline_Font_Size_Message)

            Highlight_Align = t.Choose_Option(Highlight_Align_Options, 
                                            Highlight_Align_Messages[0],
                                            Highlight_Align_Messages[1],
                                            Highlight_Align_Messages[2],
                                            Highlight_Align_Messages[3])
            
            Subline_Align = t.Choose_Option(Subline_Align_Options, 
                                            Subline_Align_Messages[0],
                                            Subline_Align_Messages[1],
                                            Subline_Align_Messages[2],
                                            Subline_Align_Messages[3])

        # Agregar opciones por si no es usuario o si es pero no elige por defecto.


        # Nombrar Output.
        if Output_Partition_Options == False:
            Output_Name = input(Naming_Message)
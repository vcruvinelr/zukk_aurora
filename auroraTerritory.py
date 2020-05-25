import arcpy
import os
import sys
import arcgisscripting
import locale

reload(sys)
sys.setdefaultencoding('UTF8')
locale.setlocale(locale.LC_TIME, "ptb")

if __name__ == '__main__':
    
    gp = arcgisscripting.create()
    tabelaGeocode = arcpy.GetParameterAsText(0)
    addressLocator = arcpy.GetParameterAsText(1)
    saidafeaturePontos = arcpy.GetParameterAsText(2)
    camadaEntrada = arcpy.GetParameterAsText(3)
    displayField = arcpy.GetParameterAsText(4)
    pastaProjeto = arcpy.GetParameterAsText(5)
    territoryName = arcpy.GetParameterAsText(6)
    minimoCapacity = arcpy.GetParameterAsText(7)
    maximoCapacity = arcpy.GetParameterAsText(8)
    metodoTerritorios = arcpy.GetParameterAsText(9)
    quantidadeAreas = arcpy.GetParameterAsText(10)
    goodBalance = arcpy.GetParameterAsText(11)
    layerOutput = "{0}\\{1}\\tdlayer.lyr".format(pastaProjeto, territoryName)

    try:
        
        arcpy.AddMessage("Iniciando Processo")
        arcpy.AddMessage("Convertendo Tabela de Enderecos")

        arcpy.GeocodeAddresses_geocoding(
            tabelaGeocode, 
            addressLocator, 
            "Address 'ENDERECO CLIE' VISIBLE NONE;Neighborhood 'BAIRRO CLIE' VISIBLE NONE;City 'CIDADE CLIE' VISIBLE NONE;Region 'ESTADO CLIE' VISIBLE NONE;Postal <None> VISIBLE NONE", 
            saidafeaturePontos, 
            "STATIC", 
            "", 
            ""
            )

        arcpy.AddMessage("Enderecos convertidos com sucesso. Iniciando processo - Criar Solucao de Territorio")

        gp.CreateTerritorySolution_TD(
            camadaEntrada,
            displayField,
            "Territories",
            pastaProjeto,
            territoryName
        )

        arcpy.AddMessage("Solucao criada com sucesso")
        arcpy.AddMessage("Iniciando Importacao de Variaveis")

        gp.ImportVariablesBySpatialJoin_TD(
            layerOutput, 
            saidafeaturePontos, 
            "Count"
            )
        
        arcpy.AddMessage("Importacao Finalizada com Sucesso. Criando territorios, este processo levara alguns minutos")

        gp.SetupLevelCapacityConstraints_TD(
            layerOutput, 
            "Territories[1]", 
            "{0}.Count_SUM {1} # {2} 100".format(saidafeaturePontos.split("\\")[-1], minimoCapacity, maximoCapacity)
        )

        gp.SetupLevelBalancingVariables_TD(
            layerOutput, 
            "Territories[1]", 
            "{0}.Count_SUM 100".format(saidafeaturePontos.split("\\")[-1])
        )
    
        gp.SetupLevelTerritoryShapeParameters_TD(
            layerOutput,
            "Territories[1]", 
            "STRAIGHT_LINE_DISTANCE", 
            "", 
            "", 
            "", 
            "", 
            "{0}".format(goodBalance), 
            "USE_ALL_FEATURES", 
            "GEOMETRIC_CENTER", 
            ""
        )

        gp.SetupLevelDistanceConstraints_TD(
            layerOutput,
            "Territories[1]", 
            "KILOMETERS", 
            "", 
            "", 
            ""
        )

        if metodoTerritorios == "Automatico":

            gp.CreateTerritories_TD(
                layerOutput, 
                "Territories[1]", 
                "REMOVE_TERRITORIES", 
                "OPTIMAL_NUMBER", 
                "", 
                "CREATE_FROM_OPTIMAL_LOCATIONS", 
                "", 
                "", 
                "", 
                "", 
                "", 
                "ALL_NAMES", 
                "DO_NOT_AUTO_FILL_EXTENT", 
                "DO_NOT_OVERRIDE_CONSTRAINTS"
                )

        else:

            gp.CreateTerritories_TD(
                layerOutput, 
                "Territories[1]", 
                "REMOVE_TERRITORIES", 
                "USER_DEFINED", 
                quantidadeAreas, 
                "CREATE_FROM_OPTIMAL_LOCATIONS", 
                "", 
                "", 
                "", 
                "", 
                "", 
                "ALL_NAMES", 
                "DO_NOT_AUTO_FILL_EXTENT", 
                "DO_NOT_OVERRIDE_CONSTRAINTS"
                ) 
        
        arcpy.AddMessage("Processo finalizado com sucesso!")

    except Exception as e:

      arcpy.AddError(e)
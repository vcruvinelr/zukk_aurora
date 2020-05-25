import arcpy
import os
import sys
import arcgisscripting
import locale

reload(sys)
sys.setdefaultencoding('UTF8')
locale.setlocale(locale.LC_TIME, "ptb")

locale.setlocale(locale.LC_TIME, "ptb")

if __name__ == '__main__':
    
    gp = arcgisscripting.create()
    camadaEntrada = arcpy.GetParameterAsText(0)
    displayField = arcpy.GetParameterAsText(1)
    pastaProjeto = arcpy.GetParameterAsText(2)
    territoryName = arcpy.GetParameterAsText(3)
    pointsClientes = arcpy.GetParameterAsText(4)
    maximoCapacity = arcpy.GetParameterAsText(5)
    minimoCapacity = arcpy.GetParameterAsText(6)
    quantidadeAreas = arcpy.GetParameterAsText(7)
    layerOutput = "{0}\\{1}\\tdlayer.lyr".format(pastaProjeto, territoryName)

    try:
        
        gp.CreateTerritorySolution_TD(
            camadaEntrada,
            displayField,
            "Territories",
            pastaProjeto,
            territoryName
        )

        gp.ImportVariablesBySpatialJoin_TD(
            layerOutput, 
            pointsClientes, 
            "Count"
            )
        
        gp.SetupLevelCapacityConstraints_TD(
            layerOutput, 
            "Territories[1]", 
            "{0}.Count_SUM {1} # {2} 100".format(pointsClientes.split("\\")[-1], minimoCapacity, maximoCapacity)
        )

        gp.SetupLevelBalancingVariables_TD(
            layerOutput, 
            "Territories[1]", 
            "{0}.Count_SUM 100".format(pointsClientes.split("\\")[-1])
        )
    
        gp.SetupLevelTerritoryShapeParameters_TD(
            layerOutput,
            "Territories[1]", 
            "STRAIGHT_LINE_DISTANCE", 
            "", 
            "", 
            "", 
            "", 
            "30", 
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

    except Exception as e:

      arcpy.AddError(e)
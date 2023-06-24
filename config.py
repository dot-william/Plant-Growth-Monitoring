
# mqttIP = "ccscloud2.dlsu.edu.ph"
# mqttPort = 20010
class Config(object):

    mqttIP = "ccscloud2.dlsu.edu.ph"

    experiment_num = "0"


    # Table where environmental data are stored
    sensors_table = "dlsu_cherrytomato_"+ experiment_num

    # Table where model predictions (object detection and extrapolation) are stored
    predictions_table = "pred_table_" + experiment_num

    # Table where median of prediction from object detections of a certain date are stored
    # pred_median_table = "median_count_" + experiment_num
    pred_median_table = "test_median_counts" 
    
    # Table where DLI values are stored
    dli_table = "dli_table_" + experiment_num
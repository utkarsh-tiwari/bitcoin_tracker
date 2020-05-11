import json
import pandas as pd
import os
import sys
import logging.config
import yaml
import shutil

#--------------------importing process cocnfigs and setting logger---------------------
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import properties.config as config

with open(config.log_config, 'r') as stream:
    log_config = yaml.load(stream, Loader=yaml.FullLoader)

logging.config.dictConfig(log_config)
logger = logging.getLogger('JSONExcelTask')
#-------------------------------------------------------------------------------


def create_sample_json(count=None):
    """Function to create 'count' number of JSONs

    Args:
        count (int, optional): Number of sample JSONs to be created. Defaults to None.

    Returns:
        dict: JSON load with all individual JSONs in consecutive rows
    """    

    logger.info("Starting create sample json task")
    try:
        json_input = list()
        for index in range(1, count+1):
            json_input_ = dict()
            json_input_['Ref'] = f'ABC_{index}'
            json_input_['sample'] = f'sample_status_{index}'
            json_input.append(json_input_)
        
        json_dump = json.dumps(json_input)
        json_load = json.loads(json_dump)
        result = json_load
    
    except Exception as e:
        logger.exception(f"Exception occured: {str(e)}")
        result = "Exception occured!"
    
    logger.info("Finished create sample json task")
    return result


class ExcelHandling:
    """Class to handle all excel reading and writing operations of dumping input load to excel.
    """    

    def __init__(self, json_load=None):
        """Pass JSON load while creating object

        Args:
            json_load (dict, optional): JDON dump to be uploaded to exccel file. Defaults to None.
        """

        self.data_set = None
        self.json_load = json_load
        self.process_excel_file = os.path.join(config.processing_folder, os.path.basename(config.excel_file))
        
    def read_from_excel(self, process_file=None):
        """Create and read sample excel file.

        Args:
            process_file (string, optional): Excel file for  reading data other than theone specified in config. Defaults to None.

        Returns:
            bool: Returns true if operations successfull
        """        

        if process_file is not None:
            self.process_excel_file = process_file

        if os.path.exists(self.process_excel_file):
            os.remove(self.process_excel_file)
        
        if os.path.exists(config.excel_file):
            shutil.copyfile(config.excel_file, self.process_excel_file)
        
        self.data_set = pd.read_excel(self.process_excel_file, sheet_name='Sheet1')
        return True

    def write_to_excel(self):
        """Write JSON dump to excel file iteratively for  all rows of JSONs

        Returns:
            bool: True if operation successfull
        """        
        
        i = 1
        for item in self.json_load:
            item = json.dumps(item)
            item = json.loads(item)
            self.data_set = self.data_set.append({'Index': i, 'Reference_Key': item['Ref'], 'Status': item['sample']}, ignore_index=True)
            i += 1

        self.data_set.to_excel(self.process_excel_file, index=False)
        return True

if __name__ == '__main__':

    logger.info("Starting main task")
    result_json = create_sample_json(count=20)
    if 'Exception' not in result_json:
        
        logger.info("Starting Excel Handling task")
        try:
            excel_obj = ExcelHandling(json_load=result_json)
            result_read = excel_obj.read_from_excel()
            if result_read:
                result_write = excel_obj.write_to_excel()
                sys.stdout.write(f"{result_write}\n")
                logger.info(f"Result of writing to excel: {result_write}")
        except Exception as e_:
            logger.exception(f"Exception occured in ExceclHandling class: {str(e_)}")
        logger.info("Finished Excel Handling task")
    
    logger.info("Finished main task")

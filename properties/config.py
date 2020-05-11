import os

process_folder_name = 'json_to_excel'
properties_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)))
processing_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), process_folder_name, 'processing')
excel_file = os.path.join(properties_folder, 'excel_database.xlsx')
log_config = os.path.join(properties_folder, 'logging_config.yml')

import config
import os
import logging
import importlib

logger = logging.getLogger(__name__)

'''
Found all Solution folder in the application.
A solution folder must have an plugin subfolder with __init__.py file.
'''
def find_all_solutions():
    logger.info("Scanning for plugins ...")
    for root, dirs, files in os.walk(os.path.join(config.AppConfig.get_app_root(), '')):
        if root.endswith('__solution__') :
            logger.info ('Solutionfolder found: %s' % root)
            if 'plugins' in dirs:
                logger.info("Plugin directory found!")
                full_path_name=os.path.join(root, 'plugins')
                for file in os.listdir( full_path_name ):
                    if file.endswith(".py") and not file.startswith('__'):
                        logger.info(file)
                        namespace=config.AppConfig.convert_path_to_namespace(full_path_name)
                        i = importlib.import_module(namespace+'.'+file.replace('.py', ''))
                        i.register()
            if 'endpoints' in dirs:
                logger.info("Endpoint directory found!")
                full_path_name=os.path.join(root, 'endpoints')
                for file in os.listdir( full_path_name ):
                    if file.endswith(".py") and not file.startswith('__'):
                        logger.info(file)
                        namespace=config.AppConfig.convert_path_to_namespace(full_path_name)
                        i = importlib.import_module(namespace+'.'+file.replace('.py', ''))



    logger.info ("All files scanned!")


class Test:
    def __init__(self, fn):
        self.__fn=fn
        pass

    def __call__(self):
        pass

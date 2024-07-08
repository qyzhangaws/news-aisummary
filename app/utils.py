import importlib
import os
import shutil


def create_obj_from_class_name(class_name, module_name=None, *args, **kwargs):
    """
    Create an object from a class name provided as a string.
    
    Args:
        class_name (str): The name of the class to create an object from.
        module_name (str, optional): The name of the module containing the class.
            If not provided, the class is assumed to be in the current module.
        *args: Positional arguments to pass to the class constructor.
        **kwargs: Keyword arguments to pass to the class constructor.
        
    Returns:
        object: An instance of the specified class.
        
    Raises:
        AttributeError: If the class is not found in the specified module.
    """
    if module_name:
        module = importlib.import_module(module_name)
        class_obj = getattr(module, class_name)
    else:
        class_obj = globals()[class_name]
    
    return class_obj(*args, **kwargs)


def cleanup_tmp_space():
    """
    Clean up temporary files and directories created during the execution of the program.
    """
    TMP_PATH = "/tmp"
    if os.path.exists(TMP_PATH):
        shutil.rmtree(TMP_PATH)

from sqlalchemy import inspect

def scalar_result_to_dict_list(objects):
    return [obj.to_dict() for obj in objects]
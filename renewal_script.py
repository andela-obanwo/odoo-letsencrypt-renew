import os
import sys
from actions import SecurityGroupActions, logger

security_group_actions = SecurityGroupActions()

try:
    func_name = sys.argv[1]
except KeyError:
    logger.exception(dict(msg='Function Name not supplied', type='no_function_name'))
    raise
try:
    func = getattr(security_group_actions, func_name)
except AttributeError:
    logger.error(dict(msg='Invalid action method name supplied', type='invalid_action_method_name'))
    raise

func()





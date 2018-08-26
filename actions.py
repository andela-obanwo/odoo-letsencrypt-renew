import os
import logging
import logging.handlers

import boto3
from dotenv import load_dotenv
 
join = os.path.join
dirname = os.path.dirname

log_filename = 'logs/log.txt'
format_string = '%(asctime)s: %(levelname)s: %(message)s'

formatter = logging.Formatter(format_string)
handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=409600, backupCount=5)

handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
 
# Load file from the path.
load_dotenv(dotenv_path)


class SecurityGroupActions(object):

    def __init__(self, dry_run=False):
        self.profile_name = os.getenv('CRED_PROFILE')
        if not self.profile_name:
            logger.exception(dict(msg="no profile name supplied.", type="no_profile_name"))
            raise Exception(msg="No profile name supplied", code="no_profile_name")

        self.group_name = os.getenv('GROUP_NAME')
        self.group_id = os.getenv('GROUP_ID')

        if not self.group_id:
            logger.info(dict(msg="no security group id supplied.", type="no_security_group_id"))
            if not self.group_name:
                logger.exception(dict(msg="no security group id and name supplied.", type="no_security_group_id_and_name"))
                raise Exception(msg="No secutity group id and name supplied", code="no_security_group_id_and_name")
        try:
            self.session = boto3.Session(profile_name=self.profile_name)
            self.ec2_client = self.session.client('ec2')
        except Exception as e:
            logger.exception(dict(msg=e.message, exception=e))
        self.request_params = dict(GroupId=self.group_id,
                                GroupName=self.group_name,
                                IpPermissions=[
                                    {
                                        'FromPort': 443,
                                        'IpProtocol': 'tcp',
                                        'IpRanges': [
                                            {
                                                'CidrIp': '0.0.0.0/0',
                                                'Description': 'Temporary IPv4 Letsencrypt HTTPS access'
                                            },
                                        ],
                                        'Ipv6Ranges': [
                                            {
                                                'CidrIpv6': '::/0',
                                                'Description': 'Temporary IPv6 Letsencrypt HTTPS access'
                                            },
                                        ],
                                
                                        'ToPort': 443,
                                
                                    },
                                ],
                                DryRun=dry_run)
        
    def enable_https(self):
        try:
            self.ec2_client.authorize_security_group_ingress(**self.request_params)
        except Exception as e:
            logger.warning(dict(msg=e, type='enable_https_unsuccessful'))
        else:
            logger.info(dict(msg='enable https request completed successfully', type='enable_https_success'))

    def disable_https(self):
        try:
            self.ec2_client.revoke_security_group_ingress(**self.request_params)
        except Exception as e:
            logger.warning(dict(msg=e, type='disable_https_unsuccessful'))
        else:
            logger.info(dict(msg='disable https request completed successfully', type='disable_https_success'))

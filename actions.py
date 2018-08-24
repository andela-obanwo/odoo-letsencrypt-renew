import os
import boto3

from dotenv import load_dotenv
 
join = os.path.join
dirname = os.path.dirname

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
 
# Load file from the path.
load_dotenv(dotenv_path)


class SecurityGroupActions(object):

    def __init__(self, dry_run=False):
        self.profile_name = os.getenv('CRED_PROFILE')
        self.session = boto3.Session(profile_name=self.profile_name)
        self.ec2_client = self.session.client('ec2')
        self.group_name = os.getenv('GROUP_NAME')
        self.group_id = os.getenv('GROUP_ID')
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
        self.ec2_client.authorize_security_group_ingress(**self.request_params)

    def disable_https(self):
        self.ec2_client.revoke_security_group_ingress(**self.request_params)

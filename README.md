## Global HTTPS access on AWS EC2 security group

### This app is designed to either enable or disable global https access to the specified aws ec2 security group

Steps to use
* clone the repository `git clone git@github.com:andela-obanwo/odoo-letsencrypt-renew.git`
* create the necessary virtual enviroments
* run `pip install -r requirements.txt`
* add credentials with the necessary permissions to `~/.aws/credentials`
* for example: 
```
[XXX-XXX-PROFILE-NAME]
region=us-east-1
aws_access_key_id = XXXXXXXXXXXXXXX
aws_secret_access_key = +laksdflasdLKJLADLAKDLASDLFKADSLFasdsdf
```

* add the security group id and or group name to your `.env` file (you need to have created this prior)
* for example:
```
GROUP_ID=sg-XXXXXXb
GROUP_NAME='Demo Security Group'
CRED_PROFILE='XXX-XXX-PROFILE-NAME'
```

* run the script `renewal_script.py` and pass in the desired action `'enable_https'` or `'disable_https'` as an argument
* for example
```
python renewal_script.py enable_https
python renewal_script.py disable_https
```
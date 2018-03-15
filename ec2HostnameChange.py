import boto3
#import paramiko to facilitate ssh session for hostname change
import paramiko
#import expanduser to allow key path from ~/.ssh
from os.path import expanduser

#set the variable for the key for paramiko to use, initialize the ssh client, set auto add policy for paramiko
key=paramiko.RSAKey.from_private_key_file(expanduser("~/.ssh/Keypairname"))
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#get all ec2 instances and store in a variable
ec2 = boto3.resource('ec2')
#iterate through all instances, retreive DNS, value of the name tag, use paramiko to ssh and execute command to change hostname, 
#close connection and go to the next instance 
for ec2instance in ec2.instances.all():
    #get public DNS for each instance to use with paramiko as hostname to connect
    instanceDNS = ec2instance.public_dns_name
    #iterate through tags until finding Name and then storing that value in a varaible
    for tag in ec2instance.tags:
        if tag['Key'] == 'Name':
            newHostname = tag['Value']
            #ssh in and run command to change hostname to the new host name
            client.connect(hostname = instanceDNS, username = 'ec2-user', pkey=key)
            stdin, stdout, stderr = client.exec_command("sudo hostname {} ".format(newHostname))
            client.close()
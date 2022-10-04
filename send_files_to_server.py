#Ensure that paramiko package is installed

import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('',username='', password= '')
print("Connected successfully")

sftp = ssh.open_sftp()
print ("Connected successfully!")

sftp = ssh.open_sftp()
print (sftp)
sftp.put(file_path_of_file, file_destination_on_server)
sftp.close()

print ("copied successfully!")
ssh.close()
exit()

#To do:
#Save files with raspberry id and date and time
#make this dynamic

EFS_ID="<YOUR_EFS_ID>"
mkdir -p /home/ec2-user/efs
echo "${EFS_ID}:/ /home/ec2-user/efs efs _netdev,tls 0 0" >> /etc/fstab
mount -a
chown -R ec2-user:ec2-user /home/ec2-user/efs

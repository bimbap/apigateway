cd /home/ec2-user
git clone -b master https://github.com/bimbap/apigateway.git app
cd /home/ec2-user/app
npm install --omit=dev

cat <<EOF > /home/ec2-user/app/.env
PORT=5000
API_URL=<YOUR_API_GATEWAY_URL>
EFS_LOG_PATH=<YOUR_EFS_LOG_PATH>
EOF

chown -R ec2-user:ec2-user /home/ec2-user/app

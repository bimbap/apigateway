su - ec2-user -c "cd /home/ec2-user/app && npx pm2 start index.js --name books-app && npx pm2 save"
env PATH=$PATH:/usr/bin /home/ec2-user/app/node_modules/.bin/pm2 startup systemd -u ec2-user --hp /home/ec2-user

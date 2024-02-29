# Dashboard
Dashboard from  Device, you must be set from the database NoSQL.

# Application
## Install nodejs
`curl -fsSL https://rpm.nodesource.com/setup_21.x | sudo bash -`<br/>
`sudo yum install -y nodejs git amazon-efs-utils`
## Install Dependencies
`npm install`

# Envinronment Variable
Setting the environment variable on your path application, use the name .env, and set the variable name on the instruction below:<br/>
`API_URL=set your API Gateway URL`<br/>
`EFS_MOUNT_PATH=set your path EFS`

# Command run application
`npm run start-prod`

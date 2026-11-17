# Books Portal Application (EC2 + API Gateway + Lambda + DynamoDB + EFS)

Web application and serverless CRUD backend for the Cloud Computing post-test scenario.

---

## Architecture
![Architecture](Latiahn-APlikasi.drawio.png)

---

## AWS Lambda Functions (`Python 3.12`)

Deploy all five functions using the **Python 3.12** runtime with **Lambda Proxy Integration** enabled in API Gateway:

| Function | Source File | Route & Method |
|---|---|---|
| Book Get (List) | [`lambda/bookget.py`](lambda/bookget.py) | `GET /books` |
| Book Create | [`lambda/bookcreate.py`](lambda/bookcreate.py) | `POST /books` |
| Books Get (Detail) | [`lambda/booksget.py`](lambda/booksget.py) | `GET /books/{id}` |
| Book Update | [`lambda/book-update.py`](lambda/book-update.py) | `PUT /books/{id}` |
| Book Delete | [`lambda/book-delete.py`](lambda/book-delete.py) | `DELETE /books/{id}` |

---

## EC2 Application Setup (Amazon Linux 2023)

### 1. Install Node.js 22 LTS & EFS Utils
```bash
curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
sudo dnf install -y nodejs git amazon-efs-utils
```

### 2. Mount EFS
Using EFS Mount Helper:
```bash
mkdir -p /home/ec2-user/efs
sudo mount -t efs -o tls <your-efs-id>:/ /home/ec2-user/efs
```

Using NFSv4 Client:
```bash
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport <your-efs-dns>:/ /home/ec2-user/efs
```

### 3. Install Dependencies
```bash
npm install
```

### 4. Environment Variables (`.env`)
Create a `.env` file in the project root:
```env
PORT=5000
API_URL=https://<api-id>.execute-api.us-east-1.amazonaws.com/production/books
EFS_LOG_PATH=/home/ec2-user/efs/app.log
```

### 5. Run Application
```bash
npm run start-prod
```

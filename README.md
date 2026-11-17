# Dashboard
Dashboard from Device, you must set up the NoSQL database and serverless API.

---

# Architecture
![Architecture](Latiahn-APlikasi.drawio.png)

---

# AWS Lambda Functions (`Python 3.12`)

| Function | Source File | Route & Method |
|---|---|---|
| Book Get (List) | [`lambda/bookget.py`](lambda/bookget.py) | `GET /books` |
| Book Create | [`lambda/bookcreate.py`](lambda/bookcreate.py) | `POST /books` |
| Books Get (Detail) | [`lambda/booksget.py`](lambda/booksget.py) | `GET /books/{id}` |
| Book Update | [`lambda/book-update.py`](lambda/book-update.py) | `PUT /books/{id}` |
| Book Delete | [`lambda/book-delete.py`](lambda/book-delete.py) | `DELETE /books/{id}` |

---

# API Gateway Mapping Templates (Non-Proxy Reference)

If using non-proxy Integration Request mapping templates:

## Method POST
```vtl
$input.json('$')
```

## Method PUT (`/books/{id}`)
```json
{
  "body": $input.json('$'),
  "pathParameters": {
    "id": "$input.params('id')"
  }
}
```

## Method GET (`/books/{id}`)
```json
{
  "body": $input.json('$'),
  "pathParameters": {
    "id": "$input.params('id')"
  }
}
```

## Method DELETE (`/books/{id}`)
```json
{
  "pathParameters": {
    "id": "$input.params('id')"
  }
}
```

---

# Application

## Install Node.js 22 LTS & Dependencies
```bash
curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
sudo dnf install -y nodejs git amazon-efs-utils
```

## Mounting EFS

### Using EFS Mount Helper:
```bash
sudo mount -t efs -o tls yourEFS:/ efs
```

### Using NFS Client:
```bash
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport yourEFS:/ efs
```

## Install Packages
```bash
npm install
```

## Environment Variable
Setting the environment variable on your application path, and set the variable names on the instruction below:
- `API_URL=set your API Gateway URL`
- `EFS_LOG_PATH=set your path EFS`

## Command Run Application
```bash
npm run start-prod
```

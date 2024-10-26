# Menggunakan image Node.js versi 20
FROM node:20

# Mengatur working directory
WORKDIR /usr/src/app

# Menyalin package.json dan package-lock.json
COPY package*.json ./

# Menginstal dependencies
RUN npm install pm2 -g
RUN npm install


# Menyalin seluruh kode aplikasi
COPY . .

# Mengatur environment variable
ENV API_URL=ganti urlnya
ENV EFS_LOG_PATH=ganti pathnya

# Mengekspos port 5000
EXPOSE 5000

# Menjalankan aplikasi
CMD [ "npm", "run", "start-prod" ]

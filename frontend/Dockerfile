FROM node:18

# Instala una versión estable de npm sin el bug
RUN npm install -g npm@9.6.3

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

# Comando para iniciar la aplicación frontend
CMD ["npm", "run", "dev"]

FROM node:18-alpine

LABEL maintainer="https://suk.kr"

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile

COPY index.js ./

CMD ["node", "index.js"]
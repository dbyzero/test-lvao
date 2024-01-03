# Build Stage 1

FROM node:16-slim AS appbuild

RUN mkdir /var/www
WORKDIR /var/www
COPY package.json .
COPY .npmrc .
COPY pnpm-lock.yaml .

RUN npm install -g pnpm
RUN pnpm install

RUN ls -la /
COPY . /var/www
RUN pnpm build

# Build Stage 2

FROM nginx:1.23
WORKDIR /var/www
COPY --from=appbuild /var/www/dist ./build
COPY ./server.conf /etc/nginx/conf.d/default.conf


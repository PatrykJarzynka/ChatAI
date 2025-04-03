FROM node:22 AS build

WORKDIR /app
COPY package*.json ./

RUN npm install

COPY . .
RUN npm run build:prod

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist/chat-ai/browser /usr/share/nginx/html

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]

EXPOSE 80
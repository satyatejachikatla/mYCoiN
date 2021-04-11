FROM node:lts-alpine3.13

COPY ./app /app

WORKDIR /app

RUN npm install
# RUN npx install bootstrap


CMD [ "npm", "run", "start-frontend" ]
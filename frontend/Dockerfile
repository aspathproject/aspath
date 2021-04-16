FROM node:14

COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
WORKDIR /app
RUN yarn install

COPY . /app

ENV HOST=0.0.0.0
ENV PORT=8080

RUN yarn generate

CMD [ "yarn", "start" ]

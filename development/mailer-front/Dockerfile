FROM node:8

COPY mailer-front/package.json /usr/src/app/package.json
COPY mailer-front/yarn.lock /usr/src/app/yarn.lock

WORKDIR /usr/src/app/

RUN yarn install

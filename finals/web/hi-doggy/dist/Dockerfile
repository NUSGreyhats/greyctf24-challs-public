FROM alpine as builder
COPY readflag.c /readflag.c
RUN apk add --no-cache gcc musl-dev && \
    gcc -o /readflag /readflag.c

FROM node:lts-alpine
COPY --from=builder /readflag /readflag
COPY flag /flag
RUN chmod 400 /flag && chmod 4755 /readflag
ENV NODE_ENV=production
WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
RUN npm install --production --silent && mv node_modules ../
COPY . .
EXPOSE 3000
USER node
CMD ["node", "index.js"]

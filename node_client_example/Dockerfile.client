# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM node:5

WORKDIR /src

COPY src/package.json /src/package.json
RUN npm install
COPY src/* /src/

CMD ["node", "client.js"]

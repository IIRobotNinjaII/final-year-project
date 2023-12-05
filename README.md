# final-year-project

1)Get Metamask
https://metamask.io/
Install to your browser
Make 4 accounts , User 1, Officer 1 , Officer 2, Officer 3
Add Polygon Mumbai Test Network to your metmask, follow the below link
https://www.datawallet.com/crypto/add-polygon-mumbai-to-metamask
Add matic token to each of your accounts, go to the below website and do for each account
https://faucet.polygon.technology/

2)Deploy Contract
Go to the website below and sign in with your User 1 Account and make an account
https://thirdweb.com/
Then Click on the below link and deploy to Mumbai Test Network
https://thirdweb.com/contracts/deploy/QmNX7dGEkPnjAty8PVf2aSpAnD4G63ma8c6JJEAqnFey8V
Add the 3 officers address and click deploy


3)To run Frontend
Rename .env.example to .env
And edit the values in there
Replace REACT_APP_CONTRACT_ID with your deployed contract ID
Replace REACT_APP_TEMPLATE_CLIENT_ID by following the below link
https://portal.thirdweb.com/api-keys
Then run these commands
```
cd frontend/
yarn install
yarn start
```

4)To run key exchange server
Run these
```
cd key-exchange-server/
npm i
node server.js
```

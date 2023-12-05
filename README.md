# final-year-project

1)Get Metamask <br />
https://metamask.io/ <br />
Install to your browser <br />
Make 4 accounts , User 1, Officer 1 , Officer 2, Officer 3 <br />
Add Polygon Mumbai Test Network to your metmask, follow the below link <br />
https://www.datawallet.com/crypto/add-polygon-mumbai-to-metamask <br />
Add matic token to each of your accounts, go to the below website and do for each account <br />
https://faucet.polygon.technology/ <br />

2)Deploy Contract <br />
Go to the website below and sign in with your User 1 Account and make an account <br />
https://thirdweb.com/ <br />
Then Click on the below link and deploy to Mumbai Test Network <br />
https://thirdweb.com/contracts/deploy/QmNX7dGEkPnjAty8PVf2aSpAnD4G63ma8c6JJEAqnFey8V <br />
Add the 3 officers address and click deploy <br />


3)To run Frontend <br />
Rename .env.example to .env <br />
And edit the values in there <br />
Replace REACT_APP_CONTRACT_ID with your deployed contract ID <br />
Replace REACT_APP_TEMPLATE_CLIENT_ID by following the below link <br />
https://portal.thirdweb.com/api-keys <br />
Then run these commands <br />
```
cd frontend/
yarn install
yarn start
```

4)To run key exchange server <br />
Run these <br />
```
cd key-exchange-server/
npm i
node server.js
```

# is213
README

[IS213] G7-T6 : ECOPAL
Welcome to ECOPAL, where here, we aim to encourage eco-friendly habits starting from reducing the use of single-use plastic bags. Statistics show that in Singapore, over 2.5 billion plastic bags are used each year - a major contributor to the amount of waste generated in the country which may also pose a threat to the environment if not properly disposed of.
With ECOPAL, we encourage eco-friendliness through incentivisation and building communities. Through identifying key reasons that contribute to people’s lack of motivation to adopt eco-friendly practices, we embarked on implementing the best features in our app.
In providing attractive rewards, ECOPAL uses a tiering system - Bronze, Silver and Gold, which offers different rewards and in building communities, ECOPAL aims to connect like-minded individuals and engage them through eco-friendly activities and events.

Key Features
Our application supports the following:
Supermarket Transactions
Special Event Rewards
ECOPAL Events

1. Supermarket Transactions

This scenario describes a user's experience when transacting with ECOPAL at a participating supermarket. Users can earn reward points by bringing their own bags to the store. The user provides transaction details, such as a unique transaction ID and transaction amount, as well as their email address. The backend service then returns the rewards that the user is eligible for. Users can then choose a reward to use, redeem the reward, and complete the transaction with the discounted price.

The microservices involved in this scenario are:
- Update Points complex microservice
- Transaction service
- User service
- Reward service

The external service used is a cross-browser QRCode generator, which converts discount information into a QR code.


2. Special Event Rewards

This scenario describes an admin's process for adding a new reward to the database for ECOPAL users to use. Once the reward has been added, the admin can promptly broadcast the reward through email to existing users using the SendinBlue email API.

The microservices involved in this scenario are:
- Rewards service
- Send Email complex microservice
- User microservice
- Email microservice

The external service used is the SendinBlue API, which creates and sends transactional emails and allows for batch sending of customised emails.


3. ECOPAL Events

This scenario describes a user's experience in joining an event, as well as an admin's experience in creating and deleting events. The application also sends messages to users to encourage them to sign up for events or to notify them when an event has been deleted.

The microservices involved in this scenario are:
- Join Events Complex Microservice
- Events service
- Participant service
- Edit Events service


Setting up

1. How to run
To set up our web application locally based on the .zip file

Here are the requirements (for Mac):
MAMP server
Install MAMP: https://www.mamp.info/en/downloads/ 
Docker
Install Docker: https://www.docker.com/products/docker-desktop/

Here are the requirements (for Windows):
WAMP server
Install WAMP: https://www.wampserver.com/en/ 
Docker
Install Docker: https://www.docker.com/products/docker-desktop/ 

2. How to start the application:
- Run Docker on your desktop
- Run MAMP / WAMP
- Open http://localhost/phpmyadmin
- In the project folder, open the DB folder and import all databases into PHPmyadmin
- Start Docker and change all the docker ids in docker-compose.yml to your own docker id
- Open your terminal and cd microservice
- Run docker-compose up
- In project folder, open AdminUI.html and UserProfile.html
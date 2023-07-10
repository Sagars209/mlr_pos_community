# mlr-pos-community

Prerequisites

Versions
Compatible with Odoo 16.


Installation (see this video for tutorial on Odoo module installation)
1. Download repository and place extracted folder in the Odoo addons folder.
2. Login to Odoo database to upgrade and enable developer mode under settings.
3. Under apps Update the App list.
4. Search for the module (MLR) and install.

Setup

1. In Odoo navigate to Point of Sale-> Configuration -> BTCpay server instance.
2. Click New to create a new record.
   ![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/002bd8f6-9223-4512-97e8-4c26ee669310)
4. Enter a Name for the Instance and Company Name to display on the receipt. Enter the expiration 
5. Login into the BTCpay server to be used and navigate to Account -> API Key. Create a key with full priviledges.
6. From BTCpay server copy the following information and paste in the Odoo BTCpay server Instance record: the server base URL, API key, and enter the password to BTCpay server.
   ![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/4ca911a4-94b2-46ff-90e6-fc88e73873d2)
7. Click Test Connection to verify the information is correct. If it is correct a green popup will affirm so, if it is incorrect a red popup will appear.
8. Click Activate to make BTCpay instance a current method (the first time a new Accounting Journal BTCpay will be created and used for recording transactions).
9. In Configuration -> Payment Methods add BTCpay.

Operation
1. From the Point of Sale Dashboard open a New Session.
2. After creating an order click Create Invoice to generate Lightning Invoice. The generated invoice ID from BTCpay server will appear on a popup, acknowledge by clicking Ok.
3. To view the invoice QR code click Bill.


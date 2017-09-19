The BasicUserTracker is MAKEmory's way of keeping stats on how many and what kinds of interactions our employees have with our customers. It does this by executing a script through Amazon Web Services that communicates with and records on google spread sheets.

The tracker works via the intersection of several things - AWS Button, Lambda service, Google OAuth, and gspread.

AWS BUTTON / LAMBDA:

It works via the Amazon Button -- a device that when pressed executes the corresponding python script (this script can be found in the gspread_button_update.py file). The script is executed on the Amazon Web Service "Server-less" Lambda feature, which you can access if you have an AWS account (Sign in --> AWS Management Console --> Search "Lambda"). You can create a new function in Lambda and attach "triggers" (like the button) to this function. Access to the script that is being run is from Robin's account.

However, and this is where things start to get convoluted, if your script needs to import modules that are not in the AWS SDK (which is pratically any module in python, JS, etc.), then you need to create what's called a deployment package. A deployment package is a directory that contains in it all the modules you need to run the script, necessary files for authentication, as well as the script. There is a defined structure to them and this can be found here -- https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html (specifically for python, but the idea is relatively the same for whatever language you choose).

Referring to line 66 -
This formatting is crucial to running the script. When the button is pressed, the script refers to the handler, which then executes the rest of the code.

Google OAuth and gspread:

gspread is friggin' awesome because it basically helps you circumvent a lot of the craziness that is working through the Google OAuth process (I linked the API for gspread in gspread_button_update.py).

To begin, you need to head to the Google API Dashboard (while signed in to the account that is hosting the spread sheet) and activate the relevant APIs (in this case, this is the Sheets and Drive API). Then, follow the instructions to receive the relevant credentials (the JSON KEYFILE).

Referring to lines 12-14:
The JSON KEYFILE is crucial as it provides the script with the necessary permissions.

The SHEET ID is just a string of characters and numbers in the URL of the sheet (between "d/" and "/edit") -
https://docs.google.com/spreadsheets/d/1vdifwbycoT7rW9WmRCOuXkjsyTRcxV2P72YbwCqjszY/edit#gid=0

The scope refers to what permissions the Sheets API grants you - the one in the code basically gives you read and write permissions.


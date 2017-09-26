The BasicUserTracker is MAKEmory's way of keeping stats on how many and what kinds of interactions our employees have with our customers. It does this by executing a script through Amazon Web Services that communicates with and records on google spread sheets.

The tracker works via the intersection of several things - AWS Button, Lambda service, Google OAuth, and gspread.

DISCLAIMER: This code is written in python, and there are some python specific things I did to set it up. In case you are scripting in a another language, I've put headers to let you know what you can skip over.

AWS BUTTON / LAMBDA:

The Amazon Button is a device that when pressed executes the corresponding python script (this script can be found in the gspread_button_update.py file). The script is executed on the AWS "Server-less" Lambda feature, which you can access if you have an AWS account (Sign in --> AWS Management Console --> Search "Lambda"). You can create a new function (like our python script) in Lambda and attach "triggers" (the button) to this function. Access to the script that is being run is solely from Robin's account, for obvious reasons.

However, and this is where things start to get complicated, if your script needs to import modules that are not in the AWS SDK (which is pratically any module in python, JS, etc.), then you need to create a "deployment package." This is a directory that contains in it all the modules you need to run the script, necessary files for authentication (such as our JSON KEYFILE), and the script itself. There is a defined structure to them (documentation -- https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html -- that one is specifically for python, but you can find the doc relevant to whatever language you're using).



SETTING UP / DEPLOYING IN LAMBDA

What SHOULD BE UNDERSTOOD from that link is that your script must be in the root of the deployment package. Lambda WILL NOT BE ABLE to find the script otherwise. The same is true of the modules imported in the script. So your package should look like this:

+--------------+

|script.py
|JSON KEYFILE
|module1
|module2
|.....
|module n
|.....

(Robin can also help if there any questions about this since he actually has the file)

DISREGARD THIS NEXT SECTION IF YOU'RE NOT SCRIPTING IN PYTHON:

With this, I used two pieces of software to actually create the package 
  - pip (https://pypi.python.org/pypi/pip)
  - virtualenv (https://pypi.python.org/pypi/virtualenv). 
  
pip is python's version of package management, and if your version of python is 2.7.9+ or 3.4+, then pip actually comes with your installation of python. If you're not using these versions, you need to consider your OS. pip is easy to install if you have bash (so linux and MacOS), but less so with Windows (honestly, figure out how to partition your hard drive, get Ubuntu, and dual boot; your coding world will be way better). Otherwise, figoure how to install pip and virtualenv for Windows. With MacOS, I believe homebrew is the software used for package management.

If you don't need to set environment variables or the ones being set are don't affect your OS in a meaningful way, then don't worry about virtualenv. Otherwise, with virtualenv, you can create an entirely separate environment to script in. What this means is adding variables to your class path, or setting environment variables, without interfering with these really important things in your actual OS. So you can use pip to install packages as necessary, and you can set env vars, building your deployment package in a completely safe, self-contained way.



LAMBDA FIELDS / VARS:

It is also important to note the method in the script called lambda_handler.

This formatting is crucial to running the script. When the button is pressed, the script refers to the handler, and that in turn executes the rest of the code. In the Lambda console, you must specify the handler in the Handler field. The format is simply script_name.handler_method_name.

Next is specifying the environment variables. There's only one, and it's important that GOOGLE_APPLICATION_CREDENTIALS is set to "JSON KEYFILE.json" (quotes included, as this is a symbolic link).



GOOGLE OAUTH / GSPREAD:

gspread is friggin' awesome because it basically helps you circumvent a lot of the craziness that is complying with the Google OAuth process (I linked the API for gspread in gspread_button_update.py).

If you wanted to start from scratch and figure out how to authorize your google account and thus use any of its relative APIs, you start by:
- heading to the Google API Dashboard (while signed in to the account that is hosting the spread sheet)
- making a developer account
- enabling the relevant APIs (in this case, I enabled the Sheets and Drive API)
- following the instructions to receive the relevant credentials (the JSON KEYFILE is crucial in this case, but depending on what project you're using determines what kind of authetication you need).

Another kind of esoteric but important detail is that it's necessary to share your sheet with the Google dashboard account you made and received the credentials from. You will likely get an email saying that the email is non-existent or something, but ignore that. 

Referring to lines 12-14:
The JSON KEYFILE is crucial as it provides the script with the necessary permissions.

The SHEET ID is just a string of characters and numbers in the URL of the sheet (between "d/" and "/edit") -
https://docs.google.com/spreadsheets/d/1vdifwbycoT7rW9WmRCOuXkjsyTRcxV2P72YbwCqjszY/edit#gid=0

The scope refers to what permissions the Sheets API grants you - the one in the script basically gives you read and write permissions.


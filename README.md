# QRmoney

-This Python-based project simulates a digital balance system that integrates with QR codes. Each QR code has a unique ID and a value associated with it, which can fluctuate based on the state of the code (active or inactive). When a QR code is scanned, different actions are triggered depending on its current state:

-Active QR Code: If the QR code has not been used before (active), the system allows you to load the value specified on the QR code into your digital balance.
-Inactive QR Code: If the QR code has already been used (inactive), the system requires a certain amount of value to be deducted from your balance to activate the QR code. Once activated, the QR code can be used for future transactions.

# Requirements 

-Python 3.x
Necessary libraries:
qrcode for generating and reading QR codes
json or any database for storing user data and QR code states
flask for website UI

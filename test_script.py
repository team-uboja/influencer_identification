#created by Steffen Schmidt 5/23/2020

import utils



utils=utils.utils()
utils.writeIntoUserDB('steffen','hallo','steffen@hallo.com')
print(utils.check_password('steffen','hallo'))
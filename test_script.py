#created by Steffen Schmidt 5/23/2020

import utils



utils=utils.utils()
utils.writeIntoUserDB('steffen1','hallo123','steffen@hallo.com')
print(utils.check_password('steffen','hallo'))
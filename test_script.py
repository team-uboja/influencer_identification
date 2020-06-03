#created by Steffen Schmidt 5/23/2020

import utils
import messaging_handler


#utils=utils.utils()
#utils.writeIntoUserDB('steffen1','hallo123','steffen@hallo.com')
#print(utils.check_password('steffen','hallo'))

return_values = {}
return_values['from'] = '+18572091961'
return_values['to'] = '+18706863913'
return_values['cost'] = '0.03'
return_values['currency'] = 'USD'
return_values['content'] = "I would vote for +41799113009"
return_values['created'] = None
return_values['sent'] = None
return_values['updated'] = None
return_values['status'] = None
return_values['error_code'] = None
return_values['error_message'] = None
return_values['from_city'] = 'Cambridge'
return_values['from_zip'] = '02138'
return_values['campaign_identifier'] = 'campaign_maboko_1'
return_values['voted_for'] = '+41799113009'
return_values['age'] = '24'

messaging_handler.messaging_handler().writeIntoMessagingDB(return_values, False)
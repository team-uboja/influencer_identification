#created by Steffen Schmidt 5/23/2020

import utils
import messaging_handler


#utils=utils.utils()
#utils.writeIntoUserDB('steffen1','hallo123','steffen@hallo.com')
#print(utils.check_password('steffen','hallo'))
# i=20
# while i>0:
#     return_values = {}
#     return_values['from'] = '+' + str(18572091961+i)
#     return_values['to'] = '+' + str(18706863913-i)
#     return_values['cost'] = '0.03'
#     return_values['currency'] = 'USD'
#     return_values['content'] = "I would vote for +" + str(41799113009-i)
#     return_values['created'] = None
#     return_values['sent'] = None
#     return_values['updated'] = None
#     return_values['status'] = None
#     return_values['error_code'] = None
#     return_values['error_message'] = None
#     return_values['from_city'] = 'Cambridge'
#     return_values['from_zip'] = '02138'
#     return_values['campaign_identifier'] = 'campaign_maboko_1'
#     return_values['voted_for'] = '+' + str(41799113009-i)
#     return_values['age'] = str(24+i)
#
#     messaging_handler.messaging_handler().writeIntoMessagingDB(return_values, False)

# restriction_dict={}
# restriction_dict['from_'] = None
# restriction_dict['to'] = None
# restriction_dict['from_city'] = None
# restriction_dict['campaign_identifier'] = 'campaign_maboko_1'
# restriction_dict['voted_for'] = None
# restriction_dict['age'] = '24'
#
# print(utils.utils().getSelectedDataIncoming(restriction_dict))

utils.utils().barChartData()
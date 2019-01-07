
# Run using python -m tests.tests

import json
import coparse

#Open tests config file
with open("tests/tests.json",'r') as json_raw:
    test_config =  json.load(json_raw)

#Update progress
print('Running Tests:')
result = test_config['result']
#Process all tests
for test in test_config['tests']:
    #Update progress
    print('- {test}'.format(test=test['name']))
    #Run test
    res = coparse.parse(test['query'],debug=True)
    #Check for success
    if not res['success']:
        print (' * Query: {query}'.format(query=res['debug']['query'].encode('utf-8')))
        print (' * Error: {error}'.format(error=res['error']))
    else: 
        #Check against expected methods
        if  res['debug']['method'] != 'Unknown' and res['debug']['method'] != test['method']:
            print (' * Query: {query}'.format(query=res['debug']['query'].encode('utf-8')))
            print (' * Error: Incorrect Method {returned} (should be {expected})'.format(returned=res['debug']['method'],expected=test['method']))
        #Check against expected longitude
        elif round(res['result']['x'],4) != round(result['x'],4):   
            print (' * Query: {query}'.format(query=res['debug']['query'].encode('utf-8')))
            print (' * Error: Incorrect longitude {returned} (should be {expected})'.format(returned=res['result']['x'],expected=result['x']))
        #Check against expected latitude
        elif round(res['result']['y'],4) != round(result['y'],4):
            print (' * Query: {query}'.format(query=res['debug']['query'].encode('utf-8')))
            print (' * Error: Incorrect latitude {returned} (should be {expected})'.format(returned=res['result']['y'],expected=result['y']))
        #Indicate pass
        else:
            print(' - Passed')
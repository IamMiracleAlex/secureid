from collections import OrderedDict

from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer



#####################################
#####################################
# DO NOT MODIFY THIS FILE
######################################
######################################


class SuccessResponse:
    '''Standardise API Responses and add additional keys'''
    
    def __new__(cls,  data={}, message = 'successful', status=status.HTTP_200_OK):
        return Response(
            {
                'code': status,
                'status': 'Success',
                'message': message,
                'data': data
            },
            status
        )

class FailureResponse:
    def __new__(cls, message = 'Error', status=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                'code': status,
                'status': 'Failed',
                'message': message
            },
            status
        )


class CustomJSONRenderer(JSONRenderer):
    '''Override the default JSON renderer to be consistent and have additional keys'''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        status = 'Success' if status_code < 400 else 'Failed'
        message = 'successful' if status else 'Error'
        
        # when response data is a list, convert to dict
        if isinstance(data, list):
            data = {
                'code': status_code,
                'status': status,
                'message': message,
                'data': data
            }
    
        # if response data is none, convert to dict
        if data is None:
            data = {}

        # if response data is not well formated dict, and not an error response, convert to right format
        if isinstance(data, OrderedDict) and ('data' not in data) and ('non_field_errors' not in data):
            data = {
                'code': status_code,
                'status': status,
                'message': message,
                'data': data,
            }

        # convert non_field_errors message to text, instead of list
        if 'non_field_errors' in data:
            data['message'] = data.pop('non_field_errors')[0]
        
        if not 'code' in data:
            data['code'] = status_code
            
        # if not `status` in response, add status
        if not 'status' in data:
            data['status'] = status
   
        # if no `message` in response, add message based on status
        if not 'message' in data:
            data['message'] = message

        # Added this so we can use `.move_to_end` to make `status` & `message` come on top  
        # if isinstance(data, dict):
            # data = OrderedDict(data.items()) 

        # removing to increase spead, since this is O(N), and only needed when 
        # returning some error responses 
        # data.move_to_end('message', last=False)
        # data.move_to_end('status', last=False)

        return super().render(data, accepted_media_type, renderer_context)

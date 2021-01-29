import math
from hls4ml.converters.pytorch_to_hls import pytorch_handler
from hls4ml.converters.utils import * #Get parse data format and the two padding functions 

#Assuming version 0.5.0 not in master branch yet
pooling_layers = ['MaxPool1D', 'MaxPool2D', 'AvgPool1D', 'AvgPool2D']
@pytorch_handler(*pooling_layers) #Iterate through the 4 types of pooling layers
def parse_pooling_layer(pytorch_layer, layer_name, input_shapes, data_reader, config):
    
    layer = {}
    
    layer['name'] = layer_name
    layer['class_name'] = pytorch_layer['class_name']
    layer['data_format'] = 'channels_first' #By Pytorch default, cannot change
    
    
    #check if 1D or 2D by getting the class name and get the second to last character
    if int(layer['class_name'][-2]) == 1:
        
        '''Compute number of channels'''
        (layer['n_in'], layer['n_filt']) 
                    = parse_data_format(input_shapes[0], 'channels_first')
        
        #prepare padding input
        layer['pool_width'] = pytorch_layer.config['pool_size']#Not sure about this one
        layer['stride_width'] = pytorch_layer.stride[0] #Got this from another document
        layer['padding'] = pytorch_layer.padding[0]
        
        '''Compute padding 1d'''
        #hls4ml layers after padding
        (
        layer['n_out'], 
        layer['pad_left'],
        layer['pad_right']
        ) 
        = compute_padding_1d(
        layer['padding'], layer['n_in'],
        layer['stride_width'], layer['pool_width']
        )
        
        #Assuming only 'channels_first' is available
        output_shape=[input_shapes[0][0], layer['n_filt'], layer['n_out']]
        
    elif int(layer['class_name'][-2]) == 2:
        
        '''Compute number of channels'''
        (layer['in_height'], layer['in_width'], layer['n_filt']) 
                    = parse_data_format(input_shapes[0], 'channels_first')

        layer['stride_height'] = pytorch_layer.stride[0]
        layer['stride_width'] = pytorch_layer.stride[1]
        layer['pool_height'] = pytorch_layer. IDK
        layer['pool_width']=pytorch_layer. IDK
        layer['padding']=pytorch_layer.padding[0] 
        #pytorch_layer.padding is an object with attributes lower()--> Should output 'same' or 'valid' or otherwise unsupported

        #hls4ml layers after padding
        (
        layer['out_height'], layer['out_width'], 
        layer['pad_top'], layer['pad_bottom'], 
        layer['pad_left'], layer['pad_right']
        ) 
        = compute_padding_2d(
        layer['padding'],
        layer['in_height'], layer['in_width'],
        layer['stride_height'],layer['stride_width'],
        layer['pool_height'], layer['pool_width']
        )
        #Only channels_first is available in pytorch. cannot change
        output_shape=[input_shapes[0][0], layer['n_filt'], layer['out_height'], layer['out_width']]
    
    
    #Return parsed layer and output shape
    return layer, output_shape         
        
        
        
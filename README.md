# ads_web_api

Simple web API interface build with flask to give access to data on a Beckhoff PLC.  
The whole API interface can be descriped in a single text file.  
Possibility to read directly by PLC variable name.

The API is defined by one or more calls of which each contains a number of data request points.  
## API definition structure
```
{
  "request_1": {
    "data_access_point1": {
      "var": "Main.MyTestVar1",
      "lable": "Var1",
      "description": "Explain what informaiton you provide here"
    },
    "data_access_point2": {
      "var": "Main.MyTestVar2",
      "lable": "Var2",
      "description": "Explain what informaiton you provide here"
    }
  },
  "request_2": {
    ...
  }
}
```

## Example requests
### Request request_1  
localhost:5000/api/call_1  
### Response request_1  
```
{
  "data_access_point1": 132.32,
  "data_access_point2": true,
}
```

### It's possible to request a single data point or a list of data points
 localhost:5000/api/call_1?data_access_point1  
### Response request_1  
```
{
  "data_access_point1": 132.32,
}
```

### Request the API description  
localhost:5000/api/apiinfo  
### Response API definition  
The variable names are ommited in the response if "omit_var_names" is set to true in config.json  
```
{
  "request_1": {
    "data_access_point1": {
      "var": "Main.MyTestVar1",
      "lable": "Var1",
      "description": "Explain what informaiton you provide here"
    },
    "data_access_point2": {
      "var": "Main.MyTestVar2",
      "lable": "Var2",
      "description": "Explain what informaiton you provide here"
    }
  },
  "request_2": {
    ...
  }
}
```

### Request values directly by PLC variable names
This needs to be allowed in config.json by setting "allow_var_req" to true

localhost:5000/api/readvar?Main.MyTestVar1+Main.MyTestVar2  

### Response 
```
{
  "Main.MyTestVar1": 132.32,
  "Main.MyTestVar2": true,
}
```

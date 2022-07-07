# ads_web_api

Simple web API interface build with flask to give access to data on a Beckhoff PLC.  
The whole API interface can be descriped in a single text file.  
Possibility to read directly by PLC variable name.

The API is defined by one or more calls of which each contains a number of data request points.  
## API definition structure
```
{
  "call_1": {
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
  ...more calls...
}
```

## Example requests
### Request call_1  
localhost:5000/api/call_1  
### Response call_1  
```
{
  "data_access_point1": 132.32,
  "data_access_point2": true,
  
}
```

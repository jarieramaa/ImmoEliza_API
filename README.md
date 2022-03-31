# ImmoEliza_API

Numpy numpy-1.22.3
flask-2.1.0
pandas-1.4.1
requests-2.27.1
pycurl-7.45.1
matplotlib-3.5.1



### data description

```json
{
  "data": {
    "living-area": int,
    "property-subtype": ['APARTMENT_BLOCK' | 'BUNGALOW' | 'CASTLE' |
    				       'CHALET' | 'COUNTRY_COTTAGE' |'DUPLEX' | 
    				       'EXCEPTIONAL_PROPERTY' | 'FARMHOUSE' | 'FLAT_STUDIO' |
    				       'GROUND_FLOOR' | 'KOT' | 'LOFT' | 'MANOR_HOUSE' |
    				       'MANSION' | 'MIXED_USE_BUILDING'| 'OTHER_PROPERTY' |
    				       'PENTHOUSE' | 'SERVICE\_FLAT' | 'TOWN_HOUSE' | 'TRIPLEX' |
    				       'VILLA']
    "zip-code": int,
    "land-area": Optional[int],
    "kitchen-type": Optional['Hyper equipped'| 'Installed'|'Not installed'|
                             'Semi equipped'|'USA hyper equipped'|'USA installed'|
                             'USA semi equipped'|'USA uninstalled',
    "swimming-pool" : Optional[bool],
    "energy-class" : "Optional : ['A'| 'A+'| 'B'| 'C'| 'C\_B'| 'D'|
    								   'E'| 'F'| 'F\_B'| 'G'| 'G\_C'| 'G\_D']
    "street-address": Optional(Str)
    "house-number" : Optional(int)
    ]
  }
}
```


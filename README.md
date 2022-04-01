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
  "data" : {
    "living-area": int,
    "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
    "property-subtype": [ "APARTMENT_BLOCK" | "BUNGALOW" | "CASTLE"
                      | "CHALET" | "COUNTRY_COTTAGE" | "DUPLEX" | "EXCEPTIONAL_PROPERTY"
                      | "FARMHOUSE" | "FLAT_STUDIO" | "GROUND_FLOOR" | "KOT" | "LOFT"
                      | "MANOR_HOUSE" | "MANSION" | "MIXED_USE_BUILDING" | "OTHER_PROPERTY"
                      | "PENTHOUSE" | "SERVICE_FLAT" | "TOWN_HOUSE" | "TRIPLEX" | "VILLA"],
    "zip-code": str,
    "land-area": Optional[int],
    "kitchen-type": Optional[ "Hyper equipped" | "Installed" | "Not installed"
                    | "Semi equipped" | "USA hyper equipped" | "USA installed" | "USA semi equipped"
                    | "USA uninstalled" ],
    "swimming-pool": Optional[bool],
    "energy-class": Optional["A" | "A+" | "B" | "C" | "C_B" | "D" | "E" | "F" | "F_B" | "G" | "G_C" | "G_D" ],
    "street": Optional(str),
    "house-number": Optional(int)},
    "rooms-number": Optional[int],
    "garden": Optional[bool],
    "garden-area": Optional[int],
    "furnished": Optional[bool],
    "open-fire": Optional[bool],
    "terrace": Optional[bool],
    "terrace-area": Optional[int],
    "facades-number": Optional[int],
    "building-state": Optional["NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"]}
```


```json
    {
        "area": 300,
        "property-type" : "APARTMENT",
        "property-subtype": "FLAT_STUDIO",
        "zip-code": 1301,
        "land-area": 581,
        "kitchen-type": "Not installed",
        "swimming-pool" : false,
        "energy-class": "F",
        "street": "sdfa",
        "house-number": 190,
        "rooms-number": 5,
        "garden": true,
        "garden-area": 130,
        "furnished": true,
        "open-fire": true,
        "terrace": true,
        "terrace-area": 57,
        "facades-number": 3,
        "building-state": "JUST RENOVATED"
    }

```

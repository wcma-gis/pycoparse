# Coparse

Coordinate parser for use in python which parses coordinates in DD. DM, DMS and UTM coordinates, returning a standardised DD json object. By default the parser accepts coordinates in Long/Lat or UTM format.

## Requirements

Uses the UTM library

## Use

Import the library into your python project

`import coparse`

Pass your query string to the libary, if successful it will return a coordinate object

`coparse.parse('146° 2.3153' -41° 48.3037')`

### Supported Query Formats
Queries can be passed in Degrees, Decimal Degrees, Degrees Minutes Seconds or UTM format. The following are some examples of supported query strings.

#### Decimal Degrees (Long Lat)

The following are tested variants on a value passed as Decimal Degrees:

 * 146.038588 -41.805062
 * E146.038588 S41.805062
 * 146.038588E 41.805062S

#### Degrees Decimal Minutes (Long Lat)

The following are tested variants on a value passed as Degrees Decimal Minutes:

 * 146° 2.3153' -41° 48.3037'
 * E146° 2.3153' S41° 48.3037'
 * 146° 2.3153'E 41° 48.3037'S
 * 146° 2.3153' -41° 48.3037'
 * 146 2.3153 -41 48.3037
 * 146 2.3153E 41 48.3037S

#### Degrees Minutes Seconds (Long Lat)

The following are tested variants on a value passed as Degrees Minutes Seconds:

 * 146° 2' 18.9168" -41° 48' 18.2226"
 * E146° 2' 18.9168" S41° 48' 18.2226"
 * 146° 2' 18.9168"E 41° 48' 18.2226"S
 * 146 2 18.9168 -41 48 18.2226
 * E146 2 18.9168 S41 48 18.2226
 * 146 2 18.9168E 41 48 18.2226S

#### UTM (Zone Easting Northing)

The following are tested variants on a value passed as UTM:

 * S55 420135E 5371420N
 * 55S E420135 N5371420

Note the zone component of the coordinate contains the zone number of its hemisphere, not zone letter as is sometimes used.

#### Notes

The only charactors supported to seperate coordinate groups are semi colons, comma's and spaces.

All methods use WGS 84

## Response

### Successful Query

simple

```json
{
  "success": true,
  "result": {
        "y": "-74.123",
        "x": "40.123"
    }
}
```

### Unsuccessful Query

```json
{
  "success": false,
  "error_msg": "Latitude minutes out of bounds [Expected:0,60 Value: 371420]"
}
```
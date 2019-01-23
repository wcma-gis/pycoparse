import math
import re

def parse( query, debug=False):

    # Setup result
    result = {}

    # Check for query
    if not query:
        result['success'] = False
        result['error'] = "No query sent"
        return result

    # Strip query of unneccessary char
    clean = re.sub(r"[^\-a-z0-9\.\ \,\;]+",'',query.lower()).encode('ascii', 'ignore')

    # Get coordinate groups
    parts = []
    matches = re.finditer(r"([\-a-z]?)(\d+\.?\d*)([a-z]?)", clean)
    for i, match in enumerate(matches, start=1):
        part = []
        for grpNumber in range(0, len(match.groups())):
            part.append(match.group(grpNumber+1))
        parts.append(part)

    # Update debug
    if debug:
        result['debug'] = {}
        result['debug']['query'] = query
        result['debug']['parsed'] = clean
        result['debug']['parts'] = parts

    # Guess coord type by counting parts
    if (len(parts) == 2):
            # Lat long in DD
        method = "DD"
        pt = fromDD(parts)
    elif (len(parts) == 3):
        # UTM
        method = "UTM"
        pt = fromUTM(parts)
    elif (len(parts) == 4):
        # Lat long in DM
        method = "DM"
        pt = fromDM(parts)
    elif (len(parts) == 6):
        # Lat long in DMS
        method = "DMS"
        pt = fromDMS(parts)
    else:
        result['success'] = False
        result['error'] = "Cannot determine coordinate type"
        return result

    # Update debug
    if debug:
        result['debug']['method'] = method

    # Check point
    if pt['error']:
        result['success'] = False
        result['error'] = pt['error_msg']
        return result
    else:
        result['success'] = True
        result['result'] = {'x': pt['lng'], 'y': pt['lat']}
        lat = round(pt['lat'], 6)
        lng = round(pt['lng'], 6)
        result['display'] = '{lng} {lat}'.format(lng=lng, lat=lat)

    return result

def fromDD(parts):
    # Converts a DD coordinate into a DD object
    #
    # @param {*} parts 2 part list consisting of lat decimal degrees, lng decimal degrees with the format [string,prefix,value,postfix]
    # @returns DD object

    # Parse parts
    lng = float(parts[0][1])
    lat = float(parts[1][1])
    # Parse hemispheres
    if (parts[0][0] in ["w","-"] or parts[0][2] == "w"):
        lng *= -1
    if (parts[1][0] in ["s","-"] or parts[1][2] == "s"):
        lat *= -1
    # Validate results
    if (lat >= 90 or lat <= -90):
        return {
            'error': True,
            'error_msg': "Latitude degrees out of bounds [Expected:-90,90 Value: " +
            str(lat) +
            "]"
        }
    if (lng >= 180 or lng <= -180):
        return {
            'error': True,
            'error_msg': "Longitude degrees out of bounds [Expected:-180,180 Value: " +
            str(lng) +
            "]"}
    # Return coords
    return {
        'lat': lat,
        'lng': lng,
        'error': False
    }

def fromDM(parts):
    # Converts a DM coordinate into a DD object
    #
    # @param {*} parts 4 part array consisting of lat degrees, lat decimal minutes, lng degrees, lng decimal minutes with the format [string,prefix,value,postfix]
    # @returns DD object

    # Parse parts
    dlng = float(parts[0][1])
    mlng = float(parts[1][1])
    dlat = float(parts[2][1])
    mlat = float(parts[3][1])
    # Parse hemispheres
    if (parts[0][0] in ["w","-"] or parts[0][2] == "w" or parts[1][2] == "w"):
        dlng *= -1
    if (parts[2][0] in ["s","-"] or parts[2][2] == "s" or parts[3][2] == "s"):
        dlat *= -1
    # Validate results
    if (dlat >= 90 or dlat <= -90):
        return {
            'error': True,
            'error_msg': "Latitude degrees out of bounds [Expected:-90,90 Value: " +
            str(dlat) +
            "]"
        }
    if (dlng >= 180 or dlng <= -180):
        return {
            'error': True,
            'error_msg': "Longitude degrees out of bounds [Expected:-180,180 Value: " +
            str(dlng) +
            "]"}
    if (mlat <= 0 or mlat >= 60):
        return {
            'error': True,
            'error_msg': "Latitude minutes out of bounds [Expected:0,60 Value: " +
            str(mlat) +
            "]"
        }
    if (mlng <= 0 or mlng >= 60):
        return {
            'error': True,
            'error_msg': "Longitude minutes out of bounds [Expected:0,60 Value: " +
            str(mlng) +
            "]"}
    lng = dlng + (math.copysign(mlng,dlng)) / 60
    lat = dlat + (math.copysign(mlat,dlat)) / 60
    # Return coords
    return {
        'lat': lat,
        'lng': lng,
        'error': False
    }

def fromDMS(parts):
    # Converts a DM coordinate into a DD object
    #
    # @param {*} parts  6 part array consisting of lat degrees, lat minutes, lat seconds, lng degrees, lng minutes, lng seconds with the format [string,prefix,value,postfix]
    # @returns DD object

    # Parse parts
    dlng = float(parts[0][1])
    mlng = float(parts[1][1])
    slng = float(parts[2][1])
    dlat = float(parts[3][1])
    mlat = float(parts[4][1])
    slat = float(parts[5][1])
    # Parse hemispheres
    if (parts[0][0]  in ["w","-"]  or parts[0][2] == "w" or parts[2][2] == "w"):
        dlng *= -1
    if (parts[3][0]  in ["s","-"]  or parts[3][2] == "s" or parts[5][2] == "s"):
        dlat *= -1
    # Validate results
    if (dlat >= 90 or dlat <= -90):
        return {
            'error': True,
            'error_msg': "Latitude degrees out of bounds [Expected:-90,90 Value: " +
            str(dlat) +
            "]"
        }
    if (dlng >= 180 or dlng <= -180):
        return {
            'error': True,
            'error_msg': "Longitude degrees out of bounds [Expected:-180,180 Value: " +
            str(dlng) +
            "]"}
    if (mlat <= 0 or mlat >= 60):
        return {
            'error': True,
            'error_msg': "Latitude minutes out of bounds [Expected:0,60 Value: " +
            str(mlat) +
            "]"
        }
    if (mlng <= 0 or mlng >= 60):
        return {
            'error': True,
            'error_msg': "Longitude minutes out of bounds [Expected:0,60 Value: " +
            str(mlng) +
            "]"}
    if (slat <= 0 or slat >= 60):
        return {
            'error': True,
            'error_msg': "Latitude seconds out of bounds [Expected:0,60 Value: " +
            str(slat) +
            "]"
        }
    if (slng <= 0 or slng >= 60):
        return {
            'error': True,
            'error_msg': "Longitude seconds out of bounds [Expected:0,60 Value: " +
            str(slng) +
            "]"}
    lng = dlng + (math.copysign(mlng,dlng)) / 60 + (math.copysign(slng,dlng) / 3600)
    lat = dlat + (math.copysign(mlat,dlat)) / 60 + (math.copysign(slat,dlat) / 3600)

    # Return coords
    return {
        'lat': lat,
        'lng': lng,
        'error': False
    }

def fromUTM(parts):
    # Converts a DM coordinate into a DD object
    #
    # @param {*} parts 3 part array consisting of lat degrees, lat minutes, lat seconds, lng degrees, lng minutes, lng seconds with the format [string,prefix,value,postfix]
    # @returns DD object

    # Parse input
    hemi = "N"
    if (parts[0][0] == "s" or parts[0][0] == "-" or parts[0][2] == "s"):
        hemi = "S"
    zone = int(parts[0][1])
    easting = float(parts[1][1])
    northing = float(parts[2][1])
    # Validate results
    if (zone <= 0 or zone > 60):
        return {
            'error': True,
            'error_msg': "Zone out of bounds [Expected:0,60 Value: " +
            str(zone) +
            "]"
        }
    if (easting < 100000 or easting > 1000000):
        return {
            'error': True,
            'error_msg': "Easting out of bounds [Expected:100000,999999 Value: " +
            str(easting) +
            "]"}
    if (northing < 0 or northing > 10000000):
        return {
            'error': True,
            'error_msg': "Northing out of bounds [Expected:0,10000000 Value: " +
            str(northing) +
            "]"
        }

    coord = utmToLatLng(zone, easting, northing, hemi == 'N')

    # Return coords
    return {
        'lat': coord[0],
        'lng': coord[1],
        'error': False
    }

# Derrived from https://stackoverflow.com/questions/343865/how-to-convert-from-utm-to-latlng-in-python-or-javascript
# TODO: Align method and exact e values to parent coparse libary
def utmToLatLng(zone, easting, northing, northernHemisphere=True):
    if not northernHemisphere:
        northing = 10000000 - northing

    a = 6378137
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996

    arc = northing / k0
    mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 *
                        math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

    ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / \
        (1 + math.pow((1 - e * e), (1 / 2.0)))

    ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

    cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
    cc = 151 * math.pow(ei, 3) / 96
    cd = 1097 * math.pow(ei, 4) / 512
    phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + \
        cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

    n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

    r0 = a * (1 - e * e) / \
        math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
    fact1 = n0 * math.tan(phi1) / r0

    _a1 = 500000 - easting
    dd0 = _a1 / (n0 * k0)
    fact2 = dd0 * dd0 / 2

    t0 = math.pow(math.tan(phi1), 2)
    Q0 = e1sq * math.pow(math.cos(phi1), 2)
    fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 -
                9 * e1sq) * math.pow(dd0, 4) / 24

    fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 *
                e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

    lof1 = _a1 / (n0 * k0)
    lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
    lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 *
            e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
    _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
    _a3 = _a2 * 180 / math.pi

    latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

    if not northernHemisphere:
        latitude = -latitude

    longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

    return (latitude, longitude)

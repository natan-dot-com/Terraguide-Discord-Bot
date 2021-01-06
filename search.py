from math import floor

def binary_search(JSONData, low, high, ID):
    if high >= low:
        mid = floor((high + low) // 2)
        if int(JSONData[mid]['id']) == ID:
            return JSONData[mid]
        elif int(JSONData[mid]['id']) > ID:
            return binary_search(JSONData, low, mid-1, ID)
        elif int(JSONData[mid]['id']) < ID:
            return binary_search(JSONData, mid+1, high, ID)
    return
luhn_map = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 1, 6: 3, 7: 5, 8: 7, 9: 9}


def check_imei(imei):
    if len(imei) != 15:
        return False
    if not imei.isdigit():
        return False
    result = (sum([int(x) for x in imei[::-2]]) + sum([luhn_map[int(x)] for x in imei[1::2]])) % 10
    if result == 0:
        return True
    return False

from datetime import date, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo
from app.errors import DataError
from .values import whole, parts, instant


def evaluate(row):
    try:
        day = date.fromisoformat(row['营业日'])
    except ValueError as error:
        raise DataError('BUSINESS','营业日无效') from error
    cutoff = whole(row['营业截止小时'],0,23)
    entries, seen = [], set()
    for item in parts(row['账务流水']):
        fields = item.split(',')
        if len(fields) != 4 or fields[1] not in {'SIGN','CASH','REFUND'} or not fields[2]:
            raise DataError('BUSINESS',f'账务流水缺列 {item}')
        stamp, kind, key, amount = fields
        if key in seen:
            raise DataError('BUSINESS',f'流水号重复 {key}')
        seen.add(key)
        entries.append((instant(stamp),kind,key,whole(amount,1,10**10)))
    priority = {'SIGN':0,'CASH':1,'REFUND':2}
    debt = received = refunded = total = 0
    proof = []
    for stamp,kind,key,amount in sorted(entries,key=lambda e:(e[0],priority[e[1]],e[2])):
        if kind == 'SIGN':
            if debt:
                raise DataError('BUSINESS','同一单出现多条签收')
            debt += amount
        elif kind == 'CASH':
            received += amount
            if received > debt:
                raise DataError('BUSINESS','累计实收超过签收金额')
        else:
            refunded += amount
            if refunded > received:
                raise DataError('BUSINESS','累计退款超过实收金额')
        local = stamp.astimezone(ZoneInfo('Asia/Shanghai'))
        business_day = local.date() + timedelta(days=local.hour >= cutoff)
        if business_day == day and kind != 'SIGN':
            change = amount if kind == 'CASH' else -amount
            total += change
            proof.append((key,change,'分'))
    proof.append(('未收金额',debt-received,'分'))
    return Decimal(total), proof

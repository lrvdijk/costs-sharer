import sys
import json
from decimal import Decimal, getcontext
import collections

DEFAULT_PERSONS = [
    'Tjalling',
    'Olga',
    'Mark',
    'Auke',
    'Lucas'
]

def get_status(data):
    status = collections.defaultdict(Decimal)

    for payment in data:
        status[payment['payer']] += Decimal(payment['amount'])

        persons = payment['payed_for']

        if "*" in persons:
            persons.remove("*")
            persons += DEFAULT_PERSONS

        amount_per_person = Decimal(payment['amount']) / len(persons)

        for person in persons:
            status[person] -= amount_per_person

    return status

def list_statusses(data):
    for name, status in data.items():
        print("{name}: {status}".format(name=name, status=status))

    print("Total: {sum}".format(sum=sum(data.values())))

if __name__ == '__main__':
    getcontext().prec = 5
    filename = sys.argv[1] if len(sys.argv) > 2 else "payments.json"

    with open(filename) as f:
        data = json.load(f)

        statusses = get_status(data)
        list_statusses(statusses)







import os
import sys
import json
from decimal import Decimal, getcontext
import collections

from jinja2 import Environment, FileSystemLoader

DEFAULT_PERSONS = [
    'Tjalling',
    'Olga',
    'Mark',
    'Auke',
    'Lucas'
]

ReportEntry = collections.namedtuple('ReportEntry', ['desc', 'amount'])

class CostsSharer:
    def __init__(self, data, default_persons=[]):
        self.payments = data
        self.default_persons = default_persons

        self.status = collections.defaultdict(Decimal)
        self.report = collections.defaultdict(list)

    def get_persons(self, persons):
        if "*" in persons:
            persons.remove("*")
            persons += self.default_persons

        return persons

    def gen_report_data(self):
        for payment in self.payments:
            self.status[payment['payer']] += Decimal(payment['amount'])

            persons = self.get_persons(payment['payed_for'])
            amount_per_person = Decimal(payment['amount']) / Decimal(len(persons))

            if payment['payer'] in persons:
                report_amount = Decimal(payment['amount']) - amount_per_person
            else:
                report_amount = Decimal(payment['amount'])

            self.report[payment['payer']].append(
                ReportEntry(
                    desc=payment['description'],
                    amount=report_amount.quantize(Decimal('.01'))
                )
            )

            for person in persons:
                self.status[person] -= amount_per_person

                if person != payment['payer']:
                    self.report[person].append(
                        ReportEntry(
                            desc=payment['description'],
                            amount=(-amount_per_person).quantize(Decimal('.01'))
                        )
                    )

    def gen_report(self, outfile):
        env = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')))
        report_tpl = env.get_template('report.html')

        outfile.write(
            report_tpl.render(
                report_data=self.report,
                statusses=self.status,
                total=sum(self.status.values())
            )
        )

if __name__ == '__main__':
    getcontext().prec = 5
    filename = sys.argv[1] if len(sys.argv) > 2 else "payments.json"
    outfilename = "report.html"

    with open(filename) as f:
        data = json.load(f)

        sharer = CostsSharer(data, DEFAULT_PERSONS)

        with open(outfilename, 'w') as outfile:
            sharer.gen_report_data()
            sharer.gen_report(outfile)








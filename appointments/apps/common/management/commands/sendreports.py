from django.core.management.base import BaseCommand

from appointments.apps.common.models import Report
from appointments.apps.common.utils import send_report

class Command(BaseCommand):
    args = ''
    help = 'Sends out all reports with the default appointments set'

    def handle(self, *args, **options):
        # Better do some logging
        reports = Report.objects.filter(enabled=True)
        for report in reports:
            send_report(report)
            
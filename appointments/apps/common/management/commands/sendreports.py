from django.core.management.base import BaseCommand

import logging

from appointments.apps.common.models import Report
from appointments.apps.common.utils import send_report

class Command(BaseCommand):
    args = ''
    help = 'Sends out all reports with the default appointments set'

    def handle(self, *args, **options):
        # Better do some logging
        logger = logging.getLogger(__name__)
        logger.info('sendreports command started')

        # Command logic
        reports = Report.objects.filter(enabled=True)
        for report in reports:
            send_report(report)

        # Finish up
        logger.info('sendreports command finished')        
            
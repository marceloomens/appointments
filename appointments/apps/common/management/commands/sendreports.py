from django.core.management.base import BaseCommand
from django.utils import timezone

import logging, pytz

from datetime import datetime, time, timedelta

from appointments.apps.common.models import Appointment, Report
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
            tz = pytz.timezone(report.constraint.timezone)
            now = datetime.now(tz=tz)

            # Check that this is a relevant weekday this for this report
            if now.weekday() > 4:
                # For now I'll just skip the weekend
                continue

            # Check that the time in the constraint's timezone falls between
            # 00:00 and 01:00 (exclusive)
            if not time(0, tzinfo=tz) <= now.timetz() < time(1, tzinfo=tz):
                # It's not the right time to send this report
                continue
            
            # Check that this report was not sent previously in the last hour
            # last_sent uses server default timezone (settings.TIME_ZONE)
            if not report.last_sent:
                # Report was never sent before; send now
                pass
            elif (timezone.now() - report.last_sent) < timedelta(hours=1):
                # This report was already sent in the last hour
                continue
            
            # It's time to send this report
            logger.info('sending <%s> to %s' % (str(report), str(report.user)))
            
            # I can prevent multiple similar calls by looping per constraint/per report
            appointments = Appointment.objects.filter(constraint=report.constraint, date=now.date()).order_by('time')
            send_report(report, appointments)
            
            report.last_sent = timezone.now()
            report.save()

        # Finish up
        logger.info('sendreports command finished')
                    
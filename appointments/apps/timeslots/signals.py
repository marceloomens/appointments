# The bookings app relies heavily on signals to notifiy listeners of changes to
# existing timeslots. Listeners should utilise these signals to update related
# models accordingly to avoid overbooking.

import django.dispatch

willEvaluateAvailabilityForRange = \
    django.dispatch.Signal(providing_args=['lbound', 'ubound', 'constraint'])
    
# willEvaluateAvailabilityForDate = \
#     django.dispatch.Signal(providing_args=['date',])
# willEvaluateAvailabilityForDateTime = \
#     django.dispatch.Signal(providing_args=['date', 'time',])
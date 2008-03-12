from time import sleep

from models import Message, DontSendEntry, MessageLog
from django.core.mail import *


## configuration settings
# @@@ eventually move to settings.py

# when queue is empty, how long to wait (in seconds) before checking again
EMPTY_QUEUE_SLEEP = 300



def prioritize():
    """
    Yield the messages in the queue in the order they should be sent.
    """
    
    while True:
        while Message.objects.high_priority().count() or Message.objects.medium_priority().count():
            while Message.objects.high_priority().count():
                for message in Message.objects.high_priority().order_by('when_added'):
                    yield message
            while Message.objects.high_priority().count() == 0 and Message.objects.medium_priority().count():
                yield Message.objects.medium_priority().order_by('when_added')[0]
        while Message.objects.high_priority().count() == 0 and Message.objects.medium_priority().count() == 0 and Message.objects.low_priority().count():
            yield Message.objects.low_priority().order_by('when_added')[0]
        if Message.objects.all().count() == 0:
            break


def send_all():
    """
    Send all eligible messages in the queue.
    """
    
    for message in prioritize():
        if DontSendEntry.objects.has_address(message.to_address):
            print "skipping email to %s as on don't send list " % message.to_address
            MessageLog.objects.log(message, 2) # @@@ avoid using literal result code
            message.delete()
        else:
            print "sending message '%s' to %s" % (message.subject, message.to_address)
            MessageLog.objects.log(message, 1) # @@@ avoid using literal result code
            em = EmailMessage(subject=message.subject, body=message.message_body, from_email= message.from_address, to=message.to_address)
            em.send()
            message.delete()



def send_loop():
    """
    Loop indefinitely, checking queue at intervals of EMPTY_QUEUE_SLEEP and
    sending messages if any are on queue.
    """
    
    while True:
        while not Message.objects.all():
            print 'sleeping for %s seconds before checking queue again' % EMPTY_QUEUE_SLEEP
            sleep(EMPTY_QUEUE_SLEEP)
        send_all()

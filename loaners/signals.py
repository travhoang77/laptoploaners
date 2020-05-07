from .models import Loaner, Record
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime
from django.contrib.auth.models import User
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)

@receiver(post_save, sender=Loaner)
def create_record(sender, instance, created, **kwargs):
        if created:
            record = Record(loaner=instance, action=Record.CREATED, borrower=instance.borrower, technician=get_current_authenticated_user(), action_date=datetime.now())
            record.save()
        else:
            if instance.checked_in == False:
                notes = "Loaner due on " + instance.date_in.strftime("%b %d %Y ") + "\n"
                if instance.adapter_included:
                    notes = "Adapter was included"
                record = Record(loaner=instance, action=Record.CHECK_OUT, borrower=instance.borrower, technician=get_current_authenticated_user(), action_date=datetime.now(), notes=notes)

                record.save()


@receiver(pre_save, sender=Loaner)
def create_check_in_record(sender, instance, **kwargs):
        #This test is to make sure the loaner is already exist and is not coming from the Create Loaner View
        if instance.id is not None:
            obj = Loaner.objects.get(pk=instance.id)
            if obj.checked_in == False:
                record = Record(loaner=instance, action=Record.CHECK_IN, borrower=obj.borrower, technician=get_current_authenticated_user(), action_date=datetime.now())
                record.save()


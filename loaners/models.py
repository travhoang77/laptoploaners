from django.db import models
from datetime import datetime, date

class Model(models.Model):
    DELL = 1
    LENOVO = 2
    VENDOR_CHOICES = (
        (DELL, 'Dell'),
        (LENOVO, 'Lenovo'),
    )

    name = models.CharField(max_length=50)
    cpu = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    hard_drive = models.CharField(max_length=50)
    screen = models.CharField(max_length=50)
    vendor = models.PositiveSmallIntegerField(choices=VENDOR_CHOICES)

    def __str__(self):
        return self.name

class Loaner(models.Model):

    @property
    def checked_out(self):
        return not self.checked_in

    @property
    def overdue(self):
        return self.checked_out and (datetime.date(self.date_in) < date.today())

    name = models.CharField(max_length=50)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    service_ticket = models.CharField(max_length=50)
    date_out = models.DateTimeField(null=True, editable=True)
    date_in = models.DateTimeField(null=True, editable=True)
    borrower = models.CharField(max_length=50)
    technician = models.CharField(max_length=50)
    adapter_included = models.BooleanField(default=True)
    checked_in = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Record(models.Model):
    CHECK_OUT = "CHECK OUT"
    CHECK_IN = "CHECK IN"
    CREATED = "CREATED"

    loaner = models.ForeignKey(Loaner, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    borrower = models.CharField(max_length=50)
    technician = models.CharField(max_length=50)
    action_date = models.DateTimeField(null=True, editable=True)
    notes = models.CharField(max_length=1000)
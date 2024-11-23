from django.db import models

from django.contrib.auth.models import User


class Carrier(models.Model):
    name = models.CharField(max_length=100)
    register = models.CharField(max_length=100)
    type = models.CharField(max_length=100)





class Notes(models.Model):
    """Model definition for Notes."""
    notes = models.TextField()

    class Meta:
        """Meta definition for Notes."""

        verbose_name = "Notes"
        verbose_name_plural = "Notess"

    def __str__(self):
        """Unicode representation of Notes."""
        return self.notes
class Report(models.Model):
    """Model definition for Report."""
    CHOICES=[

        ('Arrival','Arrival'),
        ('Departure','Departure'),
    ]
    date = models.DateField(blank=True,null=True)
    time = models.TimeField(blank=True,null=True)
    company = models.CharField(max_length=50)
    flight_number=models.CharField(max_length=12)
    f_from = models.CharField(max_length=12)
    f_to = models.CharField(max_length=12)
    stand = models.CharField(max_length=3)
    carrier_reg =models.CharField(max_length=12)
    carrier_type =models.CharField(max_length=12)
    statues = models.CharField(max_length=50,choices=CHOICES)
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    observations = models.ManyToManyField(Notes)
    class Meta:
        """Meta definition for Report."""

        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering=['-date']

    def __str__(self):
        """Unicode representation of Report."""
        return str(self.date)
    
    def get_top_observations(self):
        top_observations = self.observations.annotate(count=models.Count('report')).order_by('-count')[:4]
        return top_observations
    @staticmethod
    def get_reports_within_date_range(start_date, end_date):
        reports = Report.objects.filter(date__range=[start_date, end_date])
        return reports

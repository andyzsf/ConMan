from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
# Used to update what's going on before / during / after the conference.
# could be used to update social networks too

class Update(models.Model):

    name = models.CharField(max_length=150, db_index=True)
    description = models.TextField(max_length=1000,blank=True,null=True)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)
    author = models.ForeignKey(User)
    
    def save(self):
        if not self.id:
            self.created = datetime.date.today()
        self.updated = datetime.datetime.today()
        super(Update, self).save()


    def __unicode__(self):
        return self.name


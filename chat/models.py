from djongo import models


class UserTrials(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    ends = models.DateTimeField()
    starts = models.DateTimeField()
    postedBy = models.CharField()
    isReminderset = models.BooleanField()

    class Meta:
        db_table = 'userTrials'
        app_label = 'main'

    def __str__(self):
        return self.name
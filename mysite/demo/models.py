from django.db import models

class TBRsensorData(models.Model):
    temp = models.DecimalField(max_digits=10, decimal_places=4)
    timestamp = models.IntegerField()
    noise = models.IntegerField()
    noiseLP = models.IntegerField()
    freq = models.IntegerField()
    #devID = 
class tagDetection(models.Model):
    timestamp = models.IntegerField()
    codeID = models.IntegerField()
    codeData = models.IntegerField()
    snr = models.IntegerField()
    millisec = models.IntegerField()
    #devID
    #tagID

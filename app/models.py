from djongo import models


class ExecutiveID(models.Model):
    bioguide = models.CharField(max_length=10)
    govtrack = models.IntegerField()
    icpsr_prez = models.IntegerField()

    class Meta:
        abstract = True  # So it doesn't create its own collection


class ExecutiveName(models.Model):
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)

    class Meta:
        abstract = True


class ExecutiveBio(models.Model):
    birthday = models.DateField()
    gender = models.CharField(max_length=1)  # M or F

    class Meta:
        abstract = True


class Term(models.Model):
    type = models.CharField(max_length=50)
    start = models.DateField()
    end = models.DateField()
    party = models.CharField(max_length=100)
    how = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Executive(models.Model):
    _id = models.ObjectIdField()
    id = models.EmbeddedField(model_container=ExecutiveID)
    name = models.EmbeddedField(model_container=ExecutiveName)
    bio = models.EmbeddedField(model_container=ExecutiveBio)
    terms = models.ArrayField(model_container=Term)

    class Meta:
        db_table = 'executives'

    def __str__(self):
        return f"{self.name['first']} {self.name['last']} ({self.id['govtrack']})"

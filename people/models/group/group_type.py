from django.db import models

class GroupType(models.Model):
    """
    Represents a Type of a Group in the system
    Example: Fellow, Staff
    """
    grouptype_id = models.AutoField(primary_key=True)           #: ID
    grouptype_name = models.CharField('Name', max_length=200)   #: Name

    class Meta:
        ordering = ['grouptype_name',]
        verbose_name = "Group type"
        verbose_name_plural = "Group - Types"

    def __str__(self):
        return self.grouptype_name




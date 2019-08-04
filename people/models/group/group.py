from django.db import models

from .group_queryset import GroupQuerySet

class Group(models.Model):
    """
    Represents a Group in the system
    Example: Fly Facillities, Lima
    """

    group_id = models.AutoField(primary_key=True)                   #: ID
    grouptype = models.ForeignKey('GroupType', verbose_name = 'Type', on_delete=models.CASCADE) #: Fk to the Group Type Table. e.g. staff
    group_name = models.CharField('Name', max_length=200)           #: Name
    group_subject = models.CharField('Subject', max_length=200)     #: Subject of a group
    group_web = models.URLField( verbose_name = 'Web site', blank=True, null=True)         #: URL to the Group Web site if exists
    group_people = models.ImageField('People',upload_to="uploads/group/group_people", blank=True, null=True)    #: Group People Image file to upload Button
    group_img = models.ImageField('Thumbnail',upload_to="uploads/group/group_img", blank=True, null=True)       #: Group Image file to be upload Button and a Thumbnail URL of the image
    group_desc = models.TextField('Description', default='', blank=True, null=True)                             #: Description of the Group
    members = models.ManyToManyField('Person', verbose_name = 'Members',through='GroupMember')                    #: Persons belong to that Group (Connection to the Person Table)
    person = models.ForeignKey('Person', related_name = 'Head', verbose_name = 'Head', blank=True, null=True, on_delete=models.CASCADE)     #: The head of that Group is a Fk to the Person Table
    groupdjango = models.ForeignKey('Group', blank=True, null=True, verbose_name='Groups in Django', related_name = 'group_django', on_delete=models.CASCADE)

    objects = GroupQuerySet.as_manager()

    class Meta:
        ordering = ['group_name',]
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.group_name

    @staticmethod
    def autocomplete_search_fields():
        return ("group_name__icontains",)


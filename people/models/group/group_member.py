from django.db import models

from .group_member_queryset import GroupMemberQuerySet

class GroupMember(models.Model):
    """
    Represents a Person wich is a Member of that Group
    """

    person   = models.ForeignKey('Person', on_delete=models.CASCADE)  #: Fk to the Person table
    group    = models.ForeignKey('Group', on_delete=models.CASCADE)    #: Fk to the Group table
    position = models.ForeignKey('Position', verbose_name = 'Category', blank=True, null=True, on_delete=models.CASCADE) #: Fk to the member category of that Person in the Group

    date_joined = models.DateField('Joined', null=True, blank=True)
    date_left   = models.DateField('Left', null=True, blank=True)

    position = models.ForeignKey(
        to='Position',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    objects = GroupMemberQuerySet.as_manager()

    def __str__(self):
        position = self.membercategory or self.person.position
        return f'{self.person.name} is a {position} in {self.group}'

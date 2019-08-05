from confapp import conf
from permissions.models import Permission
from people.models import Person
from django.contrib.contenttypes.models import ContentType
from pyforms_web.widgets.django import ModelAdminWidget
from django.conf import settings
from pyforms.controls import ControlCheckBox

from .people_form import PeopleFormWidget

from PIL import Image
from sorl.thumbnail import delete

from confapp import conf

from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.models import Group as AuthGroup

from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget
from pyforms.basewidget import segment
from pyforms.basewidget import no_columns
from pyforms.controls import ControlImg
from pyforms.controls import ControlButton

from people.models import InstitutionAffiliation
from people.models import Person
from people.models import GroupMembership

from .privateinfo import PrivateInfoFormWidget
from ..proposals import ContractProposalsListWidget
from ..contracts import ContractsListWidget

from humanresources.models import AcademicCareer

class AcademicCareerInline(ModelAdminWidget):
    MODEL = AcademicCareer

    LIST_DISPLAY = ['institution', 'degree', 'field_of_study', 'graduation_year']

    FIELDSETS = [
        ('institution', 'degree', 'field_of_study', 'graduation_year')
    ]


class InstitutionAffiliationInline(ModelAdminWidget):
    MODEL = InstitutionAffiliation
    TITLE = 'Affiliation'

    LIST_DISPLAY = ['institution', 'date_joined', 'date_left']

    FIELDSETS = [
        ('institution', 'date_joined', 'date_left')
    ]


class ResearchGroupsInline(ModelAdminWidget):
    MODEL = GroupMembership
    TITLE = 'Research Groups'

    LIST_DISPLAY = ['group', 'position', 'date_joined', 'date_left', 'membercategory']

    FIELDSETS = [
        ('group', 'position', 'date_joined', 'date_left', 'membercategory')
    ]

class PeopleListWidget(ModelAdminWidget):
    """
    """
    UID   = 'hr-people'
    TITLE = 'Human Resources'

    MODEL = Person

    LIST_ROWS_PER_PAGE = 40

    LIST_DISPLAY = (
        'thumbnail_80x80',
        'full_name',
        'person_email',
        'person_active',
    )

    SEARCH_FIELDS = (
        'full_name__icontains',
        'person_email__icontains',
        'person_personalemail__icontains'
    )

    EDITFORM_CLASS = PeopleFormWidget

    EXPORT_CSV = True
    EXPORT_CSV_COLUMNS = [
        # NOTE: These specific columns were asked by Teresa for a report
        'full_name',
        'person_email',
        'has_active_contract',
        'get_groups',
    ]

    # Orquestra Configuration
    # =========================================================================

    LAYOUT_POSITION = conf.ORQUESTRA_HOME_FULL

    USE_DETAILS_TO_EDIT = False

    ORQUESTRA_MENU = 'left'
    ORQUESTRA_MENU_ICON = 'users'
    ORQUESTRA_MENU_ORDER = 1

    FIELDSETS = [
        'h3:PERSONAL INFORMATION',
        (
            segment(
                'full_name',
                ('person_first', 'person_last'),
                ('person_gender', 'person_birthday'),
                ('degree', 'position'),
                ('person_cv', ' '),
                'person_bio',
                field_css='fourteen wide',
            ),
            segment(
                '_img',
                '_rotimg_btn',
                'person_img',
                field_style='max-width:330px;'
            ),
        ),
        'h3:EDUCATION',
        segment('AcademicCareerInline'),
        'h3:CONTACT INFORMATION',
        segment(
            ('person_email', 'person_personalemail'),
            ('person_mobile', 'person_phoneext'),
            'person_emergencycontact',
            css='secondary'
        ),
        'h3:INSTITUTIONAL INFORMATION',
        segment(
            'InstitutionAffiliationInline',
            ('person_cardnum', 'person_room'),
            css='secondary'
        ),
    ]

    READ_ONLY = ['full_name', 'djangouser', 'person_email', 'person_cardnum']

    INLINES = [
        AcademicCareerInline,
        InstitutionAffiliationInline,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def has_permissions(cls, user):
        from .people_list import PeopleListWidget
        return PeopleListWidget.has_permissions(user)

    @property
    def title(self):
        obj = self.model_object
        if obj is None:
            return ModelFormWidget.title.fget(self)
        else:
            return "Member: {0}".format(obj.name)

    @title.setter
    def title(self, value):
        ModelFormWidget.title.fset(self, value)



    def get_queryset(self, request, qs):

        if self._active_filter.value:
            qs = qs.active()

        if self._nocontract_filter.value:
            qs = qs.noactivecontract()

        if self._noproposal_filter.value:
            qs = qs.noactiveproposal()

        return qs

    def get_toolbar_buttons(self, has_add_permission=False):
        return (
            '_add_btn' if has_add_permission else None,
            '_active_filter',
            '_nocontract_filter',
            '_noproposal_filter',
        )

    def __check_data_integraty(self):
        # FIXME needs update to show useful warnings
        return

        nostartdate = Person.objects.nostartdate()
        if nostartdate.exists():
            self.warning(
                ' <b>|</b> '.join( map(str, nostartdate) ),
                title='People without *joined date* set!')

        noenddate = Person.objects.filter(person_active=False).nostartdate()
        if noenddate.exists():
            self.warning(
                ' <b>|</b> '.join( map(str, noenddate) ),
                title='People without *end date* set!')



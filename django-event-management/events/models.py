from django.db import models
from django.urls import reverse
from mapbox_location_field.models import LocationField
from ckeditor_uploader.fields import RichTextUploadingField

from django.contrib.auth.models import ( 
    BaseUserManager, AbstractBaseUser
)


class EmployeeAccountManager(BaseUserManager):
    def create_user(self, empcode, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not empcode:
            raise ValueError('Users must have an employee code')

        user = self.model(
            empcode=empcode,
        )

        user.set_password(password)
        user.save(using=self._db)
        user.is_admin = True
        return user

    def create_superuser(self, empcode, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            empcode=empcode,
            password=password,
        )
        user.is_admin = True
        #user.is_staff = False
        user.save(using=self._db)
        return user


class EventCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=6, unique=True)
    image = models.ImageField(upload_to='event_category/')
    priority = models.IntegerField(unique=True)
    created_user = models.ForeignKey('events.Employee', on_delete=models.CASCADE, related_name='created_user')
    updated_user = models.ForeignKey('events.Employee', on_delete=models.CASCADE, related_name='updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    status_choice = (
        ('disabled', 'Disabled'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('blocked', 'Blocked'),
        ('completed', 'Completed'),
    )
    status = models.CharField(choices=status_choice, max_length=10)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('event-category-list')

class JobCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    uid = models.PositiveIntegerField(unique=True)
    description = RichTextUploadingField()
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    select_scheduled_status = (
        ('yet to scheduled', 'Yet to Scheduled'),
        ('scheduled', 'Scheduled')
    )
    scheduled_status = models.CharField(max_length=25, choices=select_scheduled_status)
    venue = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = LocationField()
    points = models.PositiveIntegerField()
    maximum_attende = models.PositiveIntegerField()
    created_user = models.ForeignKey('events.Employee', on_delete=models.CASCADE, blank=True, null=True, related_name='event_created_user')
    updated_user = models.ForeignKey('events.Employee', on_delete=models.CASCADE, blank=True, null=True, related_name='event_updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    status_choice = (
        ('disabled', 'Disabled'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('time out', 'Time Out'),
        ('completed', 'Completed'),
        ('cancel', 'Cancel'),
    )
    status = models.CharField(choices=status_choice, max_length=10)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('event-list')
    
    def created_updated(model, request):
        obj = model.objects.latest('pk')
        if obj.created_by is None:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()

class EventImage(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_image/')


class EventAgenda(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=120)
    speaker_name = models.CharField(max_length=120)
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue_name = models.CharField(max_length=255)


class EventJobCategoryLinking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    status_choice = (
        ('disabled', 'Disabled'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('blocked', 'Blocked'),
        ('completed', 'Completed'),
    )
    status = models.CharField(choices=status_choice, max_length=10)

    def __str__(self):
        return str(self.event)


class EventMember(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey('events.Employee', on_delete=models.CASCADE)
    attend_status_choice = (
        ('waiting', 'Waiting'),
        ('attending', 'Attending'),
        ('completed', 'Completed'),
        ('absent', 'Absent'),
        ('cancelled', 'Cancelled'),
    )
    attend_status = models.CharField(choices=attend_status_choice, max_length=10)
    created_user = models.ForeignKey('events.Employee', on_delete=models.CASCADE, related_name='eventmember_created_user')
    updated_user = models.ForeignKey('events.Employee', on_delete=models.CASCADE, related_name='eventmember_updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    status_choice = (
        ('disabled', 'Disabled'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('blocked', 'Blocked'),
        ('completed', 'Completed'),
    )
    status = models.CharField(choices=status_choice, max_length=10)


    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse('join-event-list')


class EventUserWishList(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey('events.Employee', on_delete=models.CASCADE)
    created_user = models.ForeignKey('events.Employee', on_delete=models.CASCADE, related_name='eventwishlist_created_user')
    updated_user = models.ForeignKey('events.Employee', on_delete=models.CASCADE, related_name='eventwishlist_updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    status_choice = (
        ('disabled', 'Disabled'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('blocked', 'Blocked'),
        ('completed', 'Completed'),
    )
    status = models.CharField(choices=status_choice, max_length=10)


    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return str(self.event)
    
    def get_absolute_url(self):
        return reverse('event-wish-list')


class UserCoin(models.Model):
    user = models.OneToOneField('events.Employee', on_delete=models.CASCADE)
    CHOICE_GAIN_TYPE = (
        ('event', 'Event'),
        ('others', 'Others'),
    )
    gain_type = models.CharField(max_length=6, choices=CHOICE_GAIN_TYPE)
    gain_coin = models.PositiveIntegerField()
    created_user = models.ForeignKey('events.Employee', on_delete=models.CASCADE, related_name='usercoin_created_user')
    updated_user = models.ForeignKey('events.Employee', on_delete=models.CASCADE, related_name='usercoin_updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    status_choice = (
        ('disabled', 'Disabled'),
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        ('blocked', 'Blocked'),
        ('completed', 'Completed'),
    )
    status = models.CharField(choices=status_choice, max_length=10)

    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse('user-mark')

# class Employee(models.Model):
class Employee(AbstractBaseUser):
    empcode = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    second_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email_id = models.CharField(unique=True, max_length=30, blank=True, null=True)
    mobileno = models.CharField(max_length=15, blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=120, blank=True, null=True)
    is_admin = models.BooleanField(default=False)


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    objects = EmployeeAccountManager()
    USERNAME_FIELD = 'empcode'
	
    def __str__(self):
        return str(self.first_name)

    class Meta:
        #managed = False #if it is set to False then table will not be created
        db_table = 'employee'
        ordering = ('first_name',)



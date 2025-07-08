from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Designation(models.Model):
    designationname = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.designationname

class User(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phoneno = models.CharField(max_length=15)  # Assuming a max length for phone number
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.pk:  # Only hash the password when creating a new user
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        # Check the provided password against the stored hashed password
        return check_password(raw_password, self.password)
    
 ###################### starting working of designation############


class Group(models.Model):
    SHIFT_CHOICES = [
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    ]
    groupname = models.CharField(max_length=100)
    members_names = models.CharField(max_length=500, blank=True)  # Comma-separated names
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)

    def __Str__(self):
        return self.groupname
    
    def set_members(self, names_list):
        """Method to set members from a list of names."""
        self.members_names = ', '.join(names_list)
        self.save()

    def get_members(self):
        """Method to retrieve members as a list."""
        return self.members_names.split(', ') if self.members_names else []
    

class Marks(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='marks')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='marks')
    project_marks = models.IntegerField()
    poster_marks = models.IntegerField()
from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class MembershipManager(models.Manager):
    def validate_registration(self, postData):
        # Original validation logic applies
        # Name must be present and at least 2 characters long
        # rate must be present
        print(postData)
        # 1. create errors dictionary
        errors = {}
        # 2. validate post information
        if len(postData['name']) == 0:
            errors['name'] = "Name must be present"
        elif len(postData['name'])<2:
            errors['name'] = "Name must be at least 2 characters long"

        if len(postData['alias']) == 0:
            errors['alias'] = "alias must be present"
        elif len(postData['alias'])<2:
            errors['alias'] = "alias must be at least 2 characters long"

        # THIS IS NEW FOR REGISTERING
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be of a proper format"
        else:
            users_with_same_email = self.filter(email=postData['email'])
            if len(users_with_same_email)>0:
                errors['email'] = 'Email is already taken'
        if postData['password'] != postData['password_confirm']:
            errors['password'] = 'Password fields must match'
        if len(postData['password'])<8:
            errors['password'] = 'Password must be at least 8 characters long'
        
        print(errors)
        # 3. Check if errors exist, if they do, add them to messages
        if len(errors):
            result = {
                'errors': errors
            }
        else:
            # THIS IS ALSO NEW, WE NEED TO ADD BCRYPT TO HASH PW
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            member = self.create(
                name = postData['name'], 
                alias = postData['alias'],
                email = postData['email'], 
                password=hashed_pw
            )
            result = {
                'the_user' : member
            }
            return result
    def login(self, postData):
        if not EMAIL_REGEX.match(postData['email']):
            return {'error' : 'Invalid Format'}

        user = Membership.objects.get(email = postData['email'])
        if not user:
            return {'error' : 'user does not exist.'}
        else:
            stored_hash = user.password
            input_hash = bcrypt.hashpw(postData['password'].encode(), stored_hash.encode())
            if not input_hash == stored_hash:
                return {'error' : 'Wrong password'}
            else:
                print("Success!")
                return {'the_user' : user } 
        

            

class Membership(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    friends = models.ManyToManyField('self')
    objects = MembershipManager()

    def __unicode__(self):
        return "id: " + str(self.id) + ", alias: " + self.alias


class Task(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    created_by = models.ForeignKey(Membership, related_name='items', null=True)
    claimed_by = models.ManyToManyField(Membership, related_name='claimed', blank=True)
    created_on = models.DateField(auto_now_add = True)
    updated_on = models.DateField(auto_now = True)


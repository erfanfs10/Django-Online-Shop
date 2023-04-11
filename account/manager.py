from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
       
        user = self.model(email=email, **extra_fields)  
        user.set_password(password)  
        user.save()  
        return user  
    
    def create_superuser(self, email, password, **extra_fields):  
        """  
        Create and save a SuperUser with the given email and password.  
        """  
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True)  
        extra_fields.setdefault('is_active', True)  
  
        if extra_fields.get('is_staff') is not True:  
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:  
            raise ValueError('Superuser must have is_superuser=True.') 
        return self.create_user(email, password, **extra_fields)  
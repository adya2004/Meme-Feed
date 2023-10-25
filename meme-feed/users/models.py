from django.db import models
from PIL import Image
from django.contrib.auth.models import User

class profile(models.Model):
    # Link a profile to a user using a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Store the user's profile picture using the ImageField
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        # A human-readable representation of the profile
        return f"{self.user.username} Profile"
    
    def save(self):
        # Override the save method to resize the profile image

        # Call the original save method to save the image
        super().save()

        # Open the saved image
        img = Image.open(self.image.path)
        
        # Resize the image if it's larger than 300x300 pixels
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            
            # Save the resized image back to the same path
            img.save(self.image.path)

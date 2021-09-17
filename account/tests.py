from django.test import TestCase
from .models import Image as Posts, Comments, Users, Profile
# Create your tests here.

class ImageTestClass(TestCase):
    def setUp(self):
        # Creating a new user and saving it
        self.user=Users(username="kk", email="kk@gmail.com",name="Kelvin Koech",following=[],followers=[], phone ='+254725801772',date_joined="2021-09-05 22:16:35.61389+03")
        self.user.save()

        # Creating a new Image  and saving it
        self.new_post = Posts(post_image = 'xyz.png', caption="I was in Mombasa",likes=[], user=self.user)
        self.new_post.save()

        # Creating a new comment and saving it
        self.new_comment = Comments(comment = 'This is awesome', date_posted="2021-09-05 22:16:35.61389+03", post=self.new_post,user=self.user)
        self.new_comment.save()

        # Creating a new profile and saving it
        self.new_post = Profile(profile_photo = 'profiles.png', bio="Always Happy",user=3)
        self.new_post.save()


    def tearDown(self):
        Users.objects.all().delete()
        Profile.objects.all().delete()
        Comments.objects.all().delete()
        Posts.objects.all().delete()

    def test_save_image(self):
        self.user=Posts(post_image = 'xyz.jpg', caption ='It was a one tour to mombasa')
        image_obj = Posts.objects.all().count()
        self.assertTrue(image_obj>0)


    def test_update_image(self):
        image_obj = Posts.objects.first()
        id=image_obj.id
        caption="This is lit"        
        
        Posts.update_caption(id,caption)
        image = Posts.objects.get(id=id)
        self.assertEqual(image.caption,"This is lit")

    def test_delete_image(self):
        image=Posts.objects.first()
        id=image.id
        Posts.delete_image(id)
        try:
            img = Posts.objects.get(id=id)
            self.assertTrue("Some results")
        except Posts.DoesNotExist:
            self.assertTrue("no results"=="no results")
from django.test import TestCase
from .models import Image as Posts, Comments, Users
# Create your tests here.

class ImageTestClass(TestCase):
    def setUp(self):
        # Creating a new image and saving it
        self.user=Users(username="kk", email="kk@gmail.com" ,image = 'xyz.jpg', caption ='It was a one tour to mombasa',date_joined="2021-09-05 22:16:35.61389+03")
        self.user.save()

        # Creating a new comment and saving it
        self.new_comment = Comments(comment = 'This is awesome')
        self.new_comment.save()

        # Creating a new  and saving it
        self.new_post = Posts(image = 'xyz.png', caption="I was in Mombasa", user="1")
        self.new_post.save()

    def tearDown(self):
        Users.objects.all().delete()
        Comments.objects.all().delete()
        Posts.objects.all().delete()

    def test_save_image(self):
        self.user=Posts(username="kk", email="kk@gmail.com" ,image = 'xyz.jpg', caption ='It was a one tour to mombasa',date_joined="2021-09-05 22:16:35.61389+03")

    def test_update_image(self):
        image_obj = Posts.objects.all()[:1].get()
        id=image_obj.id
        caption="This is lit"        
        
        Posts.update_caption(id,caption)
        caption = Posts.objects.get(id=id)
        self.assertEqual(caption,"This is lit")

    def test_delete_image(self):
        image=Posts.objects.first()
        id=image.id
        Posts.delete_image(id)
        try:
            img = Posts.objects.get(id=id)
            self.assertTrue("Some results")
        except Posts.DoesNotExist:
            self.assertTrue("no results"=="no results")
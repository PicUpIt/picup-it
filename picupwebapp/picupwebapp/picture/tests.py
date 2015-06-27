from django.test import TestCase
from django.test import Client

from picupwebapp.picture.models  import Picture, Gallery
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.conf import settings
from os import path

class PictureTestCase(TestCase):

    API_KEY = "some_api_key"
    USERNAME = "test_user"
    PASSWORD = "password"
    EMAIL = 'test@example.com'
    FILENAME = path.join(settings.PROJECT_DIR, 'fixtures', "test00.png")

    def setUp(self):
        test_user = User(username=self.USERNAME)
        test_user.id = 2
        test_user.set_password(self.PASSWORD)
        test_user.email = self.EMAIL
        test_user.save()

    def test_login_page(self):
        """Test if login page displays correctly.
        """

        c = Client()
        response = c.get('/signin/')
        self.assertContains(response,'OpenID')
        self.assertContains(response,'Mozilla Persona')
        self.assertContains(response,'Github')

    def test_create_user(self):
        """Test if there is no problems during user creation.
        
        Note
        ----
        This test just verify if nothing is broken internally due to
        the dependencies.
        """
        u = User(username="test")
        u.save()
        self.assertEqual(u.id>0,True)

    def test_login_user(self):
        """Test if user can login with pass.
        """
        c = Client()
        self.assertEqual(c.login(username=self.USERNAME, 
                                 password=self.PASSWORD), True)

    def test_remove_user(self):
        """Test user's remove.
        """
        c = Client()
        c.login(username=self.USERNAME, password=self.PASSWORD)        
        response = c.post('/accounts/remove/', {'test':'test'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(c.login(username=self.USERNAME, 
                                 password=self.PASSWORD), False)    
        self.assertEqual(User.objects.filter(username=self.USERNAME).count(),0)
        
    def test_upload(self):
        """Test if picture is being uploaded and belongs to correct user.
        """
        c = Client()
        c.login(username=self.USERNAME, password=self.PASSWORD)
        with open(path.join(settings.PROJECT_DIR, 
                            'fixtures', "test00.png")) as fp:
            c.post('/picup', {'picture': fp})
        pictures = Picture.objects.all()
        picture = pictures[0]
        user = User.objects.get(username=self.USERNAME)
        self.assertEqual(picture.user_id, user.id)        

    def test_upload_and_view(self):
        """Test picture upload and view.
        """
        c = Client()
        c.login(username=self.USERNAME, password=self.PASSWORD)
        with open(path.join(settings.PROJECT_DIR, 
                            'fixtures', "test00.png")) as fp:
            c.post('/picup', {'picture': fp})
        pictures = Picture.objects.all()
        picture = pictures[0]
        response = c.get('/p/%s/' % (picture.id))
        self.assertEqual(response.status_code, 200)

    def test_create_gallery(self):
        """Test create gallery via internal url call.
        """
        c = Client()
        c.login(username=self.USERNAME, password=self.PASSWORD)
        galleries = Gallery.objects.all()
        self.assertEqual(galleries.count(), 0)
        
        response = c.post(reverse('intcall_gallery'),
                               {'gallery_title':'Test title',
                                'create':True})
        galleries = Gallery.objects.all()
        self.assertEqual(galleries.count(), 1)
        
    def test_create_and_view_gallery(self):
        """Test create and view gallery via internal url call.
        """        
        c = Client()
        c.login(username=self.USERNAME, password=self.PASSWORD)
        pictures = Picture.objects.all()
        response = c.post(reverse('intcall_gallery'),
                          {'gallery_title':'Test title',
                           'create':True})
        galleries = Gallery.objects.all()
        self.assertEqual(galleries.count(), 1)
        with open(path.join(settings.PROJECT_DIR,
                        'fixtures', "test00.png")) as fp:   
                c.post('/picup', {'picture': fp, 'gallery_id':1})
        response = c.get('/u/2/1/')
        user = User.objects.get(username=self.USERNAME)
        pictures = Picture.objects.all()
        picture = pictures[0]        
        self.assertEqual(response.status_code,200)
        
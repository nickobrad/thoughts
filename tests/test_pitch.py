import unittest
from app.models import User, Pitch
from app import db

class PitchTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Review class
    '''
    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()
 
    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.user_James = User(username = 'James',secured_password = 'potato', email = 'james@ms.com')
        self.new_pitch = Pitch(id = 20, pitch="This is a good day", categoryOfPitch=1, user= self.user_James.username, date_posted = "14/11/2020", upvote = 0, downvote = 0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.id,20)
        self.assertEquals(self.new_pitch.pitch,"This is a good day")
        self.assertEquals(self.new_pitch.categoryOfPitch,1)
        self.assertEquals(self.new_pitch.user,self.user_James.username)

    def test_save_pitch(self):
        db.session.add(self.user_James)
        db.session.commit()
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all()) == 1)

    def test_get_pitch_by_id(self):
        db.session.add(self.user_James)
        db.session.commit()
        self.new_pitch.save_pitch()
        got_pitch = Pitch.pitch_by_id(20)
        self.assertTrue(got_pitch is not None)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Pitch))


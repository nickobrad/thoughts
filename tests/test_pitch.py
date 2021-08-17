import unittest
from app.models import User, Pitch, PitchComment
from app import db

class ReviewTest(unittest.TestCase):
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
        self.new_pitch = Pitch(id = 200, pitch="This is a good day",categoryOfPitch=1,user= self.user_James.username)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.pitch,"This is a good day")
        self.assertEquals(self.new_pitch.categoryOfPitch,1)
        self.assertEquals(self.new_pitch.user,self.user_James.username)

    def test_save_review(self):
        self.new_pitch.save_review()
        self.assertTrue(len(Pitch.query.all() > 0))

    def test_get_pitch_by_id(self):
        self.new_pitch.save_pitch()
        got_pitch = Pitch.all_pitches(200)
        self.assertTrue(len(got_pitch) == 1)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Pitch))

if __name__ == '__main__':
    unittest.main()

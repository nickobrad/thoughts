import unittest
from app.models import User, Pitch, PitchComment
from app import db

class PitchCommentTest(unittest.TestCase):
    
    def tearDown(self):
        PitchComment.query.delete()
        Pitch.query.delete()
        User.query.delete()
 
    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.user_James = User(username = 'James',secured_password = 'potato', email = 'james@ms.com')
        self.new_pitch = Pitch(id = 20, pitch="This is a good day", categoryOfPitch=1, user= self.user_James.username, date_posted = "14/11/2020", upvote = 0, downvote = 0)
        self.new_comment= PitchComment(id=1,pitch_id=20, comment="Very nice", user=self.user_James.username,date_posted="14/08/2020")

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.id,1)
        self.assertEquals(self.new_comment.pitch_id,20)
        self.assertEquals(self.new_comment.comment,"Very nice")
        self.assertEquals(self.new_comment.user,self.user_James.username)
        self.assertEquals(self.new_comment.date_posted,"14/08/2020")

    def test_save_comment(self):
        db.session.add_all([self.user_James, self.new_pitch, self.new_comment])
        db.session.commit()
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all()) == 1)

    # def test_delete_comment(self):
    #     db.session.add_all([self.user_James, self.new_pitch, self.new_comment])
    #     db.session.commit()
    #     self.new_pitch.save_pitch()
    #     got_pitch = PitchComment.all_comments(self.user_James.username)
    #     self.assertTrue(got_pitch is not None)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Pitch))



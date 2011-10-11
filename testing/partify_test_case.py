import os
import random
import tempfile

from testify import *

from partify import app
# TODO: Figure out these imports and how to remove duplication between this and run.py
from partify import player, queue, track, user
from partify.database import db_session, init_test_db
from partify.models import User

class PartifyTestCase(TestCase):
	@class_setup
	def _prepare(self):
		self.db_fd = tempfile.mkstemp()
		app.config['DATABASE'] = "sqlite:///%s" % self.db_fd[1]
		app.config['TESTING'] = True
		self.app = app.test_client()
		init_test_db()

	@class_teardown
	def _cleanup(self):
		os.close(self.db_fd[0])
		#os.unlink(app.config['DATABASE'])

	def create_test_user(self):
		"""Creates a test user with the same username as password."""
		r = random.Random()
		uid = r.randint(0,10000000000000)
		user = User(name='test_user_%d' % uid,
			username='%d' % uid,
			password='%d' % uid)
		return user
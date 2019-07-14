from datetime import datetime
from beforetheproduct import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    headline = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    ideas = db.relationship('Idea', backref='user', lazy=True, cascade='all,delete')
    yessed = db.relationship('IdeaYes', foreign_keys='IdeaYes.user_id', backref='user', lazy='dynamic', cascade='all,delete')
    noed = db.relationship('IdeaNo', foreign_keys='IdeaNo.user_id', backref='user', lazy='dynamic', cascade='all,delete')
    upvoted = db.relationship('Upvote', foreign_keys='Upvote.user_id', backref='user', lazy='dynamic', cascade='all,delete')
    commented = db.relationship('IdeaComment', foreign_keys='IdeaComment.user_id', backref='user', lazy='dynamic', cascade='all,delete')


    # Idea Yes functions

    def yes_idea(self, idea):
        if not self.has_yessed_idea(idea):
            yes = IdeaYes(user_id=self.id, idea_id=idea.id)
            db.session.add(yes)

    def unyes_idea(self, idea):
        if self.has_yessed_idea(idea):
            IdeaYes.query.filter_by(
                user_id=self.id,
                idea_id=idea.id).delete()

    def has_yessed_idea(self, idea):
        return IdeaYes.query.filter(
            IdeaYes.user_id == self.id,
            IdeaYes.idea_id == idea.id).count() > 0


    # Idea No functions

    def no_idea(self, idea):
        if not self.has_noed_idea(idea):
            dislike = IdeaNo(user_id=self.id, idea_id=idea.id)
            db.session.add(dislike)

    def unno_idea(self, idea):
        if self.has_noed_idea(idea):
            IdeaNo.query.filter_by(
                user_id=self.id,
                idea_id=idea.id).delete()

    def has_noed_idea(self, idea):
        return IdeaNo.query.filter(
            IdeaNo.user_id == self.id,
            IdeaNo.idea_id == idea.id).count() > 0


    # Idea Upvote functions

    def upvote(self, idea):
        if not self.has_upvoted(idea):
            upvote = Upvote(user_id=self.id, idea_id=idea.id)
            db.session.add(upvote)

    def unupvote(self, idea):
        if self.has_upvoted(idea):
            Upvote.query.filter_by(
                user_id=self.id,
                idea_id=idea.id).delete()

    def has_upvoted(self, idea):
        return Upvote.query.filter(
            Upvote.user_id == self.id,
            Upvote.idea_id == idea.id).count() > 0


class IdeaYes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'))

class IdeaNo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'))

class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'))

class IdeaComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'))

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(20), nullable=True)
    main_image = db.Column(db.String(20), nullable=True)
    view_count = db.Column(db.Integer, nullable=True, default=0)
    topic = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    yesses = db.relationship('IdeaYes', backref='idea', lazy='dynamic', cascade='all,delete')
    noes = db.relationship('IdeaNo', backref='idea', lazy='dynamic', cascade='all,delete')
    upvotes = db.relationship('Upvote', backref='idea', lazy='dynamic', cascade='all,delete')
    comments = db.relationship('IdeaComment', backref='idea', lazy='dynamic', cascade='all,delete')

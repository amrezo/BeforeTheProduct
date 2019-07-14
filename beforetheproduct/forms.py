from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from beforetheproduct.models import User

topics=[

('Productivity','Productivity'),
('Developer Tools','Developer Tools'),
('Tech','Tech'),
('Artificial Intelligence','Artificial Intelligence'),
('User Experience', 'User Experience'),
('Marketing', 'Marketing'),
('Wearables', 'Wearables'),
('Internet of Things', 'Internet of Things'),
('Design Tools', 'Design Tools'),
('Home', 'Home'),
('Analytics', 'Analytics'),
('Photography', 'Photography'),
('Growth Hacking', 'Growth Hacking'),
('Books', 'Books'),
('Bots', 'Bots'),
('iPhone', 'iPhone'),
('Mac', 'Mac'),
('APIs', 'APIs'),
('Web App', 'Web App'),
('Games', 'Games'),
('Slack', 'Slack'),
('Task Management', 'Task Management'),
('Social Media Tools', 'Social Media Tools'),
('Prototyping', 'Prototyping'),
('Health and Fitness', 'Health and Fitness'),
('Education', 'Education'),
('Open Source', 'Open Source'),
('BeforeTheProduct', 'BeforeTheProduct'),
('Writing Tools', 'Writing Tools'),
('Messaging', 'Messaging'),
('Android', 'Android'),
('Touch Bar Apps', 'Touch Bar Apps'),
('Facebook', 'Facebook'),
('Venture Capital', 'Venture Capital'),
('Chrome Extensions', 'Chrome Extensions'),
('Music', 'Music'),
('Virtual Reality', 'Virtual Reality'),
('Augmented Reality', 'Augmented Reality'),
('Netflix', 'Netflix'),
('GitHub', 'GitHub'),
('News', 'News'),
('Email', 'Email'),
('Travel', 'Travel'),
('E-Commerce', 'E-Commerce'),
('Branding', 'Branding'),
('Calendar and Scheduling', 'Calendar and Scheduling'),
('Nomad Lifestyle', 'Nomad Lifestyle'),
('Fintech', 'Fintech'),
('LinkedIn', 'LinkedIn'),
('Coffee', 'Coffee'),
('SEO Tools', 'SEO Tools'),
('GIFs', 'GIFs'),
('Freelance', 'Freelance'),
('Software Engineering', 'Software Engineering'),
('Crypto', 'Crypto'),
('Email Marketing', 'Email Marketing'),
('iMessage Apps', 'iMessage Apps'),
('Drones', 'Drones'),
('Crowdfunding', 'Crowdfunding'),
('Twitter', 'Twitter'),
('Advertising', 'Advertising'),
('Spotify', 'Spotify'),
('SaaS', 'SaaS'),
('Snapchat', 'Snapchat'),
('Investing', 'Investing'),
('Instagram', 'Instagram'),
('Sketch', 'Sketch'),
('Startup Books', 'Startup Books'),
('A/B Testing', 'A/B Testing'),
('WordPress', 'WordPress'),
('Typography', 'Typography'),
('Medium', 'Medium'),
('Design Books', 'Design Books'),
('Text Editors', 'Text Editors'),
('Amazon', 'Amazon'),
('Google', 'Google'),
('Virtual Assistants', 'Virtual Assistants'),
('reddit', 'reddit'),
('YouTube', 'YouTube'),
('Biohacking', 'Biohacking'),
('Sales', 'Sales'),
('Maps', 'Maps'),
('Learn a Language', 'Learn a Language'),
('Hiring and Recruiting', 'Hiring and Recruiting'),
('Photoshop', 'Photoshop'),
('Mac Menu Bar Apps', 'Mac Menu Bar Apps'),
('Art', 'Art'),
('Movies', 'Movies'),
('Apple', 'Apple'),
('Meditation', 'Meditation'),
('Payment', 'Payment'),
('Time Tracking', 'Time Tracking'),
('Facebook Messenger', 'Facebook Messenger'),
('Email Newsletters', 'Email Newsletters'),
('Hardware', 'Hardware'),
('Funny', 'Funny'),
('Green Tech', 'Green Tech'),
('Fashion', 'Fashion'),
('Robots', 'Robots'),
('Windows', 'Windows'),
('Privacy', 'Privacy'),
('Emoji', 'Emoji'),
('Pokemon', 'Pokemon'),
('Wi-Fi', 'Wi-Fi'),
('Spreadsheets', 'Spreadsheets'),
('Alexa Skills', 'Alexa Skills'),
('Customer Communication', 'Customer Communication'),
('Icons', 'Icons'),
('Video Streaming', 'Video Streaming'),
('3D Printing', '3D Printing'),
('Space', 'Space'),
('Public Relations', 'Public Relations'),
('Cooking', 'Cooking'),
('Outdoors', 'Outdoors'),
('Airbnb', 'Airbnb'),
('Google Home', 'Google Home'),
('Dropbox', 'Dropbox'),
('iPad', 'iPad'),
('On-Demand', 'On-Demand'),
('Delivery', 'Delivery'),
('Linux', 'Linux'),
('Wallpaper', 'Wallpaper'),
('Note', 'Note'),
('Uber', 'Uber'),
('Beauty', 'Beauty'),
('Free Games', 'Free Games'),
('Backpacks', 'Backpacks'),
('Meetings', 'Meetings'),
('Sports', 'Sports'),
('Anonymous', 'Anonymous'),
('TV', 'TV'),
('Indie Games', 'Indie Games'),
('Apple Watch', 'Apple Watch'),
('Events', 'Events'),
('PC', 'PC'),
('SoundCloud', 'SoundCloud'),
('Kindle', 'Kindle'),
('Apple TV', 'Apple TV'),
('Transportation', 'Transportation'),
('Standing Desks', 'Standing Desks'),
('Board Games', 'Board Games'),
('Emulators', 'Emulators'),
('Couples', 'Couples'),
('Legal', 'Legal'),
('Telegram', 'Telegram'),
('Strategy Games', 'Strategy Games'),
('Dating', 'Dating'),
('Cars', 'Cars'),
('Dogs', 'Dogs'),
('Parenting', 'Parenting'),
('CSM Tools', 'CSM Tools'),
('Batteries', 'Batteries'),
('Oculus Rift', 'Oculus Rift'),
('Charity and Giving', 'Charity and Giving'),
('Ad Blockers', 'Ad Blockers'),
('Phone Cases', 'Phone Cases'),
('Science Books', 'Science Books'),
('Kids', 'Kids'),
('Pets', 'Pets'),
('Puzzle Games', 'Puzzle Games'),
('Safari Extensions', 'Safari Extensions'),
('Star Wars', 'Star Wars'),
('Gear VR', 'Gear VR'),
('Firefox Extensions', 'Firefox Extensions'),
('Politics', 'Politics'),
('Cats', 'Cats'),
('Squarespace', 'Squarespace'),
('Adventure Games', 'Adventure Games'),
('PS4', 'PS4'),
('Card Games', 'Card Games'),
('Retro Games', 'Retro Games'),
('Sneakers and Shoes', 'Sneakers and Shoes'),
('Comics and Graphic Novels', 'Comics and Graphic Novels'),
('Open World Games', 'Open World Games'),
('Moving and Storage', 'Moving and Storage'),
('Weather Apps', 'Weather Apps'),
('Biking', 'Biking'),
('Art Books', 'Art Books'),
('Action Games', 'Action Games'),
('Party', 'Party'),
('RPGs', 'RPGs'),
('Cooking Books', 'Cooking Books'),
('Sci-fi Games', 'Sci-fi Games'),
('Novels', 'Novels'),
('History Books', 'History Books'),
('Jewelry', 'Jewelry'),
('Crafting Games', 'Crafting Games'),
('ARKit', 'ARKit'),
('Simulation Games', 'Simulation Games'),
('Alarm Clocks', 'Alarm Clocks'),
('Xbox One', 'Xbox One'),
('DJing', 'DJing'),
('Word Games', 'Word Games'),
('Fantasy Games', 'Fantasy Games'),
('Fashion Books', 'Fashion Books'),
('Tabletop Games', 'Tabletop Games'),
('Custom iPhone Keyboards', 'Custom iPhone Keyboards'),
('Football', 'Football'),
('PlayStation VR', 'PlayStation VR'),
('Soccer', 'Soccer'),
('Funny Games', 'Funny Games'),
('Platformers', 'Platformers'),
('Yoga Books', 'Yoga Books'),
('Celebrities', 'Celebrities'),
('MMOs', 'MMOs'),
('Sports Games', 'Sports Games'),
('Basketball', 'Basketball'),
('Horror Games', 'Horror Games'),
('Driving Games', 'Driving Games'),
('Donald Trump', 'Donald Trump'),
('FPS', 'FPS'),
('Isometric Games', 'Isometric Games'),
('Historical Games', 'Historical Games'),
('Surfing', 'Surfing'),
('Swimming', 'Swimming'),
('Skateboarding','Skateboarding'),
('3DS','3DS'),
('Crime Books','Crime Books'),
('HTC Vive','HTC Vive'),
('Thriller Books','Thriller Books'),
('Fighting Games','Fighting Games'),
('Golf','Golf'),
('Horror Books','Horror Books'),
('Tennis','Tennis'),
('Tower Defense Games','Tower Defense Games'),
('Quantified Self','Quantified Self'),
('Zombie Games','Zombie Games'),
('Boxing','Boxing'),
('Baseball','Baseball'),
('Wii U','Wii U'),
('Vita','Vita'),
('Startup Lessons','Startup Lessons'),
('Side Projects','Side Projects'),
('Growth Hacks','Growth Hacks'),
('Medtech','Medtech'),
('Money','Money'),
('Blockstack','Blockstack'),
('Work in Progress','Work in Progress'),
('Other','Other')

]

class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    headline = StringField('Headline')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class IdeaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    link = StringField('Link (if available)')
    description = HiddenField('Description', validators=[DataRequired()])
    thumbnail_image = FileField('Thumbnail Image', validators=[FileAllowed(['jpg', 'png']), FileRequired()])
    main_image = FileField('Main Image - 800px by 500px optimal', validators=[FileAllowed(['jpg', 'png']), FileRequired()])
    topic = SelectField('Select relevant topic', choices=topics, validators=[DataRequired()])
    submit = SubmitField('Post')

class UpdateIdeaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    link = StringField('Link (if available)')
    description = HiddenField('Description', validators=[DataRequired()])
    thumbnail_image = FileField('Replace Thumbnail Image', validators=[FileAllowed(['jpg', 'png'])])
    main_image = FileField('Replace Main Image - 800px by 500px optimal', validators=[FileAllowed(['jpg', 'png'])])
    topic = SelectField('Select relevant topic', choices=topics, validators=[DataRequired()])
    submit = SubmitField('Update Post')


class CommentForm(FlaskForm):
    content = HiddenField('Your Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')

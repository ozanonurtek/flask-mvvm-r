import re
from project.models import User,Event, db
from flask_login import login_user, current_user
from flask import flash


class RegisterViewModel(object):

    def __init__(self, form, method):
        self.email = ""
        self.username = ""
        self.password = ""
        self.isAdmin = False
        self.error = ""
        self.register_success = False
        self.new_user = User
        self.form = form
        self.method = method

    def __checkUsername(self):
        if re.match("^((\w|_|-)+)$", self.username) is None:
            self.error += "'{} ' kullanıcı adı uygun değil.\n".format(self.username)
            return False
        return True

    def __checkPassword(self):
        if self.password == "":  # TODO: add a password control.
            self.error += "Şifren kullanılmaya uygun değil."
            return False
        return True

    def __checkEmail(self):
        if re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", self.email) is None:
            self.error += "'{}' mail adresi uygun değil.\n".format(self.email)
            return False
        return True

    def getError(self):
        return self.error

    def getRegisterSuccess(self):
        return self.register_success

    def getRegisteredUser(self):
        return self.new_user

    def checkValidation(self):
        if self.__checkEmail() and self.__checkUsername() and self.__checkPassword():
            # The username, password and email does not have dangerous characters. Check if it's being used.
            username_check = User.query.filter_by(username=self.username).first()
            email_check = User.query.filter_by(email=self.email).first()
            can_register = True

            if username_check:
                self.error += "'{}' kullanıcı adı zaten kullanımda.\n".format(self.username)
                can_register = False
            if email_check:
                self.error += "'{}' email adresi zaten kullanımda.\n".format(self.email)
                can_register = False
            if can_register:
                self.new_user = User(self.username, self.email, self.password, self.isAdmin)
                db.session.add(self.new_user)
                db.session.commit()
                self.register_success = True

    def validate(self):
        if self.form.check.data is not None:
            if self.form.check.data == "on":
                self.is_admin = True

        if self.request.method == "POST" and self.form.validate_on_submit():
            self.username = self.form.username.data
            self.password = self.form.password.data
            self.email = self.form.email.data
            self.checkValidation()

            if self.register_success:
                flash("Kayıt Başarılı " + self.getRegisteredUser().username, "success")
            else:
                flash(self.getError(), "danger")
        else:
            flash(self.form.errors, "danger")

class LoginViewModel(object):

    def __init__(self, form, method):
        self.username = ""
        self.password = ""
        self.form = form
        self.method = method
        self.login_success = False
        self.valid_try = True
        self.error =""
        self.loggedinUser = User

    def __checkUsername(self):
        if re.match("^((\w|_|-)+)$", self.username) is None:
            self.error += "'{}'  kullanıcı adı kullanılmaya uygun değil.".format(self.username)
            self.valid_try = False

    def __checkPassword(self):
        if self.password == "":  # TODO: add a password control.
            self.error += "Şifren kullanılmaya uygun değil."
            self.valid_try = False

    def getError(self):
        return self.error

    def getLoginSuccess(self):
        return self.login_success

    def getLoggedInUser(self):
        return self.loggedinUser

    def checkValidation(self):
        self.__checkPassword()
        self.__checkUsername()
        if self.valid_try:
            self.loggedinUser = User.query.filter_by(username=self.username).first()
            if self.loggedinUser:
                if self.loggedinUser.check_password(self.password):
                    login_user(self.loggedinUser)
                    self.login_success = True
                else:
                    self.error = "Şifre hatalı"
            else:
                self.error = "Bu isimde kullanıcı bulunamadı."

    def validate(self):
        if self.form.validate_on_submit() and self.method == "POST":
            self.username = self.form.username.data
            self.password = self.form.password.data
            self.checkValidation()
            if self.getLoginSuccess():
                flash("Giriş başarılı, hoşgeldin " + self.getLoggedInUser().username + ".", "success")
            else:
                flash(self.getError(), "warning")
        else:
            flash(self.form.errors, "danger")


class EventViewModel(object):

    def __init__(self, form, method):
        self.date = ""
        self.form = form
        self.request_method = method

    def __event_exist(self):
        return Event.query.filter_by(date=self.date).first()

    def submit_event(self):
        if self.request_method == "POST" and self.form.validate_on_submit():
            self.date = self.form.date.data
            if self.__event_exist():
                flash("Seçtiğiniz tarih ve saat maalesef dolu : " + "(" + self.date + "). Başka tarih seçmeyi deneyin.", "danger")
            else:
                event = Event(self.date)
                db.session.add(event)
                current_user.event.append(event)
                flash("Yer ayırtıldı : " + "(" + self.date + "). Profilinizden görebilirsiniz.", "success")
                db.session.add(current_user)
                db.session.commit()
        else:
            flash(self.form.errors, "danger")

    @staticmethod
    def get_all_events():
        return Event.query.order_by(Event.id.desc()).all()

from model.user import Users
from sqlalchemy.orm.exc import NoResultFound
from validate_email import validate_email
import hashlib


class UsersRepository:
    def __init__(self, ConnectionHandler) -> None:
        self.__ConnectionHandler = ConnectionHandler

    def select(self):
        with self.__ConnectionHandler() as db:
            try:
                data = db.session.query(Users).all()
                return data
            except Exception as ex:
                db.session.rollback()
                raise ex

    def select_user(self, uemail, upwd):
        #hashedPassword = self.hashPassword(upwd)
        #print(hashedPassword)
        with self.__ConnectionHandler() as db:
            try:
                hashedPassword = hashlib.sha256(upwd.encode()).hexdigest()
                data = db.session.query(Users).filter(
                    Users.uemail == uemail).filter(Users.upwd == hashedPassword).one()
                return data
            except NoResultFound:
                return None
            except Exception as ex:
                db.session.rollback()
                raise ex

    def insert(self, uname, uemail, upwd):
        res = self.select_user(uname,upwd)

        if (res == None or len(res) == 0):
            is_verified = self.validation(uname, uemail, upwd)
            if (is_verified):
                #hashedPassword = self.hashPassword(upwd)
                hashedPassword = hashlib.sha256(upwd.encode()).hexdigest()
                with self.__ConnectionHandler() as db:
                    try:
                        dbins = Users(uname=uname, uemail=uemail,
                                      upwd=hashedPassword)
                        db.session.add(dbins)
                        db.session.commit()
                        return 1
                    except Exception as ex:
                        db.session.rollback()
                        raise ex
            else:
                return is_verified
        else:
            return 5    

    def delete(self, uname):
        with self.__ConnectionHandler() as db:
            try:
                db.session.query(Users).filter(Users.uname == uname).delete()
                db.session.commit()
                return 1
            except Exception as ex:
                db.session.rollback()
                raise ex

    def update(self, uemail, uname):
        with self.__ConnectionHandler() as db:
            try:
                db.session.query(Users).filter(
                    Users.uemail == uemail).update({'uname': uname})
                db.session.commit()
                return 1
            except Exception as ex:
                db.session.rollback()
                raise ex

    def validation(self, uname, uemail, upwd):
        valid_email = validate_email(uemail, verify=True)
        if len(uname) < 6 or len(uname) > 25:
            return 2
        elif (not valid_email):
            return 3
        elif len(upwd) < 4 or len(upwd) > 15:
            return 4
        else: return 1

    def hashPassword(self, upassword):
        # Encode password into a readable utf-8 byte code:
        encpwd = upassword.encode('utf-8')

        # Hash the encoded password and generate a salt:
        hashedPassword = bcrypt.hashpw(encpwd, bcrypt.gensalt(10))
        return hashedPassword


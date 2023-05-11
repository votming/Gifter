from admin.views.countries import CountryView
from admin.views.currencies import CurrencyView
from admin.views.language import LanguageView
from admin.views.paragraphs import ParagraphView
from admin.views.roles import RoleView
from admin.views.titles import TitleView
from admin.views.users import UserView
from app.modules.database import engine
from app.modules.database import session
from app.modules.models import User
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing import Optional


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        # And update session
        user = session.query(User).filter(User.login == username, User.password == password).first()
        if user:
            request.session.update({"token": "some_token", 'login': user.login, 'role': user.role.name})
            return True
        return False
#JUMA4PSMSK9S
#FKCR9FVPPKWJ
    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth


def mount_admin_routes(app):
    authentication_backend = AdminAuth(secret_key="somekey")
    admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
    admin.add_view(CountryView)
    admin.add_view(LanguageView)
    admin.add_view(CurrencyView)
    admin.add_view(TitleView)
    admin.add_view(ParagraphView)
    admin.add_view(RoleView)
    admin.add_view(UserView)







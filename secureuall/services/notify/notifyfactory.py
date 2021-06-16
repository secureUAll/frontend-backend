from .email import EmailNotify
from .teams import TeamsNotify
from .notify import Notify

class NotifyFactory:

    @staticmethod
    def createNotification(name: str) -> Notify:
        if name == "Email":
            return EmailNotify()
        if name == "Microsoft Teams":
            return TeamsNotify()

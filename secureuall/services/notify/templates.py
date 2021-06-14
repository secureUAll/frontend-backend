from services.notify.notify import Notify


class Templates:

    @staticmethod
    def hostdown(notify: Notify, name: str, hostname: str, machineid: int, recipient: list) -> int:
        # Templates.hostdown(EmailNotify(), "Manuel", "abc.pt", 3, "gmatos.ferreira@sapo.pt")
        notify\
            .heading(f"Hello {notify.bold(name)},")\
            .text(f" Your host {notify.bold(hostname)} could not be reached by our system. Please check that it is available and make an instant request on the machine page. If the problem persists contact the system administrator. ")\
            .text("For more information visit your host page on Secure(UA)ll website.")\
            .button(f"https://deti-vuln-mon.ua.pt/machines/{machineid}", "Machine page")\
            .text("Remember to keep your software updated,", end="")\
            .text(notify.bold("Secure(UA)ll"))
        return notify.send("[Secure(UA)ll alert] Your machine is down", "Your machine is down!", recipient)

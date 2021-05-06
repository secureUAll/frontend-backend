import re
from ..models import Machine, MachineWorker


class MachineHandler:
    ipRegex = r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
    dnsRegex = r"([a-zA-Z0-9]([-a-zA-Z0-9]{0,61}[a-zA-Z0-9])?\.){0,2}([a-zA-Z0-9]{1,2}([-a-zA-Z0-9]{0,252}[a-zA-Z0-9])?)\.([a-zA-Z]{2,63})"
    inputRegex = r",|;|\n"


    @staticmethod
    def machineValid(machine):
        """
        Tells if machine is valid
        -- Parameter
        machine             machines.models.Machine
        -- Returns
        valid               bool
        """
        print(machine)
        if not machine.dns and not machine.ip:
            return False
        if machine.ip and not re.fullmatch(MachineHandler.ipRegex, machine.ip):
            return False
        if machine.dns and not re.fullmatch(MachineHandler.dnsRegex, machine.dns):
            return False
        print("VALID")
        return True


    @staticmethod
    def machinesFromInput(input:str):
        """
        Convert text input to Machine objects (without saving to the database)
        -- Parameters
        input               String
        -- Returns
        machinesList        machines.models.Machine[]
        ignored             int                             Number of invalid machines in input
        """
        # Split input
        original = [m.strip() for m in re.split(MachineHandler.inputRegex, input)]
        # Create Machine objects
        machines = [
            Machine(
                ip=m if re.match(MachineHandler.ipRegex, m) else None,
                dns=m if re.match(MachineHandler.dnsRegex,m) else None
            ) for m in original
        ]
        # A Machine must have a dns or ip!
        machines = [m for m in machines if MachineHandler.machineValid(m)]
        return machines, len(original)-len(machines)


    @staticmethod
    def gatherFormByNumber(request):
        """
        Gathers form attributes with numbers together
        For example: { name0: , lastName0:, name1: , lastName1: }
        Returns: { 0: { name: , lastName: } 1: { name: , lastName: } }
        -- Parameters
        request             request.POST
        -- Returns
        numbers             dict
        """
        numbers = {}
        # For every form parameter
        for key, val in request.items():
            # Find keys with numbers
            r = re.search(r"[0-9]+", key)
            if not r:
                continue
            r = r[0]
            # Add key, val to number dictionary
            if r not in numbers:
                numbers[r] = {}
            numbers[r][key.replace(str(r), "")] = val
        return numbers

    @staticmethod
    def machinesDetailsForm(machinesData, worker):
        """
        Processes a machines detail form
        -- Parameters
        machinesData        dict                        Object { id: {ip: , dns: , location: , scanLevel: , periodicity: } }
        worker              workers.models.Worker       The worker do associate machines with
        -- Returns
        machinesList        machines.models.Machine[]
        success             bool
        """
        machinesList = []
        invalid = False
        # For machine dict, create Machine object
        for id, m in machinesData.items():
            mobj = Machine(**m)
            # Validate object
            if not MachineHandler.machineValid(mobj):
                mobj.invalid = True
                invalid = True
            # Add to list
            machinesList.append(mobj)
        # If any invalid, return list with error flag
        if invalid:
            return machinesList, False
        # If they are all valid, store to the db
        for m in machinesList:
            m.save()
            MachineWorker.objects.create(machine=m, worker=worker)
        return machinesList, True




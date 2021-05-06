import re

from django.db.models import Q

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
        if not machine.dns and not machine.ip:
            return False
        if machine.ip and not re.fullmatch(MachineHandler.ipRegex, machine.ip):
            return False
        if machine.dns and not re.fullmatch(MachineHandler.dnsRegex, machine.dns):
            return False
        return True


    @staticmethod
    def machinesFromInput(input:str, worker):
        """
        Convert text input to Machine objects (without saving to the database)
        -- Parameters
        input               String
        -- Returns
        machinesList        machines.models.Machine[]
        ignored             int                             Number of invalid machines in input
        alreadyAssociated   int                             Number of machines that were already associated with worker
        edit                bool                            Does any machine match any at the db?
        """
        machines = []
        # Split input
        original = [m.strip() for m in re.split(MachineHandler.inputRegex, input.strip())]
        # Create Machine objects
        edit = False
        alreadyAssociated = 0
        for m in original:
            mobj = Machine(
                ip=m if re.fullmatch(MachineHandler.ipRegex, m) else None,
                dns=m if re.fullmatch(MachineHandler.dnsRegex,m) else None
            )
            if not MachineHandler.machineValid(mobj):
                continue
            dbQuery = Machine.objects.filter((Q(dns=mobj.dns) & Q(dns__isnull=False) & ~Q(dns="")) | (Q(ip=mobj.ip) & Q(ip__isnull=False) & ~Q(ip="")))
            if dbQuery.exists():
                mobj = dbQuery.first()
                mobj.edit = True
                edit = True
                if MachineWorker.objects.filter(machine=dbQuery.first(), worker=worker).exists():
                    mobj.alreadyAssociated = True
                    alreadyAssociated += 1
            machines.append(mobj)
        return machines, len(original)-len(machines), alreadyAssociated, edit


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
        alreadyAssociated   int                             Number of machines that were already associated with worker
        success             bool
        """
        machinesList = []
        invalid = False
        alreadyAssociated = 0
        # For machine dict, create Machine object
        for id, m in machinesData.items():
            mobj = Machine(**m)
            # Validate object
            if not MachineHandler.machineValid(mobj):
                mobj.invalid = True
                invalid = True
            # Check if already exists
            dbQuery = Machine.objects.filter((Q(dns=mobj.dns) & Q(dns__isnull=False) & ~Q(dns="")) | (Q(ip=mobj.ip) & Q(ip__isnull=False) & ~Q(ip="")))
            if dbQuery.exists():
                mobj.edit = True
                if MachineWorker.objects.filter(machine=dbQuery.first(), worker=worker).exists():
                    mobj.alreadyAssociated = True
                    alreadyAssociated += 1
            # Add to list
            machinesList.append(mobj)
        # If any invalid, return list with error flag
        if invalid:
            return machinesList, alreadyAssociated, False
        # If they are all valid, store to the db
        finalList = []
        for m in machinesList:
            # If already exists, update parameters
            dbQuery = Machine.objects.filter((Q(dns=m.dns) & Q(dns__isnull=False) & ~Q(dns="")) | (Q(ip=m.ip) & Q(ip__isnull=False) & ~Q(ip="")))
            if dbQuery.exists():
                dbMachine = dbQuery.first()
                dbMachine.scanLevel = m.scanLevel
                dbMachine.periodicity = m.periodicity
                dbMachine.location = m.location
                dbMachine.save()
                m=dbMachine
            # Else, create new object
            else:
                m.save()
            # If not associated to worker yet, associate
            if not MachineWorker.objects.filter(machine=m, worker=worker).exists():
                MachineWorker.objects.create(machine=m, worker=worker)
            finalList.append(m)
        return finalList, alreadyAssociated, True




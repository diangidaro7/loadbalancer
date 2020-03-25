from uuid import uuid4


class User:
    """Users who will perform tasks on servers that will be created automatically by Load Balancer."""

    def __init__(self, tasks):
        """Init User class."""
        self.__name = f'USER-{str(uuid4())[:8]}'
        self.__completed_ttasks = 0
        self.__tasks = tasks
        print(f'Novo usuário online: {self.__name}')

    @property
    def name(self):
        """Get user name."""
        return self.__name

    @property
    def completed_tasks(self):
        """Number of tasks completed by the user."""
        return self.__completed_ttasks

    @property
    def tasks(self):
        """Maximum sequence of tasks execution."""
        return self.__tasks

    def execute_task(self):
        """Run the task for the user.

        :return: success information.
        """
        self.__completed_ttasks += 1
        print(f'- Execução do usuário {self.name} número {self.__completed_ttasks}')
        return 'success'


class Server:
    """Server to manage active users."""

    def __init__(self):
        """Init Server class."""
        self.__name = f'SERVER-{str(uuid4())[:8]}'
        self.__users = list()
        print(f'Novo servidor criado: {self.__name}')

    @property
    def name(self):
        """Get the server name."""
        return self.__name

    @property
    def users(self):
        """Get all active users on the server."""
        return self.__users

    def allocate_user(self, user):
        """Allocate a new user to the server."""
        self.__users.append(user)
        print(f'Usuário {user.name} alocado no servidor {self.name}')

    def run_users_tasks(self):
        """Perform the task for all active users."""
        for user in reversed(self.users):
            user.execute_task()
            if user.completed_tasks >= user.tasks:
                del self.__users[self.__users.index(user)]
                print(f'    - Usuário {user.name} encerrou suas tasks e foi removido do servidor {self.name}')


class LoadBalancer:
    """Load balancer that will manage servers and users."""

    def __init__(self, max_user_server: int):
        """Init LoadBalancer class.

        :param max_user_server: Max number users in the servers.
        """
        self.__servers = list()
        self.__max_user_server = max_user_server
        self.__price = 0
        self.__output = list()

    @property
    def servers(self):
        """Server active in the load balancer."""
        return self.__servers

    @property
    def price(self):
        """Current usage price."""
        return self.format_currency(self.__price)

    @property
    def users(self):
        """User active in the servers."""
        users = list()
        for server in self.servers:
            for user in server.users:
                users.append(user)
        return users

    @property
    def output(self):
        """Output that will be stored in output.txt."""
        return self.__output

    @staticmethod
    def format_currency(value):
        """Formatt float to currency."""
        return ('R$ {:.2f}'.format(float(value))).replace('.', ',')

    def __allocate_new_server(self, server: Server):
        self.__servers.append(server)

    def __price_update(self):
        self.__price += len(self.servers)
        print(f'Custo para execução da Tick: {self.price}')
        return self.__price

    def __turn_off_server(self, server: Server):
        del self.__servers[self.__servers.index(server)]
        print(f'- Servidor {server.name} foi desativado por não haver usuários online')

    def set_output(self, tick: int, input: str = '0'):
        """Set the value to output."""
        if len(self.servers) > 0:
            output = ', '.join(list(map(lambda server: str(len(server.users)), self.servers)))
        else:
            output = '0'

        self.__output.append({
            'tick': tick,
            'input': input,
            'output': output
        })

    def create_new_server(self):
        """Create a new server."""
        new_server = Server()
        self.__allocate_new_server(new_server)
        return 'success'

    def clean_servers(self):
        """Check all servers and shuts down those without users."""
        for server in reversed(self.servers):
            if len(server.users) == 0:
                self.__turn_off_server(server)

    def allocate_new_user(self, user: User) -> bool:
        """Allocate a new user for some disponible server.

        :param user: instance of class User
        :return: allocate: bool
        """
        allocate = False

        for server in self.servers:
            if len(server.users) >= self.__max_user_server:
                continue
            server.allocate_user(user)
            allocate = True

        if not allocate:
            self.create_new_server()
            return self.allocate_new_user(user)

        return allocate

    def execute_tick(self):
        """Execute all taks for the all task's users actives."""
        self.__price_update()
        for server in self.servers:
            server.run_users_tasks()

    def end_active_tasks(self, last_tick: int):
        """Execute all active task.

        :parameter last_tick: Last tick in the simulation.
        """
        if len(self.servers) > 0:
            tick = last_tick
            while True:
                tick += 1
                print(f'TICK: {tick}')
                self.clean_servers()
                if len(self.servers) == 0:
                    self.set_output(tick=tick)
                    break

                self.set_output(tick=tick)
                self.execute_tick()
                print(50 * '=')
            print(50 * '=')
            self.turn_off_load_balancer()

    def turn_off_load_balancer(self):
        """Create a file output.txt with the information about this execution."""

        print(f'Não há servidores ou usuários online nesse momento.')
        print(f'Processo de LoadBalancer finalizado com sucesso.')
        print(f'Custo total: {self.price}')

        file = open('output.txt', 'w+')
        file.write('\n'.join(list(map(lambda output: output.get('output'), self.output))))
        file.write(f'\n{self.__price}')
        file.close()
        print('Arquivo output.txt gerado com sucesso.')

from load_balancer import LoadBalancer, User

MAX_USER_SERVER = 2
TASKS = 1


class TestLoadBalancer:

    def test_create_new_server(self):
        load_balancer = LoadBalancer(MAX_USER_SERVER)
        status = load_balancer.create_new_server()
        assert status == 'success'

    def test_allocate_new_user(self):
        load_balancer = LoadBalancer(MAX_USER_SERVER)
        new_user = User(TASKS)
        status = load_balancer.allocate_new_user(new_user)
        assert status is True

    def test_run_tasks(self):
        new_user = User(TASKS)
        status = new_user.execute_task()
        assert status == 'success'

    def test_price_increase(self):
        load_balancer = LoadBalancer(MAX_USER_SERVER)
        users_creation = 3
        for user in range(users_creation):
            new_user = User(TASKS)
            load_balancer.allocate_new_user(new_user)
        load_balancer.execute_tick()
        assert load_balancer.price != 'R$ 0,00'

    def test_run_full(self):
        with open('input.txt', 'r') as file:
            lines = file.read()
            data = lines.split('\n')
            ttask = int(data[0])
            umax = int(data[1])
            file.close()

        load_balancer = LoadBalancer(umax)
        print(50 * '=')

        tick = 0
        for tick, users in enumerate(data[2:], start=1):
            if users == '':
                continue

            print(f'TICK: {tick}')
            if int(users) > 0:
                for user in range(int(users)):
                    new_user = User(ttask)
                    load_balancer.allocate_new_user(new_user)

            load_balancer.set_output(tick=tick, input=users)
            load_balancer.execute_tick()
            load_balancer.clean_servers()
            print(50 * '=')

        load_balancer.end_active_tasks(last_tick=tick)

        assert load_balancer.price == 'R$ 15,00'


if __name__ == '__main__':
    testes = TestLoadBalancer()
    testes.test_run_full()
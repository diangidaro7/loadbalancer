from load_balancer import LoadBalancer, User
import os


if __name__ == '__main__':

    if os.path.exists('input.txt'):
        with open('input.txt', 'r') as file:
            lines = file.read().splitlines()
            ttask = int(lines[0])
            umax = int(lines[1])

        load_balancer = LoadBalancer(umax)
        print(50 * '=')

        tick = 0
        for tick, users in enumerate(lines[2:], start=1):
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
    else:
        print('Arquivo input.txt não localizado.')

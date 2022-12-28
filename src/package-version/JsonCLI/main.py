from tomllib import load as toml_load
from os.path import join as path_join

__all__ = ['CLI']

class CLI:
    def __init__(self, CONFIG_PATH: list[str] = ['.', 'config.toml']):
        with open(file=path_join(*CONFIG_PATH), mode='rb') as file:
            self.CONFIG_DATA = toml_load(file)
        self.answer = []
        
    def clear_answer(self):
        self.answer = []

    def start(self):
        self.clear_answer()
        
        now_key = 'root'
        while 1:
            now = self.CONFIG_DATA[now_key]
            options = [i for i in now['option'].values()]
            default = now['option'][now['default']] if 'default' in now else None
            print(f'# {now["title"]}\n> {now["description"]}\n')
            print('\n'.join(f'[{index+1}] {value["name"]}' for index, value in enumerate(options)))
            option = input()
            if option == '' and default is not None:
                option = default
            else:
                option = options[int(option)-1]
            print()
            match option['goto']:
                case '%%shutdown%%':
                    self.answer = [None]
                    return
                case '%%end%%':
                    self.answer.append(option['name'])
                    return
                case x:
                    self.answer.append(option['name'])
            now_key = x

if __name__ == '__main__':
    cli = CLI(['.', 'sample', 'config.toml'])
    cli.start()
    print(cli.answer)
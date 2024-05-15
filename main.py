import argparse, sys, os, pathlib


BASE_DIR    = pathlib.Path(__file__).parent.resolve()

def parser():
    DESC = 'gb file mng'
    WRITE_HELP = 'arg0="firstname surname phone adress", arg1=method l | c'
    READ_HELP = 'arg0=method l | c'
    DEL_HELP = 'arg0="firstname surname", arg1=method l | c'
    ED_HELP = 'arg0="firstname surname", arg1="firstname surname phone address" arg2=method l | c'

    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('-w', type=str, nargs=2, help=WRITE_HELP)
    parser.add_argument('-r', type=str, nargs=1, help=READ_HELP)
    parser.add_argument('-d', type=str, nargs=2, help=DEL_HELP)
    parser.add_argument('-e', type=str, nargs=3, help=ED_HELP)
    return parser

def get_input(prompt):
    return input(prompt)

def make_prompt(name):
    return f'let"s ur {name}: '

class File_Manager():

    LINE_DATA = 'line.csv'
    COLS_DATA = 'cols.csv'
    METHOD = 'method: l=line | c=column'

    def __init__(self):
        self.e = self.setUp()

    def setUp(self):
        self.parser = parser()
        self.namespaces = self.parser.parse_args()
        return 0
    
    def get_command(self):
        prompt = 'type cmd: w | r | q: '
        cmd = get_input(prompt)
        while not (cmd in ('w', 'r', 'q')):
            cmd = get_input(prompt)
        return cmd
    
    def get_path(self, _path):
        return pathlib.Path(BASE_DIR / _path)
    
    def unformatted_data(self, args):
        if args[0] == 'c':
            return [item.split('\n') for item in args[1] if item]
        else:
            return [item.split(';') for item in args[1] if item]

    def get_format_4line(self, data):
        return f'{data[0]};{data[1]};{data[2]};{data[3]}\n'
    
    def get_format_4cols(self, data):
        return f'{data[0]}\n{data[1]}\n{data[2]}\n{data[3]}\n\n'
    
    def write_line(self, data):
        p = self.get_path(self.LINE_DATA).open('a')
        f_data = self.get_format_4line(data)
        p.write(f_data)
        print(f'write line: {f_data}')
    
    def write_cols(self, data):
        p = self.get_path(self.COLS_DATA).open('a')
        f_data = self.get_format_4cols(data)
        p.write(f_data)
        print(f'write cols:\n{f_data}')
    
    def read_line(self, args, _print=True):
        p = self.get_path(self.LINE_DATA).open('r')
        data = p.read()
        if _print:
            print(data)
        return data.split('\n')
    
    def read_cols(self, args, _print=True):
        p = self.get_path(self.COLS_DATA).open('r')
        data = p.read()
        if _print:
            print(data)
        return data.split('\n\n')

    def write_data(self, args):
        if args[0] == 'l':
            self.write_line(args[1:])
        else:
            self.write_cols(args[1:])
        print('write data done')
        return 0
    
    def read_data(self, args, _print=True):
        if args[0] == 'c':
            return self.read_cols(args[1:], _print)
        else:
            return self.read_line(args[1:], _print)
    
    def rewrite_cols(self, data):
        p = self.get_path(self.COLS_DATA)
        f_data = ''
        for user in data:
            f_data += self.get_format_4cols(user)
        p.write_text(f_data)
        return 0, f'done'
    
    def rewrite_line(self, data):
        p = self.get_path(self.LINE_DATA)
        f_data = ''
        for user in data:
            f_data += self.get_format_4line(user)
        p.write_text(f_data)
        return 0, f'done'
    
    def rewrite_data(self, args):
        if args[0] == 'c':
            return self.rewrite_cols(args[1:])
        else:
            return self.rewrite_line(args[1:])

    def write_process(self):
        NAME = 'firstname'
        SNAME = 'surname'
        PHONE = 'phone'
        ADRESS = 'adress'
        
        name_ = get_input(make_prompt(NAME))
        sname_ = get_input(make_prompt(SNAME))
        phone_ = get_input(make_prompt(PHONE))
        adress_ = get_input(make_prompt(ADRESS))

        method_ = get_input(make_prompt(self.METHOD))
        if not (method_ in ('c', 'l')):
            method_ = 'l'
        return self.write_data((method_, name_, sname_, phone_, adress_))
    
    def read_process(self):
        method_ = get_input(make_prompt(self.METHOD))
        if not (method_ in ('c', 'l')):
            method_ = 'l'
        return self.read_data((method_,))

    def base_process(self):
        cmd = self.get_command()
        if cmd == 'q':
            print('f_mng close')
            return 0
        elif cmd == 'w':
            return self.write_process()
        elif cmd == 'r':
            return self.read_process()
        else:
            print('unknown command')
            return 0
    
    def check_data(self, data):
        data = data[0].split()
        if len(data) != 4:
            return 1, f'there must be 4 arguments. but now it"s: {len(data)}'
        else:
            return 0, data
    
    def write_check_method(self, args):
        _method = args[-1]
        if _method not in ('l', 'c'):
            method_ = get_input(make_prompt(self.METHOD))
            if not (method_ in ('c', 'l')):
                method_ = 'l'
        state, resp = self.check_data(args[:-1])
        if state:
            print(f'invalid data: {resp}')
            return 1
        self.write_data((_method, *resp))
        return 0
    
    def check_method(self, _method):
        if _method not in ('l', 'c'):
            return f'invalid method: {_method}'
        return 0
    
    def read_check_method(self, args):
        resp = self.check_method(args[0])
        if resp:
            print(resp)
            return self.read_process()
        return self.read_data((args[0],))
    
    def check_write(self, args):
        return self.write_check_method(args)
    
    def check_read(self, args):
        return self.read_check_method(args)
    
    def check_del_method(self, method):
        if method not in ('l', 'c'):
            return 1, f'supports only methods l | c'
        return 0, method
    
    def del_user(self, find_user, data):
        find_user = find_user.split()
        idx = 0
        for item in data:
            if find_user[0] == item[0] and find_user[1] == item[1]:
                data.pop(idx)
                print(f'delete: {item}')
                return 0, data
            idx += 1
        return 1, f'not this user'
    
    def edit_user(self, edit_user, edited_user, data):
        edit_user = edit_user.split()
        idx = 0
        for item in data:
            if edit_user[0] == item[0] and edit_user[1] == item[1]:
                data.pop(idx)
                print(f'edit: {item} >> {edited_user}')
                data.append(edited_user.split())
                return 0, data
            idx += 1
        return 1, 'not this user'
    
    def find_user(self, args):
        data = self.read_data((args[-1],), _print=False)
        undata = self.unformatted_data((args[-1], data))
        state, data = self.del_user(args[0], undata)
        if state:
            print(f'{data}')
            return 1, data
        return self.rewrite_data((args[-1], *data))

    def del_process(self, args):
        state, resp = self.check_del_method(args[-1])
        if state:
            print(f'{resp}')
            return 1
        state, resp = self.find_user(args)
        if state:
            print(f'don"t delete')
            return 1
        return 0
    
    def find_edit(self, args):
        data = self.read_data((args[-1],), _print=False)
        undata = self.unformatted_data((args[-1], data))
        state, data = self.edit_user(args[0], args[1], undata)
        if state:
            print(data)
            return 1
        # print(f'data:\n{data}')
        return self.rewrite_data((args[-1], *data))
    
    def edit_process(self, args):
        resp = self.check_method(args[-1])
        if resp:
            print(resp)
            return 1
        return self.find_edit(args)
    
def setUp():
    os.chdir(BASE_DIR)
    return File_Manager()

def main(args):
    f_mng = setUp()
    if not args:
        return f_mng.base_process()
    if f_mng.namespaces.w:
        return f_mng.check_write(f_mng.namespaces.w)
    if f_mng.namespaces.r:
        return f_mng.check_read(f_mng.namespaces.r)
    if f_mng.namespaces.d:
        return f_mng.del_process(f_mng.namespaces.d)
    if f_mng.namespaces.e:
        return f_mng.edit_process(f_mng.namespaces.e)

if __name__ == '__main__':
    print('start...')
    main(sys.argv[1:])
    print('done')
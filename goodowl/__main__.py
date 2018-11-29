from enum import Enum
import json
import pprint

from carl import command, Arg
import owlready2 as owl


class Log(Enum):
    RESET = '\033[0m'
    INFO = '\033[93m'
    GOOD = '\033[92m'
    ERROR = '\033[91m'


def log(kind, text, *args, **kwargs):
    print(f'[{kind.value}{kind.name}{Log.RESET.value}] {text}',
          *args,
          **kwargs)


def build_stub_ontology(prefix: str = 'http://own.tology'):
    onto = owl.get_ontology(prefix)

    with onto:
        # Definitions

        # Language-related
        class Language(owl.Thing):
            pass

        class Dialect(owl.Thing):
            equivalent_to = Language

        class Implementation(owl.Thing):
            pass

        class Domain(owl.Thing):
            pass

        class target_domain(Language >> Domain):
            pass

        class DomainSpecific(Language):
            equivalent_to = [Language & target_domain.max(1, Domain)]

        class GeneralPurpose(Language):
            equivalent_to = [Language & target_domain.exactly(0, Domain)]

        # Software-related
        class Program(owl.Thing):
            pass

        class Compiler(Implementation):
            pass

        class Interpreter(Implementation):
            pass

        class VirtualMachine(Program):
            pass

        # Properties
        class mother(Dialect >> Language):
            pass

        # Behaviors
        class implements(Implementation >> Language):
            pass

        class runs_in(Compiler >> VirtualMachine):
            pass

    with open('stub.json') as f:
        contents = json.load(f)

    data = {}

    for name, about in contents['languages'].items():
        lang = Language(name)

        try:
            lang.target_domain = [Domain(a) for a in about['domains']]
        except KeyError as e:
            print('    ', end='')
            log(Log.INFO, f'{name} has no about[{e}]')

        data[name] = lang

    for name, _mother in contents['dialects'].items():
        lang = Dialect(name)
        lang.mother = [_mother]
        data[name] = lang

    for name, properties in contents['compilers'].items():
        compiler = Compiler(name)

        try:
            compiler.implements = [properties['implements']]
        except KeyError:
            pass

        try:
            compiler.runs_in = [properties['runs_in']]
        except KeyError:
            pass

        data[name] = compiler

    for name, properties in contents['interpreters'].items():
        interpreter = Interpreter(name)

        try:
            interpreter.implements = [properties['implements']]
        except KeyError:
            pass

        try:
            interpreter.runs_in = [properties['runs_in']]
        except KeyError:
            pass

        data[name] = interpreter

    for name in contents['vm']:
        VirtualMachine(name)

    return onto


def load_ontology(path: str):
    log(Log.INFO, f'Welcome to the new ontology analyser!')
    if path == '--stub':
        log(Log.INFO, f'Building stub ontology...')
        onto = build_stub_ontology()
    else:
        log(Log.INFO, f'Analysing "{path}"...')
        owl.onto_path.append(path)
        onto = owl.get_ontology(path).load()
    log(Log.GOOD, 'Done loading ontology.')

    return onto


def show_classes(onto: owl.namespace.Ontology):
    classes = [*onto.classes()]
    log(Log.INFO, f'Found {len(classes)} classes:')
    for _class in classes:
        ans = [str(ans).split('.')[-1] for ans in _class.ancestors()]
        ins = [str(ins).split('.')[-1] for ins in _class.instances()]
        print(f'       Class {_class}:\n'
              f'           Ancestors: {ans}\n'
              f'           Instances: {ins}')


def show_obj_properties(onto: owl.namespace.Ontology):
    obj_props = [*onto.object_properties()]
    if obj_props:
        log(Log.INFO, f'Object properties:')
        for i, prop in enumerate(obj_props):
            print(f'       {i+1}. {prop}')
    else:
        log(Log.INFO, 'No Object Properties.')


NOCLASS = object()


def show_which_implements(onto: owl.namespace.Ontology, classname: str):
    def show_impl(impl: str):
        log(Log.INFO, f'{impl} implements:')
        for i, lang in enumerate(impl.implements):
            print(f'    {i+1}: {lang}')

    if classname is NOCLASS:
        log(Log.INFO, 'Showing all implementations:')
        # for impl in onto['webprotege.stanford.edu.RBcN21gLfPDk63bFltEHZTL'].instances():
        #     show_impl(impl)
    else:
        show_impl(classname)


def show_inconsistencies(onto):
    inconsistencies = [*onto.inconsistent_classes()]
    if inconsistencies:
        for i, _class in enumerate(inconsistencies[1:]):
            if i == 0 and inconsistencies:
                log(Log.WARN, f'There are inconsistent classes:')
            print(f'       {i + 1} {_class}')
    else:
        log(Log.GOOD, f'There are no inconsistent classes.')


def show_class(onto, classname):
    log(Log.INFO, f'About {classname}: ')
    print(pprint.pformat(onto[classname].__dict__))


@command
def main(path: str = '',
         output: str = None,
         stub: Arg(action = 'store_true') = False,
         infer: Arg(action = 'store_true') = False):
    if stub:
        path = '--stub'
    elif not path:
        log(Log.ERROR, f'Missing filename')
        exit(1)

    onto = load_ontology(path)
    show_classes(onto)
    show_obj_properties(onto)
    show_which_implements(onto, NOCLASS)

    if infer:
        with onto:
            owl.sync_reasoner()

    show_inconsistencies(onto)
    show_classes(onto)
    if output:
        onto.save(file=output, format='owlxml')
    # show_class(onto, 'SQL')


if __name__ == '__main__':
    main.run()

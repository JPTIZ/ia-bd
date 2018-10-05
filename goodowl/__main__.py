from sys import argv

from carl import command, Arg
import owlready2 as owl


def build_stub_ontology(prefix: str = 'http://own.tology'):
    onto = owl.get_ontology(prefix)

    with onto:
        # Definitions
        class Language(owl.Thing):
            pass

        class Implementation(owl.Thing):
            pass

        class Program(owl.Thing):
            pass

        class Compiler(Implementation):
            pass

        class Interpreter(Implementation):
            pass

        class VirtualMachine(Program):
            pass

        # Behaviors
        class implements(Implementation >> Language):
            pass

        class runs_in(Compiler >> VirtualMachine):
            pass

    python = Language('Python')
    cpython = Interpreter('CPython')
    cpython.implements = [python]
    pypy = Interpreter('Pypy')
    pypy.implements = [python]

    return onto


def load_ontology(path: str):
    print('[INFO] Welcome to the new ontology analyser!')
    if path == '--stub':
        print(f'[INFO] Building stub ontology...', end='')
        onto = build_stub_ontology()
    else:
        print(f'[INFO] Analysing "{path}"...', end='')
        owl.onto_path.append(path)
        onto = owl.get_ontology(path).load()
    print('Done')

    return onto


def show_classes(onto: owl.namespace.Ontology):
    print(type(onto))
    classes = [*onto.classes()]
    print(f'\n[INFO] {len(classes)} found:')
    for _class in classes:
        print(f'       Class {_class}:\n'
              f'           Ancestors: {_class.ancestors()}\n'
              f'           Instances: {_class.instances()}')


def show_obj_properties(onto: owl.namespace.Ontology):
    obj_props = [*onto.object_properties()]
    if obj_props:
        print(f'\n[INFO] Object properties:')
        for i, prop in enumerate(obj_props):
            print(f'       {i+1}. {prop}')
    else:
        print('\n[INFO] No Object Properties.')


NOCLASS = object()
def show_which_implements(onto: owl.namespace.Ontology, classname: str):
    def show_impl(impl: str):
        print(f'[INFO] {impl} implements:')
        for i, lang in enumerate(impl.implements):
            print(f'    {i+1}: {lang}')

    if classname is NOCLASS:
        print('\n[INFO] Showing all implementations:')
        for impl in onto['Implementation'].instances():
            show_impl(impl)
    else:
        show_impl(classname)


def show_inconsistencies(onto):
    inconsistencies = [*onto.inconsistent_classes()]
    if inconsistencies:
        for i, _class in enumerate(inconsistencies[1:]):
            if i == 0 and inconsistencies:
                print('[WARN] There are inconsistent classes:')
            print(f'       {i + 1} {_class}')
    else:
        print('[GOOD] There are no inconsistent classes.')


@command
def main(path: str = '',
         output: str = None,
         stub: Arg(action='store_true') = False,
         infer: Arg(action='store_true') = False):
    if stub:
        path = '--stub'
    else:
        print('[ERROR] Missing filename')
        exit(1)

    onto = load_ontology(path)
    show_classes(onto)
    show_obj_properties(onto)
    show_which_implements(onto, NOCLASS)

    if infer:
        with onto:
            owl.sync_reasoner()

    show_inconsistencies(onto)
    if output:
        onto.save(file=output, format='rdfxml')


if __name__ == '__main__':
    main.run()

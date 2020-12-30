from __future__ import annotations

import itertools
from copy import deepcopy
from enum import Enum, auto
from typing import Set, Tuple, TYPE_CHECKING, List, Union

from specification import Specification
from specification.enums import *
from specification.exceptions import NotSatisfiableException, AtomNotSatisfiableException
from tools.logic import LogicTuple, Logic
from type import Boolean
from typeset import Typeset

if TYPE_CHECKING:
    from specification.atom import Atom, AtomKind


class Formula(Specification):
    def __init__(self,
                 atom: Union[Atom, str] = None,
                 kind: FormulaKind = None):

        if kind is None:
            self.__kind = FormulaKind.UNDEFINED
        self.__kind = kind

        if self.__kind == FormulaKind.REFINEMENT_RULES or \
                self.__kind == FormulaKind.ADJACENCY_RULES or \
                self.__kind == FormulaKind.MUTEX_RULES:
            self.__spec_kind = SpecKind.RULE
        else:
            self.__spec_kind = SpecKind.UNDEFINED

        self.__refinement_rules = None
        self.__mutex_rules = None
        self.__adjacency_rules = None

        self.__saturation = None

        if isinstance(atom, str) and atom == "TRUE":
            from specification.atom import Atom
            new_atom = Atom("TRUE")
            self.__cnf: List[Set[Atom]] = [{new_atom}]
            self.__dnf: List[Set[Atom]] = [{new_atom}]

        elif isinstance(atom, str) and atom == "FALSE":
            from specification.atom import Atom
            new_atom = Atom("FALSE")
            self.__cnf: List[Set[Atom]] = [{new_atom}]
            self.__dnf: List[Set[Atom]] = [{new_atom}]

        elif atom is not None:
            self.__cnf: List[Set[Atom]] = [{atom}]
            self.__dnf: List[Set[Atom]] = [{atom}]

        else:
            raise Exception("Wrong parameters LTL construction")

    from ._printing import pretty_print

    @property
    def kind(self) -> FormulaKind:
        return self.__kind

    @kind.setter
    def kind(self, value: FormulaKind):
        self.__kind = value

    @property
    def spec_kind(self) -> SpecKind:
        return self.__spec_kind

    @spec_kind.setter
    def spec_kind(self, value: SpecKind):
        self.__spec_kind = value

    @property
    def cnf(self) -> List[Set[Atom]]:
        return self.__cnf

    @property
    def dnf(self) -> List[Set[Atom]]:
        return self.__dnf

    def _remove_atoms(self, atoms_to_remove: Set[Atom]):
        """Remove Atoms from Formula"""

        """Remove from CNF"""
        for clause in self.__dnf:
            clause -= atoms_to_remove

        """Remove from CNF"""
        clause_cnf_to_remove = set()
        for clause in self.__cnf:
            """Remove clause if contains atoms to be removed"""
            if clause & atoms_to_remove:
                clause_cnf_to_remove |= clause

        """Filter out clauses"""
        for clause in list(self.cnf):
            if len(clause & clause_cnf_to_remove) > 0:
                self.__cnf.remove(clause)

    @staticmethod
    def extract_refinement_rules(typeset: Typeset) -> Formula:
        """Extract Refinement rules from the Formula"""

        refinement_rules = None

        for key_type, set_super_types in typeset.super_types.items():
            if isinstance(key_type, Boolean):
                for super_type in set_super_types:
                    f = Logic.g_(Logic.implies_(key_type.name, super_type.name))
                    t = Typeset({key_type, super_type})
                    from specification.atom import Atom
                    new_atom = Atom(formula=(f, t), kind=AtomKind.REFINEMENT_RULE)
                    new_formula = Formula(atom=new_atom, kind=FormulaKind.REFINEMENT_RULES)
                    if refinement_rules is None:
                        refinement_rules = new_formula
                    else:
                        refinement_rules &= new_formula

        return refinement_rules

    @staticmethod
    def extract_mutex_rules(typeset: Typeset) -> Formula:
        """Extract Mutex rules from the Formula"""

        mutex_rules = None

        for mutex_group in typeset.mutex_types:
            or_elements = []
            for mutex_type in mutex_group:
                neg_group = mutex_group.symmetric_difference({mutex_type})
                and_elements = [mutex_type.name]
                for elem in neg_group:
                    and_elements.append(Logic.not_(elem.name))
                or_elements.append(Logic.and_(and_elements))
            f = Logic.g_(Logic.or_(or_elements))
            t = Typeset(mutex_group)
            from specification.atom import Atom
            new_atom = Atom(formula=(f, t), kind=AtomKind.MUTEX_RULE)
            new_formula = Formula(atom=new_atom, kind=FormulaKind.MUTEX_RULES)
            if mutex_rules is None:
                mutex_rules = new_formula
            else:
                mutex_rules &= new_formula

        return mutex_rules

    @staticmethod
    def extract_adjacency_rules(typeset: Typeset) -> Formula:
        """Extract Adjacency rules from the Formula"""

        adjacency_rules = None

        for key_type, set_adjacent_types in typeset.adjacent_types.items():
            if isinstance(key_type, Boolean):
                """G(a -> X(b | c | d))"""
                f = Logic.g_(Logic.implies_(key_type.name, Logic.x_(Logic.or_([e.name for e in set_adjacent_types]))))
                t = Typeset({key_type, set_adjacent_types})
                new_atom = Atom(formula=(f, t), kind=AtomKind.ADJACENCY_RULE)
                new_formula = Formula(atom=new_atom, kind=FormulaKind.ADJACENCY_RULES)
                if adjacency_rules is None:
                    adjacency_rules = new_formula
                else:
                    adjacency_rules &= new_formula

        return adjacency_rules

    def relax_by(self, formula: Formula):
        """
        Given the assumption as set of conjunctive clauses connected by the disjunction operator (DNF),
        we can simplify any conjunct a_i in a clause x if exists a guarantee (a_j -> g_j) such that:
        1) a_j is part of x
        2) g_j -> a_i is a valid formula

        DNF = (a & b) | (c & d)
        CNF = (a | c) & (a | d) & (b | c) & (b | d)

        simplify a =>
        DNF = (b) | (c & d)
        CNF = (b | c) & (b | d)

        """
        for guarantee in formula.cnf:
            if len(guarantee) == 1:
                g = list(guarantee)[0]
            else:
                raise Exception
            atoms_to_remove = set()
            for clause in self.dnf:
                if g.saturation is not None:
                    if g.saturation in clause:
                        for conjunct in clause:
                            if (g.unsaturated >> conjunct).is_valid():
                                print(f"{str(g)} relaxes {str(conjunct)}")
                                atoms_to_remove.add(conjunct)
                else:
                    for conjunct in clause:
                        if (g.unsaturated >> conjunct).is_valid():
                            print(f"{str(g)} relaxes {str(conjunct)}")
                            atoms_to_remove.add(conjunct)

            self._remove_atoms(atoms_to_remove)

    @property
    def atoms(self) -> Set[Atom]:
        new_set = set()
        for group in self.cnf:
            new_set |= group
        return new_set

    def contains_rule(self, rule: AtomKind = None):
        return any([e.contains_rule(rule) for e in self.atoms])

    def saturate(self, value: Specification):
        """
        Saturate each atom of the formula, CNF and DNF
        x->((a | b) & (c | d)) === ((x->a) | (x->b)) & ((x->c) | (x->d))
        x->((a & b) | (c & d)) === ((x->a) & (x->b)) | ((x->c) & (x->d))
        """
        if not value.is_true():
            for clause in self.cnf:
                for atom in clause:
                    atom.saturate(value)
        """Atoms are shared between CNF and DNF"""

    def formula(self, formulatype: FormulaOutput = FormulaOutput.CNF) -> Tuple[str, Typeset]:
        """Generate the formula"""

        if formulatype == FormulaOutput.CNF:
            return LogicTuple.and_(
                [LogicTuple.or_([a.formula() for a in atoms], brakets=True) for atoms in self.cnf],
                brackets=False)

        if formulatype == FormulaOutput.DNF:
            return LogicTuple.or_(
                [LogicTuple.and_([a.formula() for a in atoms], brackets=True) for atoms in self.dnf],
                brakets=False)

    def __and__(self, other: Formula) -> Formula:
        """self & other
        Returns a new Specification with the conjunction with other"""
        if not isinstance(other, Formula):
            raise AttributeError

        if other.is_false():
            return Formula("FALSE")

        new_ltl = deepcopy(self)

        if other.is_true():
            return new_ltl

        """Cartesian product between the two dnf"""
        new_ltl.__dnf = []
        for a, b in itertools.product(self.dnf, other.dnf):

            new_set = a | b

            try:
                from specification.atom import Atom
                Atom(LogicTuple.and_([f.formula() for f in new_set], brackets=True))
                new_ltl.dnf.append(new_set)
            except AtomNotSatisfiableException:
                """Do not append if its unsatisfiable"""
                pass

        if len(new_ltl.dnf) == 0:
            """Result is FALSE"""
            return Formula("FALSE")

        """Append to list if not already there"""
        for other_elem in other.cnf:
            if other_elem not in new_ltl.cnf:
                new_ltl.cnf.append(other_elem)

        if not new_ltl.is_satisfiable():
            raise NotSatisfiableException(self, other)

        return new_ltl

    def __or__(self, other: Formula) -> Formula:
        """self | other
        Returns a new Specification with the disjunction with other"""
        global Atom
        if not isinstance(other, Formula):
            raise AttributeError

        if other.is_true():
            return Formula("TRUE")

        new_ltl = deepcopy(self)

        if other.is_false():
            return new_ltl

        """Cartesian product between the two cnf"""
        new_ltl.__cnf = []
        for a, b in itertools.product(self.cnf, other.cnf):

            new_set = a | b

            from specification.atom import Atom
            atom = Atom(LogicTuple.or_([f.formula() for f in new_set]), check=False)
            if not atom.is_valid():
                new_ltl.cnf.append(new_set)

        if len(new_ltl.cnf) == 0:
            """Result is TRUE"""
            return Formula("TRUE")

        """Append to list if not already there"""
        for other_elem in other.dnf:
            if other_elem not in new_ltl.dnf:
                new_ltl.dnf.append(other_elem)

        return new_ltl

    def __invert__(self) -> Formula:
        """Returns a new Specification with the negation of self"""

        new_ltl = deepcopy(self)

        """Negate all atoms"""
        for atom in new_ltl.atoms:
            atom.negate()

        """Swap CNF with DNF"""
        new_ltl.__cnf, new_ltl.__dnf = new_ltl.dnf, new_ltl.cnf

        return new_ltl

    def __rshift__(self, other: Union[Formula, Atom]) -> Formula:
        """>>
        Returns a new Specification that is the result of self -> other (implies)
        NOT self OR other"""
        from specification.atom import Atom
        if isinstance(other, Atom):
            other = Formula(other)

        if self.is_true():
            return other

        new_ltl = ~ self

        return new_ltl | other

    def __lshift__(self, other: Union[Formula, Atom]) -> Formula:
        """<<
        Returns a new Specification that is the result of other -> self (implies)
        NOT other OR self"""
        from specification.atom import Atom
        if isinstance(other, Atom):
            other = Formula(other)

        new_ltl = ~ other

        return new_ltl | self

    def __iand__(self, other: Union[Formula, Atom]) -> Formula:
        """self &= other
        Modifies self with the conjunction with other"""
        from specification.atom import Atom
        if isinstance(other, Atom):
            other = Formula(other)

        """Cartesian product between the two dnf"""
        for a, b in itertools.product(self.__dnf, other.dnf):
            a.update(b)

        """Append to list if not already there"""
        for other_elem in other.cnf:
            if other_elem not in self.cnf:
                self.cnf.append(other_elem)

        if not self.is_satisfiable():
            raise NotSatisfiableException(self, other)

        return self

    def __ior__(self, other: Union[Formula, Atom]) -> Formula:
        """self |= other
        Modifies self with the disjunction with other"""
        from specification.atom import Atom
        if isinstance(other, Atom):
            other = Formula(other)

        """Cartesian product between the two cnf"""
        for a, b in itertools.product(self.__cnf, other.cnf):
            a.update(b)

        """Append to list if not already there"""
        for other_elem in other.dnf:
            if other_elem not in self.dnf:
                self.dnf.append(other_elem)

        if not self.is_satisfiable():
            raise NotSatisfiableException(self, other)

        return self

import sys
import os
import shutil

from components.components import ComponentsLibrary, Component, SimpleComponent
from goals.operations import create_contextual_clusters, mapping, create_cgt, \
    pretty_cgt_exception
from helper.tools import save_to_file
from mapping_specification import get_inputs
from src.goals.cgtgoal import *
from typescogomo.subtypes.assumption import *
from typescogomo.subtypes.scopes import *
from typescogomo.variables import BoundedNat

results_path = os.path.dirname(os.path.abspath(__file__)) + "/output/results"
try:
    shutil.rmtree(results_path)
except:
    pass

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))

ap, rules, goals = get_inputs()

if __name__ == "__main__":
    """The designer specifies a mission using the predefined catalogue of patterns 
       In addition to the patterns to use the designer specifies also in which context each goal can be active"""


    """Create cgt with the goals, it will automatically compose/conjoin them based on the context"""
    context_goals = create_contextual_clusters(list_of_goals, "MUTEX", context_rules)

    for ctx, goals in context_goals.items():
        from helper.buchi import generate_buchi

        g_name = "||".join(g.name for g in goals)
        generate_buchi(ctx, file_path + "/buchi/" + g_name)

    # save_to_file(pretty_print_summary_clustering(context_goals), file_path + "/context-goals")

    try:
        cgt = create_cgt(context_goals, compose_with_context=False)
    except CGTFailException as e:
        print(pretty_cgt_exception(e))
        sys.exit()

    save_to_file(str(cgt), file_path + "/cgt_1_contexual")

    """Adding Domain Properties (i.e. descriptive statements about the problem world (such as physical laws)
    E.g. a robot cannot be in two locations at the same time. These properties are intrinsic in each pattern"""
    # cgt.add_domain_properties()

    save_to_file(str(cgt), file_path + "/cgt_2_domain")

    """Adding Domain Hypothesis or Expectations (i.e. prescriptive assumptions on the environment
    E.g. In the environment of deployment of the mission the item weight 10kg so in order to pick it up 
    there is a new assumption where the 'weight_power' must be at least 10"""
    expectations = [
        Contract(
            assumptions=Assumptions(
                LTL(
                    formula="G(weight_power > 10)",
                    variables=Variables(BoundedNat("weight_power")),
                    kind="expectation")),
            guarantees=Guarantees(
                LTL(
                    formula="G(heavy_item_pickup)",
                    variables=Variables(Boolean("heavy_item_pickup")))))
    ]

    # cgt.add_expectations(expectations)

    save_to_file(str(cgt), file_path + "/cgt_3_expectations")

    """Import library of components from file"""

    """Instantiating a Library of Components"""
    component_library = ComponentsLibrary(name="robots")

    """Import library of components from file"""
    # list_of_components = parse("./input_files/robots_components_simple.txt")

    """Or define them here"""
    component_library.add_components(
        [
            SimpleComponent(
                component_id="robot_1",
                guarantees=["robot_power = 7"]
            ),
            SimpleComponent(
                component_id="robot_2",
                guarantees=["robot_power >= 8"],
            ),
            SimpleComponent(
                component_id="robot_3",
                guarantees=["robot_power >= 9"],
            ),
            Component(
                component_id="collaborate",
                assumptions=Assumptions([
                    LTL(
                        formula="power1 >= 8",
                        variables=Variables(BoundedNat(port_type="robot_power", name="power1"))),
                    LTL(
                        formula="power2 >= 8",
                        variables=Variables(BoundedNat(port_type="robot_power", name="power2")))
                ]),
                guarantees=Guarantees(
                    LTL(
                        formula="G(weight_power > 12)",
                        variables=Variables(BoundedNat("weight_power")))
                ),
            ),
            SimpleComponent(
                component_id="pick_up_item",
                assumptions=["G(weight_power > 12)"],
                guarantees=["G(heavy_item_pickup)"]
            )
        ]
    )

    """Looking in the library for components for goals that can refine all the goals to pickup an object 'a->pickup'"""
    goals_to_map = cgt.get_all_goals_with_name("a->pickup")

    for goal in goals_to_map:
        mapping(component_library, goal)

    save_to_file(str(cgt), file_path + "/cgt_4_mapping")

    """Refinements formalize a notion of substitutability. We can substitute goals with most refined one.
    For example, from 'cgt_4_mapping' we can substitute 'a->pickup' with 'collaborate||robot_2||pick_up_item||robot_3'"""
    cgt.substitute_with("a->pickup", "collaborate||pick_up_item||robot_2||robot_3")

    """Notice how all the tree is consistent with the substitution 
    that had relaxed the expectation 'G(weight_power > 10)' from all the CGT"""
    save_to_file(str(cgt), file_path + "/cgt_5_substitution")

    """The designer can specify to 'abstract' a goal to have fewer guarantees, however CoGoMo will keep the guarantees
    that are needed to 'relax' assumptions in other goals of the trees"""
    guarantees = Guarantees(LTL("G(locB -> F(heavy_item_pickup))"))
    cgt.abstract_guarantees_of("collaborate||pick_up_item||robot_2||robot_3",
                               guarantees, "pick_up_item_abstracted")
    save_to_file(str(cgt), file_path + "/cgt_6_abstracted")

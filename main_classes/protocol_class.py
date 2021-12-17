from main_classes.loop_step import Loop_Step, Loop_Step_Container

class Measurement_Protocol:
    """Class for the measurement protocols. It mainly contains loop_steps and plots."""
    def __init__(self, loop_steps=None, plots=None):
        if plots is None:
            plots = []
        if loop_steps is None:
            loop_steps = []
        self.loop_steps = loop_steps
        self.loop_step_dict = {}
        for step in self.loop_steps:
            update_all_children(self.loop_step_dict, step)
        self.plots = plots

    def build(self):
        """Making the runable-protocol..."""
        # TODO this function...
        pass

    def add_loop_step(self, loop_step, position=-1, parent_step_name=None, model=None):
        """Adds a loop_step to the protocol (or the parent_step)at the specified position. Also appends the loop_step to the given model. The loop_step is added to the list as well as the dictionary.
        Arguments:
            - loop_step: The loop_step object to be added.
            - position: the position where to add it to the list / parent, default -1, appends the loopstep to the end
            - parent_step_name: name of the parent loop_step. If specified, the loop_step is added to the parrent instead of the main sequence
            - model: if specified, the loop_step is also added to that QStandardItemModel"""
        if parent_step_name is None:
            if position < 0:
                self.loop_steps.append(loop_step)
            else:
                self.loop_steps.insert(position, loop_step)
        else:
            loop_step.parent_step = parent_step_name
            self.loop_step_dict[parent_step_name].add_child(loop_step, position)
        if model is not None:
            loop_step.append_to_model(model)
        self.loop_step_dict.update({loop_step.full_name: loop_step})

    def add_loop_step_rec(self, loop_step, model=None, parent_step_name=None, position=-1):
        """Recursively adds the loop_step and all its children to the protocol. Steps are added to the list if they have no parent, otherwise to the parent. All are added to the dictionary."""
        if parent_step_name is None:
            self.add_loop_step(loop_step, model=model, parent_step_name=parent_step_name, position=position)
        else:
            if model is not None:
                loop_step.append_to_model(model, parent=parent_step_name)
            if loop_step not in self.loop_step_dict[parent_step_name].children:
                self.loop_step_dict[parent_step_name].add_child(loop_step, position)
            self.loop_step_dict.update({loop_step.full_name: loop_step})
        if loop_step.has_children:
            for child in loop_step.children:
                self.add_loop_step_rec(child, parent_step_name=loop_step.full_name, model=model)

    def remove_loop_step(self, loop_step_name):
        """Removes the step with the given name from the sequence-list (or parent) and from the dictionary."""
        step = self.loop_step_dict.pop(loop_step_name)
        if step.parent_step is not None:
            self.loop_step_dict[step.parent_step].remove_child(step)
        else:
            self.loop_steps.remove(step)


    def load_loop_steps(self, loop_steps, model=None):
        """Takes a list of loop_steps, creates them (with the input data of each step) and adds them to the specified model."""
        for step in loop_steps:
            loop_step = self.make_step(step)
            self.add_loop_step_rec(loop_step, model=model)

    def make_step(self, step_info):
        """Creates the step specified with step_info (including the children), 'step_type' gives which subclass of Loop_Step shall be created."""
        children = []
        if step_info['has_children']:
            for child in step_info['children']:
                child_step = self.make_step(child)
                child_step.parent_step = step_info['full_name']
                children.append(child_step)
        if step_info['step_type'] == 'Default':
            st = Loop_Step(step_info['name'])
        elif step_info['step_type'] == 'Container':
            st = Loop_Step_Container(step_info['name'], children)
        st.full_name = step_info['full_name']
        return st

    def load_plots(self, plots):
        # TODO this function
        self.plots = plots

    def rearrange_loop_steps(self, step_list):
        """Takes a list of loopsteps, each entry consisting of a tuple of the loopstep name and its children, which is recursively the same kind of list.
        Re-populates the loop_step_dict and then puts the loop_steps in the correct order."""
        self.loop_step_dict = {}
        for step in self.loop_steps:
            update_all_children(self.loop_step_dict, step)
        self.loop_steps = []
        for step, children in step_list:
            self.loop_step_dict[step].children = []
            append_all_children(children, self.loop_step_dict[step], self.loop_step_dict)
            self.loop_steps.append(self.loop_step_dict[step])

def append_all_children(child_list, step, step_dict):
    """Takes a list of the kind specified in rearrange_loop_steps, does the same as the other function, but recursively for all the (grand-)children."""
    for child, grandchildren in child_list:
        child_step = step_dict[child]
        child_step.children = []
        append_all_children(grandchildren, child_step, step_dict)
        child_step.parent_step = step.full_name
        step.children.append(child_step)

def update_all_children(step_dict, step):
    """Similar to append_all_children, but only updating the step_dict with all the children."""
    step_dict.update({step.full_name: step})
    if step.has_children:
        for child in step.children:
            update_all_children(step_dict, child)

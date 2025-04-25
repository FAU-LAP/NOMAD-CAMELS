from ophyd import SignalRO


class Variable_Signal(SignalRO):
    """
    A class to provide a bluesky signal for the variables of a CAMELS protocol.


    Parameters
    ----------
    variables_dict : dict
        A dictionary containing the variables to be read. The keys are the variable names,
        and the values are the corresponding values.
    """

    def __init__(
        self,
        name,
        value=None,
        timestamp=None,
        parent=None,
        labels=None,
        kind="normal",
        tolerance=None,
        rtolerance=None,
        metadata=None,
        cl=None,
        attr_name="",
        variables_dict=None,
    ):
        super().__init__(
            name=name,
            value=value,
            timestamp=timestamp,
            parent=parent,
            labels=labels,
            kind=kind,
            tolerance=tolerance,
            rtolerance=rtolerance,
            metadata=metadata,
            cl=cl,
            attr_name=attr_name,
        )
        self.variables_dict = variables_dict or {}
        self.vars = list(sorted(self.variables_dict.keys()))

    def describe(self):
        """
        Describe as the variables.
        """
        return {
            self.name: {
                "source": "local_NOMAD_CAMELS_variables",
                "dtype": "string",
                "shape": [],  # Scalar string
                "variables": self.vars,
            }
        }

    def get(self):
        """
        Get the values of the variables from the variables_dict.
        """
        data = {
            key: self.variables_dict[key]
            for key in sorted(self.variables_dict.keys())
            if key in self.vars
        }
        self._readback = data
        return super().get()

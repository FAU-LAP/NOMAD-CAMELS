from ophyd import SignalRO


class Variable_Signal(SignalRO):
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
        return {
            self.name: {
                "source": "local_NOMAD_CAMELS_variables",
                "dtype": "string",
                "shape": [],  # Scalar string
                "variables": self.vars,
            }
        }

    def get(self):
        data = {
            key: self.variables_dict[key]
            for key in sorted(self.variables_dict.keys())
            if key in self.vars
        }
        self._readback = data
        return super().get()

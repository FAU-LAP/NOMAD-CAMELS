from tqdm import tqdm

class ProgressBar:
    """ """
    def __init__(self, n_steps):
        self.n_steps = n_steps
        self.bar = tqdm(total=n_steps)

    def emit(self, n):
        """

        Parameters
        ----------
        n :
            

        Returns
        -------

        """
        self.bar.update()


class ForkManager:

    def __init__(self, engine):
        self.engine = engine

    def launch_forks(self, snapshot, perturbations):
        forks = []

        for perturb in perturbations:
            fork_engine = self.engine.clone_from_snapshot(snapshot)
            perturb.apply(fork_engine)
            forks.append(fork_engine)

        return forks

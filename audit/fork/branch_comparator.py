class BranchComparator:

    def compare(self, baseline, forked):
        divergences = []

        for b, f in zip(baseline, forked):
            divergences.append(abs(b - f))

        return divergences

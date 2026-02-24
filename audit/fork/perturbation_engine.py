class PerturbationEngine:
    def apply(self, snapshot, field_id, delta):
        snapshot["world_state"]["fields"][field_id] += delta

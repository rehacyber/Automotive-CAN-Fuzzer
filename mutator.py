import random


class PayloadMutator:

    def __init__(self):
        self.patterns = [
            0x00,
            0xFF,
            0xAA,
            0x55
        ]


    def random_mutation(self, data):

        mutated = data.copy()

        index = random.randint(
            0,
            len(mutated) - 1
        )

        mutated[index] = random.randint(
            0,
            255
        )

        return mutated



    def pattern_mutation(self, data):

        value = random.choice(
            self.patterns
        )

        return [
            value
            for _ in range(len(data))
        ]



    def boundary_mutation(self, data):

        mutated = data.copy()

        for i in range(len(mutated)):

            if i % 2 == 0:
                mutated[i] = 0x00

            else:
                mutated[i] = 0xFF

        return mutated



    def mutate(self, data, mode="random"):

        if mode == "random":

            return self.random_mutation(data)


        elif mode == "pattern":

            return self.pattern_mutation(data)


        elif mode == "boundary":

            return self.boundary_mutation(data)


        else:

            return data
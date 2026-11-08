import math
import random
import json
import os
import time

MEMORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cat_memory.json")

class NeuralBrain:
    def __init__(self):
        self.num_inputs = 7
        self.num_hidden = 16
        self.num_actions = 11

        self.action_names = [
            "idle_watch",
            "peeking_bookmark",
            "curious_scratch",
            "happy_bounce",
            "purr_cozy",
            "empathy_beg",
            "sad_pout",
            "angry_hiss",
            "turned_cold",
            "curled_catnap",
            "dramatic_scratch_wipe"
        ]

        self.w1 = []
        self.b1 = []
        self.w2 = []
        self.b2 = []

        self.w1_int8 = []
        self.b1_int8 = []
        self.w2_int8 = []
        self.b2_int8 = []
        self.scale_w1 = 127.0
        self.scale_w2 = 127.0
        self.quantized_mode = True

        self.affection = 0.5
        self.patience = 0.8
        self.streak_days = 1
        self.total_pets = 0
        self.tantrum_fatigue = 0.0

        self.load_memory()
        self.quantize_network()

    def init_random_weights(self):
        random.seed(42)
        self.w1 = [[random.uniform(-0.4, 0.4) for _ in range(self.num_hidden)] for _ in range(self.num_inputs)]
        self.b1 = [random.uniform(-0.1, 0.1) for _ in range(self.num_hidden)]

        self.w2 = [[random.uniform(-0.4, 0.4) for _ in range(self.num_actions)] for _ in range(self.num_hidden)]
        self.b2 = [random.uniform(-0.1, 0.1) for _ in range(self.num_actions)]

        self._seed_natural_instincts()
        self.quantize_network()

    def _seed_natural_instincts(self):
        for h in range(self.num_hidden):
            self.w1[2][h] += 0.5
            self.w2[h][9] += 0.4

            self.w1[1][h] += 0.6
            self.w2[h][5] += 0.3
            self.w2[h][6] += 0.25

            self.w1[0][h] += 0.4
            self.w2[h][0] += 0.3

    def quantize_network(self):
        max_w1 = max(0.0001, max(abs(val) for row in self.w1 for val in row))
        self.scale_w1 = 127.0 / max_w1
        self.w1_int8 = [[int(round(val * self.scale_w1)) for val in row] for row in self.w1]
        self.b1_int8 = [int(round(val * self.scale_w1)) for val in self.b1]

        max_w2 = max(0.0001, max(abs(val) for row in self.w2 for val in row))
        self.scale_w2 = 127.0 / max_w2
        self.w2_int8 = [[int(round(val * self.scale_w2)) for val in row] for row in self.w2]
        self.b2_int8 = [int(round(val * self.scale_w2)) for val in self.b2]

    def forward_quantized_int8(self, inputs):
        in_int8 = [int(round(max(0.0, min(1.0, x)) * 127.0)) for x in inputs]

        hidden_int = []
        for j in range(self.num_hidden):
            acc = self.b1_int8[j] * 127
            for i in range(self.num_inputs):
                acc += in_int8[i] * self.w1_int8[i][j]

            normalized_acc = acc / (127.0 * self.scale_w1)
            act_int = int(round(math.tanh(normalized_acc) * 127.0))
            hidden_int.append(act_int)

        logits = []
        for k in range(self.num_actions):
            acc = self.b2_int8[k] * 127
            for j in range(self.num_hidden):
                acc += hidden_int[j] * self.w2_int8[j][k]
            logits.append(acc / (127.0 * self.scale_w2))

        return logits

    def forward(self, inputs):
        if self.quantized_mode and self.w1_int8:
            logits = self.forward_quantized_int8(inputs)
        else:
            hidden = []
            for j in range(self.num_hidden):
                total = self.b1[j]
                for i in range(self.num_inputs):
                    total += inputs[i] * self.w1[i][j]
                act = math.tanh(total)
                hidden.append(act)

            logits = []
            for k in range(self.num_actions):
                total = self.b2[k]
                for j in range(self.num_hidden):
                    total += hidden[j] * self.w2[j][k]
                logits.append(total)

        if inputs[2] > 0.6:
            logits[9] += 2.5

        if inputs[1] > 1.3:
            if self.tantrum_fatigue <= 0.1:
                logits[10] += 3.0
            else:
                logits[8] += 2.0
                logits[7] += 1.5
        elif inputs[1] > 1.0:
            logits[5] += 1.8
            logits[6] += 1.4

        if inputs[0] > 0.8 and inputs[1] < 0.8:
            logits[0] += 1.2
            logits[1] += 0.8

        exp_vals = []
        max_logit = max(logits)
        temperature = 0.8
        for l in logits:
            scaled = (l - max_logit) / temperature
            exp_vals.append(math.exp(max(-20.0, min(20.0, scaled))))

        sum_exp = sum(exp_vals)
        probabilities = [v / sum_exp for v in exp_vals]

        r = random.random()
        cumulative = 0.0
        chosen_action_idx = 0
        for idx, prob in enumerate(probabilities):
            cumulative += prob
            if r <= cumulative:
                chosen_action_idx = idx
                break

        chosen_action = self.action_names[chosen_action_idx]
        return chosen_action, probabilities

    def learn_from_petting(self):
        self.affection = min(1.0, self.affection + 0.05)
        self.total_pets += 1
        for j in range(self.num_hidden):
            self.w2[j][3] += 0.02
            self.w2[j][4] += 0.02
        self.quantize_network()
        self.save_memory()

    def learn_from_break_taken(self):
        self.patience = min(1.0, self.patience + 0.1)
        self.affection = min(1.0, self.affection + 0.03)
        self.quantize_network()
        self.save_memory()

    def record_tantrum_occurred(self):
        self.tantrum_fatigue = 1.0
        self.patience = 0.4
        self.quantize_network()
        self.save_memory()

    def decay_tantrum_fatigue(self):
        if self.tantrum_fatigue > 0.0:
            self.tantrum_fatigue = max(0.0, self.tantrum_fatigue - 0.05)

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    data = json.load(f)
                    self.w1 = data.get("w1", [])
                    self.b1 = data.get("b1", [])
                    self.w2 = data.get("w2", [])
                    self.b2 = data.get("b2", [])
                    self.affection = data.get("affection", 0.5)
                    self.patience = data.get("patience", 0.8)
                    self.total_pets = data.get("total_pets", 0)
                    self.streak_days = data.get("streak_days", 1)
                    if len(self.w1) == self.num_inputs and len(self.w2) == self.num_hidden:
                        self.quantize_network()
                        return
            except Exception:
                pass

        self.init_random_weights()
        self.save_memory()

    def save_memory(self):
        try:
            data = {
                "w1": self.w1,
                "b1": self.b1,
                "w2": self.w2,
                "b2": self.b2,
                "affection": round(self.affection, 3),
                "patience": round(self.patience, 3),
                "total_pets": self.total_pets,
                "streak_days": self.streak_days,
                "quantized_int8": True,
                "last_saved": time.time()
            }
            with open(MEMORY_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

neural_brain = NeuralBrain()

if __name__ == "__main__":
    print("Testing INT8 Quantized Neural Brain...")
    test_inputs = [0.9, 0.4, 0.0, 0.7, 0.2, 0.6, 0.0]
    action, probs = neural_brain.forward(test_inputs)
    print("Quantized INT8 Inference Completed!")
    print("Decided Action:", action)
    print(f"Top Action Prob: {max(probs)*100:.1f}%")

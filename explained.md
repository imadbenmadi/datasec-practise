
This table is a cheat sheet for **Machine Learning (ML) Security**. It breaks down how attackers try to compromise AI systems at different stages of their lifecycle, from the raw data all the way to the live production server.

Here is the plain-English translation of this chart, broken down by layer so you can cram it quickly. Think of this in terms of standard application architecture to make it click faster:

### 1. Data Layer (The Raw Input)

This happens before the AI is even built. Attackers are messing with the raw files or database records (think of the raw files sitting in your local Node.js public structure) so the AI learns the wrong things from the start.

* **Label-flip poisoning:** An "Insider" (someone with access) intentionally changes the labels on the data (e.g., labeling spam emails as "not spam"). **Goal:** Make the AI inaccurate. **Defense:** Outlier detection (finding the data points that don't match the rest).
* **Backdoor samples:** Someone in the "Supply chain" (where you buy or source your data) hides a secret trigger. For example, they train a vision AI to recognize faces, but if someone wears a specific pair of red glasses, it always unlocks. **Goal:** Plant a trojan. **Defense:** Data sanitization (cleaning and verifying the data).

### 2. Training Layer (The Build Phase)

This is when the algorithm is actively crunching the data to build the model.

* **Membership inference:** A "Black-box" attacker (they can only see the inputs and outputs, not the code) tries to figure out if a specific person's private data was used in the training set. **Goal:** Steal privacy. **Defense:** DP-SGD (Differential Privacy - basically adding mathematical "noise" during training so individual records can't be reverse-engineered).

### 3. Model Layer (The Compiled Logic)

The AI is built and compiled into a file containing "weights" (the mathematical rules it learned).

* **Weight trojans:** A "Post-hoc compromise" (the attacker hacked the system *after* the model was built) directly alters the compiled model's internal math. **Goal:** Add hidden, malicious functionality. **Defense:** Activation clustering (monitoring the neural network to see if it "fires" in weird, anomalous ways).

### 4. Inference Layer (The Live API)

This is the production phase. The AI is live and taking user requests, just like an Express API endpoint taking public traffic.

* **Evasion (FGSM/PGD):** A "White-box" attacker (they can see your code/model) sends a specifically manipulated input—like an image with altered pixels invisible to the human eye—to trick the AI. **Goal:** Misclassification. **Defense:** Adversarial training (training your AI specifically to recognize and reject these trick images).
* **Model inversion:** A "Black-box" attacker spams the live API with specific requests to work backward and recreate the original, private training data. **Goal:** Reconstruct data. **Defense:** Differential privacy (again, adding noise to the outputs so they can't be traced back).
* **Sponge attacks:** A "Black-box" attacker sends complex, bloated inputs specifically designed to make your server do maximum mathematical computation. **Goal:** DoS (Denial of Service) and crashing your server. **Defense:** Standard API defenses—Input validation and rate limiting.

### 5. Ops Layer (The Infrastructure)

This is the physical or cloud server level hosting the whole system.

* **Model theft:** An attacker uses "Reconnaissance" (scanning your servers, finding open ports) to literally download and steal your proprietary AI model files. **Goal:** IP (Intellectual Property) exposure. **Defense:** Logging and anomaly detection. You stop this by setting up rigorous, continuous audit logs—similar to tracking user actions in a secure task management dashboard—to catch anyone accessing files they shouldn't be.

**Quick tip for the test:** Focus heavily on the difference between **White-box** (attacker knows the system internals) and **Black-box** (attacker only interacts with the public-facing inputs/outputs). Good luck—you've got this.
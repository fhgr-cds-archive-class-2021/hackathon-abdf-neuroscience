import numpy as np

window = 30

alpha_queue = np.array([])
beta_queue = np.array([])
gamma_queue = np.array([])
theta_queue = np.array([])
sigma_queue = np.array([])

def preprocessing_pipeline(alpha, beta, gamma, theta, sigma):
    if np.all(np.isnan([alpha, beta, gamma, theta, sigma])):
        return None
    
    alpha_queue.append(alpha)
    beta_queue.append(beta)
    gamma_queue.append(gamma)
    theta_queue.append(theta)
    sigma_queue.append(sigma)

    mean_freq = []
    if len(alpha_queue) >= window:     
        mean_freq.append(np.median(alpha_queue[:window]))
        mean_freq.append(np.median(beta_queue[:window]))
        mean_freq.append(np.median(gamma_queue[:window]))
        mean_freq.append(np.median(theta_queue[:window]))
        mean_freq.append(np.median(sigma_queue[:window]))

        
        max_freq = np.argmax(mean_freq)
        # 0: Alpha, 1: Beta, 2: Gamma, 3: Theta, 4: Sigma

        return max_freq

    return None


def map_index_to_brain_wave(index):
    brain_waves = ['alpha', 'beta', 'gamma', 'theta','theta']
    return np.argmax(index)
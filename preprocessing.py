import numpy as np

window = 30

alpha_queue = np.array([])
beta_queue = np.array([])
gamma_queue = np.array([])
delta_queue = np.array([])
theta_queue = np.array([])
sigma_queue = np.array([])

def preprocessing_pipeline(alpha, beta, gamma, delta, theta, sigma):
    global alpha_queue, beta_queue, gamma_queue, delta_queue, theta_queue, sigma_queue, window

    if not alpha or not beta or not gamma or not delta or not theta or not sigma:
        return None
    
    alpha = np.abs(alpha)
    beta = np.abs(beta)
    gamma = np.abs(gamma)
    delta = np.abs(delta)
    theta = np.abs(theta)
    sigma = np.abs(sigma)
    
    alpha_queue = np.append(alpha_queue, alpha)
    beta_queue = np.append(beta_queue, beta)
    gamma_queue = np.append(gamma_queue, gamma)
    delta_queue = np.append(delta_queue, delta)
    theta_queue = np.append(theta_queue, theta)
    sigma_queue = np.append(sigma_queue, sigma)

    mean_freq = []
    if len(alpha_queue) >= window:     
        mean_freq.append(np.median(alpha_queue[:window]))
        mean_freq.append(np.median(beta_queue[:window]))
        mean_freq.append(np.median(gamma_queue[:window]))
        mean_freq.append(np.median(delta_queue[:window]))
        mean_freq.append(np.median(theta_queue[:window]))
        mean_freq.append(np.median(sigma_queue[:window]))
        
        max_freq = np.argmax(mean_freq)
        # 0: alpha, 1: beta, 2: gamma, 3: delta, 4: theta, 5: sigma

        return max_freq

    return None


def map_index_to_brain_wave(index):
    brain_waves = ['alpha', 'beta', 'gamma', 'delta', 'theta', 'sigma']
    return brain_waves[np.argmax(index)]
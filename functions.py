import numpy as np

def LowsonRDT(f_vec, c, L, alpha, u, I, Lambda, r_e, phi, theta):
    #Important constants
    rho = 1.225 #kg/m³ air density
    c_0 = 340 #m/s speed of sound
    mu = 1.647*(10**-5) #Pa*s air viscosity

    #Pre-calculation parameters
    Re = rho*u*c/mu #flow Reynolds number
    M = u/c_0 #flow Mach number
    beta = np.sqrt(1-(M**2)) #Prandtl-Glauert compressibility factor
    D_L = (((np.sin(np.pi*theta/180))**2)*((np.sin(np.pi*phi/180))**2))/((1+(M*np.cos(np.pi*theta/180)))**4) #spherical directivity

    #Memory allocation
    j = len(f_vec)
    K = np.zeros(j)
    S = np.zeros(j)
    LFC = np.zeros(j)
    Aux1 = np.zeros(j)
    Aux = np.zeros(j)
    Aux4 = np.zeros(j)
    Aux5 = np.zeros(j)
    SPL = np.zeros(j)

    #Lowson method script
    for idx in range (0, j):
        K[idx] = np.pi*f_vec[idx]*c/u
        S[idx] = np.sqrt(((2*np.pi*K[idx]/(beta**2))+((1+(2.4*K[idx]/(beta**2)))**-1))**-1)
        LFC[idx] = (1+9*((alpha*np.pi/180)**2))*(10*(S[idx]**2)*M*(K[idx]**2))/(beta**2)
        Aux1[idx] = (10*np.log10((LFC[idx])/((1+(LFC[idx]))))) + 85.95
        Aux = (rho**2)*(c_0**2)*L*Lambda*(u**2)*(I**2)*(M**3)*(D_L)/(2*(r_e**2))
        Aux4[idx] = (((K[idx]**3)/((1+(K[idx]**2)))**(19/6)))
        Aux5[idx] = 10*np.log10(Aux*Aux4[idx])
        SPL[idx] = 10*np.log10((10**((Aux1[idx] + Aux5[idx])/10)))
    return SPL
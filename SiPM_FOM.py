#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 14:09:15 2020

@author: wscherer13
Import digitized SiPM and scintillator fiber performance curves
to create figures of merit for SiPM/optical fiber combinations
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def fom_sipm(fiber_dat,sipm_dat,n_intp):
    """
    Returns the Figure of Merit (FoM) for WLS fiber and SiPM digitized
    performance curves.  Interpolates points to constant width along the
    wavelength (x dimension)
    
    fiber_dat is the digitized WLS fiber emission curve as a dataframe
    
    sipm_dat is the digitized SiPM performance curve as a dataframe
    
    n_intp is the number of points of uniform width desired to interpolate to
    """
    xf = fiber_dat['Wavelength (nm)']; yf = fiber_dat['Amplitude']
    
    xs = sipm_dat['Wavelength (nm)']; ys = sipm_dat['PDE']
    
    xr = len(xf); xdiff = xf[xr-1]-xf[0]
    #Interpolate fiber data to constant width points
    xfe = np.linspace(xf[0],xf[xr-1],num=n_intp)
    
    dx = np.diff(xfe)[0]
    
    yfe = np.interp(xfe,xf,yf)
    
    ys = np.interp(xfe,xs,ys)
    
    fom = np.dot(ys/100,yfe)*dx
    
    return(fom, xfe, ys/100,yfe,dx)


def fom_plot(fiber_dat,sipm_dat,plot_title):
    """
    This function takes in fiber performance data, and takes the dot product
    of fiber emission spectra and the SiPM PDE (interpolated) to produce
    a rough figure of merit (FOM) and plots the results.
    
    All input data is normalized the max value of the respective array it came
    from, so everything can be plotted on a signle graph
    """
    
    # calculate figure of merit using dot product                         
    FOM, xsim, ysim, yfe, dx = fom_sipm(fiber_dat,sipm_dat,101)
    
    # plot the results and save the plot to local directoryftc
    fig = plt.figure()
    plt.plot(xsim,yfe,'rx-',label= 'Fiber Emit')
    plt.plot(xsim, ysim/max(sipm_dat['PDE']/100),'b*',
                 label='PDE - interp')
    plt.plot(sipm_dat['Wavelength (nm)'],sipm_dat['PDE']/max(sipm_dat['PDE']),'kx-',
                     label = 'SiPM PDE')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Amplitude (normalized)')
    tlt_str = 'FOM = ',FOM
    plt.legend(title = tlt_str)
    plt.title(str(plot_title))
    plt.grid()
    plt.draw()
    plt.savefig(plot_title+'.png')
    
    return(fig, len(xsim), dx)
    
def multi_plot(fiber_array,sipm_dat,plot_titles, figname):
    """
    This function takes in fiber performance data, and takes the dot product
    of fiber emission spectra and the SiPM PDE (interpolated) to produce
    a rough figure of merit (FOM) and plots the results.
    
    All input data is normalized the max value of the respective array it came
    from, so everything can be plotted on a signle graph
    """
    i = 1
    fig = plt.subplots(figsize=(12,5))
    dxa = []
    npoint = []
    for fiber in fiber_array:
    
    
        # calculate figure of merit using dot product                         
        FOM, xsim, ysim, yfe, dx = fom_sipm(fiber,sipm_dat,101)
        dxa.append(dx)
        npoint.append(len(xsim))
        # plot the results and save the plot to local directoryftc
        plt.subplot(1,len(fiber_array),i)
        plt.plot(xsim,yfe,'rx-',label= 'Fiber Emit')
        plt.plot(xsim, ysim/max(sipm_dat['PDE']/100),'b*',
                     label='PDE - interp')
        plt.plot(sipm_dat['Wavelength (nm)'],sipm_dat['PDE']/max(sipm_dat['PDE']),'kx-',
                         label = 'SiPM PDE')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Amplitude (normalized)')
        tlt_str = 'FoM = %.1f' % FOM
        plt.legend(title = tlt_str, loc = 'upper right',fancybox = True)
        plt.title(str(plot_titles[i-1]))
        plt.grid()
        plt.draw()
        
        
        i += 1
        
    #fig.tight_layout()   
    plt.tight_layout()
    plt.savefig(str(figname)+'.png')
    
    
    return(fig,dxa,npoint)
        
def multi_sipm(fiber_array,sipm_array,plot_titles, figname,figsz):
    """
    This function takes in fiber performance data, and takes the dot product
    of fiber emission spectra and the SiPM PDE (interpolated) to produce
    a rough figure of merit (FOM) and plots the results.
    
    All input data is normalized the max value of the respective array it came
    from, so everything can be plotted on a signle graph
    """
    i = 1
    row = len(fiber_array)
    col = len(sipm_array)
    fig = plt.subplots(figsize=figsz)
    dxa = []
    npoint = []
    for fiber in fiber_array:
        
        for sipm in sipm_array:

        
            # calculate figure of merit using dot product                         
            FOM, xsim, ysim, yfe, dx = fom_sipm(fiber,sipm,101)
            dxa.append(dx)
            npoint.append(len(xsim))
            # plot the results and save the plot to local directoryftc
            plt.subplot(row,col,i)
            plt.plot(xsim,yfe,'rx-',label= 'Fiber Emit')
            plt.plot(xsim, ysim/max(sipm['PDE']/100),'b*',
                     label='PDE - interp')
            plt.plot(sipm['Wavelength (nm)'],sipm['PDE']/max(sipm['PDE']),'kx-',
                         label = 'SiPM PDE')
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('Amplitude (normalized)')
            tlt_str = 'FoM = %.1f' % FOM
            plt.legend(title = tlt_str, loc = 'upper right',fancybox = True)
            plt.title(str(plot_titles[i-1]))
            plt.grid()
            plt.draw()
        
        
            i += 1
        
    #fig.tight_layout()
    plt.tight_layout()
    plt.savefig(str(figname)+'.png')
    
    return(fig,dxa,npoint)      
    
    



#%%

# import and plot the SG BCF-92 digitized performance data
bcf92_a = pd.read_csv('/Users/wscherer13/Documents/Phys-Research/SiPMs/plot_data/csv_files/stgobain/BCF_92_Absorp.csv',names = ['Wavelength (nm)',
                                                    'Amplitude'])
bcf92_e= pd.read_csv('/Users/wscherer13/Documents/Phys-Research/SiPMs/plot_data/csv_files/stgobainBCF_92_Emit_data.csv',names=['Wavelength (nm)',
                                                    'Amplitude'])

fig1 = plt.figure()
plt.plot(bcf92_a['Wavelength (nm)'],-1*bcf92_a['Amplitude'],'kx-',label= 'Absn')
plt.plot(bcf92_e['Wavelength (nm)'],bcf92_e['Amplitude'],'rx-',label= 'Emit')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Amplitude (normalized)')
plt.legend()
plt.title('BCF-92 Performance')
plt.grid()
plt.savefig('BCF-92_Performance.png')


# import and plot the Karary Y-11 digitized perforance data
y11_a = pd.read_csv('/Users/wscherer13/Documents/Phys-Research/SiPMs/plot_data/csv_files/kuraray/y11_absn.csv',names = ['Wavelength (nm)',
                                                    'Amplitude'])
y11_e= pd.read_csv('/Users/wscherer13/Documents/Phys-Research/SiPMs/plot_data/csv_files/kuraray/y11_emit.csv',names=['Wavelength (nm)',
                                                    'Amplitude'])

fig2 = plt.figure()
plt.plot(y11_a['Wavelength (nm)'],y11_a['Amplitude'],'kx-',label= 'Absn')
plt.plot(y11_e['Wavelength (nm)'],y11_e['Amplitude'],'rx-',label= 'Emit')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Amplitude (normalized)')
plt.legend()
plt.title('Y-11 Performance')
plt.grid()
plt.savefig('Y-11_Performance.png')

fibers = [y11_e, bcf92_e]

#%%
# import the AdvanSiD RGB-1C SiPM PDE
advn_rgb = pd.read_csv('Advn_RGB.csv',names = ['Wavelength (nm)',
                                                    'PDE'])   

# import the AdvanSiD NUV-1C SiPM PDE
advn_nuv = pd.read_csv('advn_nuv.csv',names = ['Wavelength (nm)',
                                                    'PDE'])
    
titles = ['Y-11 Fiber with AdvanSiD NUV-1C','Y-11 Fiber with AdvanSiD RGB-1C',
        'BCF-92 Fiber with AdvanSiD NUV-1C','BCF-92 Fiber with AdvanSiD RGB-1C']   
figtitle = 'Advn_sipm_fom'
sipms = [advn_nuv,advn_rgb]
fadv_nuv, dx_advn, adv_len = multi_sipm(fibers, sipms,titles,figtitle, (10,10))


#%%
# import the Hamamatsu S14160-61 SiPM PDE

hu_141 = pd.read_csv('HU_14160-61.csv',names = ['Wavelength (nm)',
                                                    'PDE'])

titles = ['Y-11 Fiber with HMU S14160-61','BCF-92 Fiber with HMU S14160-61']   
figtitle = 'HMU_14160_fom'

fhu_141 = multi_plot(fibers, hu_141,titles,figtitle)

#%%
# import the Hamamatsu S13361-2050 SiPM PDE
hu_133 = pd.read_csv('HU_13361_2050.csv',names = ['Wavelength (nm)',
                                                    'PDE'])

titles = ['Y-11 Fiber with HMU S13361-2050','BCF-92 Fiber with HMU S13361-2050']   
figtitle = 'HMU_13361-2050_fom'

fhu_133 = multi_plot(fibers, hu_133,titles,figtitle, (10,10)) 

#%%
# import the Hamamatsu S13360-25 through 75pe SiPM PDE
hu_13325 = pd.read_csv('s13360_25pe.csv',names = ['Wavelength (nm)',
                                                    'PDE'])
hu_13350 = pd.read_csv('hu_s13360-50pe.csv',names = ['Wavelength (nm)',
                                                    'PDE'])
hu_13375 = pd.read_csv('hu_s13360_75pe.csv',names = ['Wavelength (nm)',
                                                    'PDE'])
sipms = [hu_13325,hu_13350,hu_13375]
titles = ['Y-11 Fiber with HMU S13360-25pe','Y-11 Fiber with HMU S13360-50pe',
          'Y-11 Fiber with HMU S13360-75pe','BCF-92 Fiber with HMU S13360-25pe',
          'BCF-92 Fiber with HMU S13360-50pe', 'BCF-92 Fiber with HMU S13360-75pe']
figtitle = 'HMU_13360-xpe_fom'
fhu_133x = multi_sipm(fibers,sipms,titles,figtitle,(14,12))

#%%
# import the broadcom S4N44C013

bc_s4n44c_3v = pd.read_csv('BC_S4N44C013_3V_OV.csv',names = ['Wavelength (nm)',
                                                    'PDE'])
bc_s4n44c_6v = pd.read_csv('BC_S4N44C013_6V_OV.csv',names = ['Wavelength (nm)',
                                                    'PDE'])
sipms = [bc_s4n44c_3v,bc_s4n44c_6v]
titles = ['Y-11 Fiber with BC S4N44C013 3V OV','Y-11 Fiber with BC S4N44C013 6V OV',
          'BCF-92 Fiber with BC S4N44C013 3V OV','BCF-92 Fiber with BC S4N44C013 6V OV']
figtitle = 'BC_s4n44c013_fom'
bc_s4n44 = multi_sipm(fibers,sipms,titles,figtitle, (10,10))

#%%
# import the broadcom S4N66c013
bc_s4n66c_35 = pd.read_csv('bc_s4n66c013_3.5v_ov.csv',names = ['Wavelength (nm)',
                                                    'PDE'])
bc_s4n66c_8  = pd.read_csv('bc_s4n66c013_8v_ov.csv',names = ['Wavelength (nm)',
                                                    'PDE'])

sipms = [bc_s4n66c_35,bc_s4n66c_8]
titles = ['Y-11 Fiber with BC S4N66C013 3.5V OV','Y-11 Fiber with BC S4N66C013 8V OV',
          'BCF-92 Fiber with BC S4N66C013 3.5V OV','BCF-92 Fiber with BC S4N66C013 8V OV']
figtitle = 'BC_s4n66c013_fom'
bc_s4n66 = multi_sipm(fibers,sipms,titles,figtitle, (10,10))

#%%
# import the senseL fc-30035
sl_fc30_25 = pd.read_csv('sl_fc_30035_25.csv',names = ['Wavelength (nm)',
                                                    'PDE'])
sl_fc30_5  = pd.read_csv('sl_fc_30035_5.csv',names = ['Wavelength (nm)',
                                                    'PDE'])

sipms = [sl_fc30_25,sl_fc30_5]
titles = ['Y-11 Fiber with SL FC-30035 2.5V OV','Y-11 Fiber with SL FC-30035 5V OV',
          'BCF-92 Fiber with SL FC-30035 2.5V OV','BCF-92 Fiber with SL FC-30035 5V OV']
figtitle = 'sl_fc-30035_fom'
sl_fc30035 = multi_sipm(fibers,sipms,titles,figtitle, (10,10))

#%%
# import the senseL fj-60035
sl_fj60_25 = pd.read_csv('sl_fj-60035_25.csv',names = ['Wavelength (nm)',
                                                    'PDE'])
sl_fj60_6  = pd.read_csv('sl_fj-60035_6.csv',names = ['Wavelength (nm)',
                                                    'PDE'])

sipms = [sl_fc30_25,sl_fc30_5]
titles = ['Y-11 Fiber with SL fj-60035 2.5V OV','Y-11 Fiber with SL fj-60035 6V OV',
          'BCF-92 Fiber with SL fj-60035 2.5V OV','BCF-92 Fiber with SL fj-60035 6V OV']
figtitle = 'sl_fj-60035_fom'
sl_fj60035 = multi_sipm(fibers,sipms,titles,figtitle, (10,10))

#%%
# Import the First Sensor RGB-1C data

fs_rgb1c = pd.read_csv('FS_RGB1C.csv', names = ['Wavelength (nm)',
                                               'PDE'])

titles = ['Y-11 Fiber with FS RGB-SiPM 4V OV','BCF-92 Fiber with FS RGB-SiPM 4V OV']                                           
figtitle = 'fs_rgb1c_fom'
fs_rgb1c_fom = multi_plot(fibers,fs_rgb1c,titles,figtitle)

#%%
# Import the First Sensor NUV-1C data

fs_nuv1c = pd.read_csv('fs_nuv1c.csv', names = ['Wavelength (nm)',
                                               'PDE'])

titles = ['Y-11 Fiber with FS NUV-SiPM 6V OV','BCF-92 Fiber with FS NUV-SiPM 6V OV']                                           
figtitle = 'fs_nuv1c_fom'
fs_rgb1c_fom = multi_plot(fibers,fs_nuv1c,titles,figtitle)


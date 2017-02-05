
import scipy.io.wavfile
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

def readAudioFile(filename, resample=False, newBitRate=8, newSamplingRate=8000):
    fs1, y1 = scipy.io.wavfile.read(filename)
    
    # Select only left channel
    left = y1[:,0]
    left = np.abs(left)
    
    return left

def calculateParameter(audio, threshold=8000, numSamples=4096, binSize=128):
    if numSamples % binSize != 0:
        raise ValueError('numSample is not an integer multiple of binSize');
    
    # Use simple threshold technique to determine the start sample to process
    itemindex = np.where(audio>threshold)[0][0]   
    # Trim from that sample for the number of sample specify 
    # (should cover the lenght of hit sound)
    audio = audio[itemindex:itemindex+numSamples]
    # Group samples into many bins where each bin has size equal to binSize
    audio = audio.reshape(numSamples//binSize, binSize)
    # Calculate SD of each bins
    sd = np.std(audio, axis=1)
    return sd
    
    
if __name__ == "__main__":
    
#    with open('data_train.csv', 'w', newline='') as csvfile:
#        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
#        csvwriter.writerow(list(range(1, 33)) + ['class'])
#        
#        sandFileName = os.listdir('Sand')
#        for filename in sandFileName:
#            if ('.wav' in filename):
#                sd = calculateParameter(os.path.join('Sand', filename))
#                csvwriter.writerow(sd.tolist() + ['Sand'])
#                plt.plot(sd, 'r')
#                    
#        sandFileName = os.listdir('Thick')
#        for filename in sandFileName:
#            if ('.wav' in filename):
#                sd = calculateParameter(os.path.join('Thick', filename))
#                csvwriter.writerow(sd.tolist() + ['Thick'])
#                plt.plot(sd, 'b')
#            
#    with open('data_test.csv', 'w', newline='') as csvfile:
#        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
#        csvwriter.writerow(list(range(1, 33)) + ['class'])
#        
#        sandFileName = os.listdir('Sand2')
#        for filename in sandFileName:
#            if ('.wav' in filename):
#                sd = calculateParameter(os.path.join('Sand2', filename))
#                csvwriter.writerow(sd.tolist() + ['Sand'])
#                plt.plot(sd, 'r')
#                    
#        sandFileName = os.listdir('Thick2')
#        for filename in sandFileName:
#            if ('.wav' in filename):
#                sd = calculateParameter(os.path.join('Thick2', filename))
#                csvwriter.writerow(sd.tolist() + ['Thick'])
#                plt.plot(sd, 'b')
                
    with open('data_all.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
        csvwriter.writerow(list(range(1, 33)) + ['class'])
        
        #plt.axis([18,25,0,1000]) 
        
        sandFileName = os.listdir('Sand')
        for filename in sandFileName:
            if ('.wav' in filename):
                print (filename)
                audio = readAudioFile(os.path.join('Sand', filename))
                sd = calculateParameter(audio)
                csvwriter.writerow(sd.tolist() + ['Sand'])
                plt.plot(sd, 'r')
                    
        sandFileName = os.listdir('Thick')
        for filename in sandFileName:
            if ('.wav' in filename):
                print (filename)
                audio = readAudioFile(os.path.join('Thick', filename))
                sd = calculateParameter(audio)
                csvwriter.writerow(sd.tolist() + ['Thick'])
                plt.plot(sd, 'b', alpha=0.1)
                
        
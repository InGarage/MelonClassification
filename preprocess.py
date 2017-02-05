
import scipy.io.wavfile
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

# Read the audio file assume that the file is a 16bits 2ch (stereo) wave file
def readAudioFile(filename, resample=False, newBitRate=8, newSamplingRate=8000):
    fs, y1 = scipy.io.wavfile.read(filename)
    
    # Select only left channel
    left = y1[:,0]
    left = np.abs(left)
        
    # Resample and change the bit rate if needed
    if resample:
        if newBitRate == 8:
            left = np.floor(left / 256)
        else:
            raise ValueError('the bitrate specify is not supported yet');
        
        left = signal.resample(left, left.size // (fs/newSamplingRate))
        
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
    
    output_filename = 'data_small_resampled.csv'
    sand_sound_folder = 'data/sand_small'    # 'data/sand' or 'data/sand_small'
    thick_sound_folder = 'data/thick_small'   # 'data/thick' or 'data/thick_small'
               
    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
        csvwriter.writerow(list(range(1, 17)) + ['class'])
        
        #plt.axis([18,25,0,1000]) 
        
        sandFileName = os.listdir(sand_sound_folder)
        for filename in sandFileName:
            if ('.wav' in filename):
                audio = readAudioFile(os.path.join(sand_sound_folder, filename), True, 8, 8000)
                sd = calculateParameter(audio, 30, 1024, 64)
                csvwriter.writerow(sd.tolist() + ['sand'])
                plt.plot(sd, 'r')
                    
        sandFileName = os.listdir(thick_sound_folder)
        for filename in sandFileName:
            if ('.wav' in filename):
                audio = readAudioFile(os.path.join(thick_sound_folder, filename), True, 8, 8000)
                sd = calculateParameter(audio, 30, 1024, 64)
                csvwriter.writerow(sd.tolist() + ['thick'])
                plt.plot(sd, 'b', alpha=0.2)
                
        